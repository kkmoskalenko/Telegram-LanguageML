#include "tglang.h"
#include "vectorizer.h"
#include "ctpl_stl.h"
#include "random-forest/decision-trees.hxx"

constexpr size_t numberOfDecisionTrees = 1; // 300
constexpr size_t maxTrainingSamples = 5000; // 16500, 130479
constexpr size_t maxThreads = 8;


//using Feature = double;
//using Label = int;
//using Probability = double;

typedef double Feature;
typedef int Label;
typedef double Probability;

using namespace andres;
using namespace andres::ml;

void loadDataset(const Vectorizer::IdfVector &idfVector, Marray<Feature> &features, Marray<Label> &labels) {
    constexpr auto dataset_dir = "../../resources/dataset";
    ctpl::thread_pool pool(maxThreads);

    /*
    std::default_random_engine RandomNumberGenerator;
    std::uniform_real_distribution randomDistribution(0.0, 1.0);
    std::uniform_int_distribution intDistribution(0, 10);
    for(size_t sample = 0; sample < maxTrainingSamples; ++sample) {
        for (size_t feature = 0; feature < idfVector.size(); ++feature) {
            features(sample, feature) = randomDistribution(RandomNumberGenerator);
            labels(sample) = intDistribution(RandomNumberGenerator);
        }
    }
    return;
    */

    size_t sample = 0;
    for (const auto &dir: std::filesystem::recursive_directory_iterator(dataset_dir)) {
        const auto &path = dir.path();
        if (path.extension() != ".txt") {
            continue;
        }
        if (sample >= maxTrainingSamples) {
            break;
        }

        pool.push([&features, &labels, &idfVector, path, sample](int id) {
            std::ifstream file(path);
            std::stringstream buffer;
            buffer << file.rdbuf();

            const auto lang_name = path.parent_path().filename().string();
            const auto underscorePos = lang_name.find('_');
            const auto lang_index = lang_name.substr(0, underscorePos);
            labels(sample) = std::stoi(lang_index);

            const auto vector = Vectorizer::vectorize(buffer.str(), idfVector);
            for (size_t feature = 0; feature < vector.size(); feature++) {
                features(sample, feature) = vector.at(feature);
            }

            if (sample % 1000 == 0) {
                std::cout << "Sample: " << sample << std::endl;
            }
        });

        sample++;
    }

    pool.stop(true);
}

int main() {
    const auto idfVector = Vectorizer::loadVocabulary("../../resources/idf.txt");

    const size_t numberOfFeatures = idfVector.size();
    const size_t numberOfSamples = maxTrainingSamples;
    const size_t shape[] = {numberOfSamples, numberOfFeatures};

    andres::Marray<Feature> features(shape, shape + 2); // A matrix in which every row corresponds to a sample and every column corresponds to a feature.
    andres::Marray<Label> labels(shape, shape + 1); // A vector of labels, one for each sample.

    loadDataset(idfVector, features, labels);

//    std::cout << features.asString();
//    std::cout << labels.asString();

    DecisionForest<Feature, Label, Probability> decisionForest;
    decisionForest.learn(features, labels, numberOfDecisionTrees);

    std::ofstream outFile("trees.txt");
    decisionForest.serialize(outFile);
}