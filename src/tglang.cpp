#include "tglang.h"
#include "vectorizer.h"
#include "weights.h"
#include "random-forest/decision-trees.hxx"

using namespace andres::ml;

enum TglangLanguage tglang_detect_programming_language(const char *text) {
    const auto idfVector = defaultVocabulary;
    const auto vector = Vectorizer::vectorize(text, idfVector);

    const size_t shape[] = {1, idfVector.size()};
    andres::Marray<double> inputVector(shape, shape + 2);
    for (size_t i = 0; i < vector.size(); i++) {
        inputVector(i) = vector[i];
    }

    DecisionForest<double, int, double> decisionForest;
    std::stringstream stream(tree);
    decisionForest.deserialize(stream);

    andres::Marray<double> probabilities(shape, shape + 2);
    decisionForest.predict(inputVector, probabilities);
    const auto classes_count = probabilities.shape(1);

    double max_prob = 0;
    size_t max_index = 0;

    for (size_t i = 0; i < classes_count; i++) {
        const auto prob = probabilities(0, i);
        if (prob > max_prob) {
            max_prob = prob;
            max_index = i;
        }
    }

    return static_cast<TglangLanguage>(max_index);
}