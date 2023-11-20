import random
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from joblib import dump

DATASET_PATH = Path('./data/output/combined.csv')
OUTPUT_PATH = Path('./data/models')

TOKEN_PATTERN = r'(\b[A-Za-z_]\w*\b|[!#$%&*+:\-./<=>?@\\^_|~]+|[ \t(),;{}\[\]`"\'])'

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

MAX_FEATURES = 1000
N_ESTIMATORS = 50
MAX_DEPTH = 50

if __name__ == '__main__':
    df = pd.read_csv(DATASET_PATH)

    X, y = df.content, df.language
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    vectorizer = TfidfVectorizer(token_pattern=TOKEN_PATTERN, max_features=MAX_FEATURES, norm=None)
    classifier = RandomForestClassifier(n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH)

    print('Fitting vectorizer')
    X_train = vectorizer.fit_transform(X_train)

    print('Fitting classifier')
    classifier.fit(X_train, y_train)

    X_test = vectorizer.transform(X_test)
    score = classifier.score(X_test, y_test)
    print(f'Estimated accuracy: {score * 100:.2f}%')

    print('Dumping models')
    dump(classifier, OUTPUT_PATH / f'classifier_f{MAX_FEATURES}_e{N_ESTIMATORS}_d{MAX_DEPTH}_a{score:.4f}.joblib')
    dump(vectorizer, OUTPUT_PATH / f'vectorizer_f{MAX_FEATURES}.joblib')
