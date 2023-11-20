import pandas as pd
from pathlib import Path
from random import choices, randint
from utils import Language, ROSETTA_CODE_TO_LANGUAGE

INPUT_DIR = Path(__file__).parent.parent / 'data' / 'input'


def telegram(dataset_id):
    """
    Sources:
      - https://data-static.usercontent.dev/ml2023-r1-dataset.tar.gz
      - https://data-static.usercontent.dev/ml2023-d1-dataset.tar.gz
    """

    dataset_path = f'ml2023-{dataset_id}-dataset'
    directory_path = INPUT_DIR / dataset_path
    files = tuple(directory_path.rglob('*.txt'))

    return pd.DataFrame({
        'content': [file.read_text() for file in files],
        'language': [Language.OTHER if 'OTHER' in str(file) else pd.NA for file in files],
        'source': f'telegram-{dataset_id}'
    })


def rosetta_code(dataset_path='RosettaCodeData'):
    """
    Source: https://github.com/acmeism/RosettaCodeData
    """

    frames = []

    for (lang_name, language) in ROSETTA_CODE_TO_LANGUAGE.items():
        directory_path = INPUT_DIR / dataset_path / 'Lang' / lang_name
        files = directory_path.glob('*/*')

        frames.append(pd.DataFrame({
            'content': [file.read_text() for file in files],
            'language': language,
            'source': 'rosetta-code'
        }))

    return pd.concat(frames)


def github(dataset_path='github.csv'):
    """
    See directory `github/create-dataset.ipynb`
    """

    df = pd.read_csv(INPUT_DIR / dataset_path)
    df.dropna(inplace=True)
    df.rename(columns={'text': 'content', 'label': 'language'}, inplace=True)
    df['language'] = df['language'].map(Language)
    df['source'] = 'github'
    return df


def generated(dataset_path='tzador-tglang'):
    """
    Source: https://github.com/tzador/tglang
    """

    directory_path = INPUT_DIR / dataset_path / 'data' / 'snippets'
    files = tuple(directory_path.rglob('*.txt'))

    def language(name):
        try:
            return Language[name]
        except KeyError:
            return pd.NA

    return pd.DataFrame({
        'content': [file.read_text() for file in files],
        'language': [language(file.parent.stem) for file in files],
        'source': 'generated'
    }).dropna()


def manual(dataset_path, language, extension='*'):
    """
    Manually gathered code snippets in separate files.
    """

    directory_path = INPUT_DIR / dataset_path
    files = directory_path.rglob(f'*.{extension}')

    return pd.DataFrame({
        'content': [file.read_text() for file in files],
        'language': language,
        'source': f'manual-{language.name.lower()}'
    })


def synthetic(dataset_path, language, extension='*', n_files=1000, min_lines=10, max_lines=50):
    """
    Generates language snippets from random combinations of lines.
    """

    directory_path = INPUT_DIR / dataset_path
    files = directory_path.rglob(f'*.{extension}')

    line_pool = []
    for file in files:
        content = file.read_text()
        for line in content.splitlines():
            line = line.strip()
            if line:
                line_pool.append(line)

    return pd.DataFrame({
        'content': ['\n'.join(
            choices(line_pool, k=randint(min_lines, max_lines))
        ) for _ in range(n_files)],
        'language': language,
        'source': f'synthetic-{language.name.lower()}'
    })


def print_statistics(df):
    total_samples = len(df)
    label_percentages = df['language'].value_counts(normalize=True) * 100

    print(f'--- DATASET "{df.source[0]}" ---')
    print('Total number of samples:', total_samples)
    print('Samples distribution:')
    for label, percentage in label_percentages.items():
        print(f'  - {label}: {percentage:.1f}%')
    print()
