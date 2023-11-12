import pandas as pd

from train.utils import Language, ROSETTA_CODE_TO_LANGUAGE
from pathlib import Path

INPUT_PATH = '../input/RosettaCodeData'
OUTPUT_PATH = '../output/rosetta-code.csv'

if __name__ == '__main__':
    frames = []

    for (lang_name, enum) in ROSETTA_CODE_TO_LANGUAGE.items():
        directory_path = Path(INPUT_PATH) / 'Lang' / lang_name
        files = tuple(directory_path.glob('*/*'))

        frames.append(pd.DataFrame({
            'text': [file.read_text() for file in files],
            'label': enum.value,
            'language': lang_name
        }))

    df = pd.concat(frames)

    total_samples = len(df)
    label_percentages = df['language'].value_counts(normalize=True) * 100

    print('Total number of samples:', total_samples)
    print('Samples distribution:')
    for label, percentage in label_percentages.items():
        print(f'  - {label}: {percentage:.1f}%')

    df.to_csv(OUTPUT_PATH, index=False, columns=('text', 'label'))
    print(f'Dataset saved to "{OUTPUT_PATH}".')
