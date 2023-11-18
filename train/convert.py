from argparse import ArgumentParser
from joblib import load
from pathlib import Path
from utils import export_tree, export_vocabulary


def export_classifier():
    with open(args.output / 'trees.generated.h', 'w') as f:
        f.write(
            '#ifndef TGLANG_TREES_GENERATED_H\n'
            '#define TGLANG_TREES_GENERATED_H\n\n'
            '#include "../tglang.h"\n\n'
            f'extern enum TglangLanguage (*trees[{classifier.n_estimators}])(const double *);\n\n'
            '#endif //TGLANG_TREES_GENERATED_H\n'
        )

    with open(args.output / 'trees.generated.c', 'w') as f:
        f.write('#include "trees.generated.h"\n\n')
        for index, estimator in enumerate(classifier.estimators_):
            tree_str = export_tree(estimator, function_name=f'tree_{index}')
            f.write(tree_str)
            f.write('\n\n')

        tree_pointers = ', '.join(f'&tree_{i}' for i in range(classifier.n_estimators))
        f.write(f'enum TglangLanguage (*trees[])(const double *) = {{ {tree_pointers} }};\n')


def export_vectorizer():
    with open(args.output / 'vocabulary.generated.h', 'w') as f:
        f.write(
            '#ifndef TGLANG_VOCABULARY_GENERATED_H\n'
            '#define TGLANG_VOCABULARY_GENERATED_H\n\n'
            'struct Feature {\n'
            '    const char *term;\n'
            '    const double idf;\n'
            '};\n\n'
        )
        f.write(export_vocabulary(vectorizer))
        f.write('\n#endif //TGLANG_VOCABULARY_GENERATED_H\n')


if __name__ == '__main__':
    parser = ArgumentParser(description='Converts a random forest model to C code.')
    parser.add_argument('classifier', type=Path, help='a path to the RandomForestClassifier dump')
    parser.add_argument('vectorizer', type=Path, help='a path to the TfidfVectorizer dump')
    parser.add_argument('output', type=Path, help='an output directory path to put the generated C code')
    args = parser.parse_args()

    print('Loading the models')
    classifier = load(args.classifier)
    vectorizer = load(args.vectorizer)

    print('Exporting the decision trees')
    export_classifier()

    print('Exporting the vectorizer vocabulary')
    export_vectorizer()
