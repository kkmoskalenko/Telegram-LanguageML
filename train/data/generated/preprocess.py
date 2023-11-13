import pandas as pd

from train.utils import Language
from pathlib import Path

INPUT_PATH = '../input/tzador-tglang/data/snippets'
OUTPUT_PATH = '../output/generated.csv'


def get_language_value(name):
    try:
        return Language[f'TGLANG_LANGUAGE_{name}'].value
    except KeyError:
        return None


if __name__ == '__main__':
    directory_path = Path(INPUT_PATH)
    files = tuple(directory_path.rglob('*.txt'))

    df = pd.DataFrame({
        'text': [file.read_text() for file in files],
        'label': [get_language_value(file.parent.stem) for file in files],
        'language': [file.parent.stem for file in files]
    })
    df.dropna(inplace=True)
    df['label'] = df['label'].astype(int)

    total_samples = len(df)
    label_percentages = df['language'].value_counts(normalize=True) * 100

    print('Total number of samples:', total_samples)
    print('Samples distribution:')
    for label, percentage in label_percentages.items():
        print(f'  - {label}: {percentage:.1f}%')

    df.to_csv(OUTPUT_PATH, index=False, columns=('text', 'label'))
    print(f'Dataset saved to "{OUTPUT_PATH}".')
