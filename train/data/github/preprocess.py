import pandas as pd
from train.utils import Language

INPUT_PATH = '../input/github.csv'
OUTPUT_PATH = '../output/github.csv'


def update_language(name):
    try:
        return Language[name].value
    except KeyError:
        return None


if __name__ == '__main__':
    df = pd.read_csv(INPUT_PATH)
    df['label'] = df['language'].map(update_language)
    df.rename(columns={'content': 'text'}, inplace=True)
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
