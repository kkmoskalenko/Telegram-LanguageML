import csv
import sys
import time

from argparse import ArgumentParser
from pathlib import Path
from subprocess import getoutput
from tempfile import NamedTemporaryFile

from sklearn.metrics import accuracy_score, f1_score


def accuracy():
    score = accuracy_score(actual, predicted)
    return f'{score:.4f}'


def f1():
    score = f1_score(actual, predicted, average='macro')
    return f'{score:.4f}'


def predict():
    tmp.seek(0)
    tmp.truncate()
    tmp.write(content)
    tmp.flush()

    start = time.time()
    lang = getoutput(f'{args.tester} {tmp.name}')

    return lang, time.time() - start


def average_time():
    return f'{total_time / total_samples * 1000:.2f} ms'


if __name__ == '__main__':
    parser = ArgumentParser(description='Measures the accuracy and speed of a tglang binary.')
    parser.add_argument('tester', type=Path, help='a path to the tglang-tester executable')
    parser.add_argument('dataset', type=Path, help='a path to the CSV file containing the test dataset')
    parser.add_argument('-b', '--binary', action='store_true', help='evaluate metrics for OTHER / CODE labels')
    parser.add_argument('-m', '--max-samples', type=int, default=sys.maxsize,
                        help='a maximum number of samples from the test dataset for metrics evaluation')
    parser.add_argument('-r', '--report-step', type=int, default=1_000,
                        help='number of processed samples, after which a report message should be printed')
    args = parser.parse_args()

    csv.field_size_limit(sys.maxsize)

    total_samples = 0
    total_time = 0

    actual = []
    predicted = []

    with open(args.dataset, 'r') as csv_file, NamedTemporaryFile('w') as tmp:
        reader = csv.reader(csv_file)

        for (content, language) in reader:
            if total_samples >= args.max_samples:
                break

            prediction, duration = predict()
            total_time += duration

            if args.binary:
                prediction = 'OTHER' if prediction == '0' else 'CODE'

            actual.append(language)
            predicted.append(prediction)

            total_samples += 1
            if total_samples % args.report_step == 0:
                print(f'Samples: {total_samples}, accuracy: {accuracy()}, F1: {f1()}, time: {average_time()}')

    if total_samples % args.report_step != 0:
        print('Samples processed:', total_samples, end='\n\n')
    else:
        print()

    print(f'Accuracy: {accuracy()}, F1: {f1()}')
    print('Average time per sample:', average_time())
