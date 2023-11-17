import json
import numpy as np

from sklearn.tree import _tree
from sklearn.utils.validation import check_is_fitted


def export_vocabulary(tfidf_vectorizer, spacing=4, decimals=6):
    feature_names = tfidf_vectorizer.get_feature_names_out()
    idf_values = tfidf_vectorizer.idf_

    if spacing <= 0:
        raise ValueError(f'spacing must be > 0, given {spacing:d}')

    if decimals < 0:
        raise ValueError(f'decimals must be >= 0, given {decimals:d}')

    indent = ' ' * spacing
    result = ['const struct Feature vocabulary[] = {']

    for term, idf in zip(feature_names, idf_values):
        result.append(f'{indent}{{ {json.dumps(term)}, {idf:.{decimals}f} }},')

    result.append('};\n')
    return '\n'.join(result)


def export_tree(decision_tree, function_name='tree', decimals=6):
    check_is_fitted(decision_tree)

    tree_ = decision_tree.tree_
    # class_names = decision_tree.classes_

    if decimals < 0:
        raise ValueError(f'decimals must be >= 0, given {decimals:d}')

    feature_names_ = [f'f[{i}]' for i in tree_.feature]
    export_tree.report = [f'enum TglangLanguage {function_name}(const double *f) {{']

    def recurse(node):
        if tree_.n_outputs == 1:
            value = tree_.value[node][0]
        else:
            value = tree_.value[node].T[0]
        class_name = np.argmax(value)

        # if tree_.n_classes[0] != 1 and tree_.n_outputs == 1:
        #     class_name = class_names[class_name]

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names_[node]
            threshold = tree_.threshold[node]
            export_tree.report.append(f'if({name} <= {threshold:.{decimals}f})')
            recurse(tree_.children_left[node])

            export_tree.report.append('else')
            recurse(tree_.children_right[node])
        else:
            export_tree.report.append(f'return {class_name};')

    recurse(0)
    export_tree.report.append('}')

    return ' '.join(export_tree.report)
