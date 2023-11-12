import pandas as pd
from pathlib import Path

INPUT_PATH = '../input/ml2023-r1-dataset'
OUTPUT_PATH = '../output/telegram.csv'

if __name__ == '__main__':
    directory_path = Path(INPUT_PATH)
    files = tuple(directory_path.rglob('*.txt'))

    df = pd.DataFrame({
        'text': [file.read_text() for file in files],
        'label': ['CODE' if 'CODE' in str(file) else 'OTHER' for file in files]
    })

    total_samples = len(df)
    label_percentages = df['label'].value_counts(normalize=True) * 100

    print('Total number of samples:', total_samples)
    print('Samples distribution:')
    for label, percentage in label_percentages.items():
        print(f'  - {label}: {percentage:.1f}%')

    df.to_csv(OUTPUT_PATH, index=False)
    print(f'Dataset saved to "{OUTPUT_PATH}".')
