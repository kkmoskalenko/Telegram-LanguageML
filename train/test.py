import csv
import sys
import time

from argparse import ArgumentParser
from pathlib import Path
from subprocess import getoutput
from tempfile import NamedTemporaryFile


def predict():
    tmp.seek(0)
    tmp.truncate()
    tmp.write(content)
    tmp.flush()

    start = time.time()
    lang = getoutput(f'{args.tester} {tmp.name}')

    return lang, time.time() - start


if __name__ == '__main__':
    parser = ArgumentParser(description='Measures the accuracy and speed of a tglang binary.')
    parser.add_argument('tester', type=Path, help='a path to the tglang-tester executable')
    parser.add_argument('dataset', type=Path, help='a path to the CSV file containing the test dataset')
    parser.add_argument('-m', '--max-samples', type=int, default=sys.maxsize,
                        help='a maximum number of samples from the test dataset for metrics evaluation')
    parser.add_argument('-r', '--report-step', type=int, default=1_000,
                        help='number of processed samples, after which a report message should be printed')
    args = parser.parse_args()

    csv.field_size_limit(sys.maxsize)

    total_samples = 0
    total_time = 0
    true_predictions = 0

    with (
        open(args.dataset, 'r') as csv_file,
        NamedTemporaryFile('w') as tmp
    ):
        reader = csv.reader(csv_file)

        for (content, language) in reader:
            if total_samples >= args.max_samples:
                break

            prediction, duration = predict()
            total_time += duration

            total_samples += 1
            if total_samples % args.report_step == 0:
                print('Samples processed:', total_samples)
            if language == prediction:
                true_predictions += 1

    if total_samples % args.report_step != 0:
        print('Samples processed:', total_samples, end='\n\n')
    else:
        print()

    print(f'Accuracy: {true_predictions / total_samples * 100:.2f}%')
    print(f'Average time per sample: {total_time / total_samples * 1000:.2f} ms')
