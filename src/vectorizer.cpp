#include "vectorizer.h"

Vectorizer::IdfVector Vectorizer::loadVocabulary(const std::string &filePath) {
    IdfVector idfVector;
    std::ifstream file(filePath);

    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return idfVector;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string token;
        double idf;

        size_t pos;
        idf = std::stod(line, &pos);

        token = line.substr(pos + 1);
        idfVector.emplace_back(token, idf);
    }

    file.close();
    return idfVector;
}

std::vector<double> Vectorizer::vectorize(const std::string &inputString, const IdfVector &idfVector) {
    std::unordered_map<std::string, int> termCount;
    std::vector<double> tfidf;

    const std::regex pattern(Vectorizer::tokenizeRegex);
    const auto words_begin = std::sregex_iterator(inputString.begin(), inputString.end(), pattern);
    const auto words_end = std::sregex_iterator();

    int totalTerms = 0;
    for (std::sregex_iterator it = words_begin; it != words_end; it++) {
        termCount[(*it).str()]++;
        totalTerms++;
    }

    for (const auto &pair: idfVector) {
        const std::string token = pair.first;
        const double idf = pair.second;

        double tf;
        try {
            tf = termCount.at(token);
            // tf /= totalTerms;
        } catch (const std::out_of_range &) {
            tf = 0;
        }

        tfidf.push_back(tf * idf);
    }

    return tfidf;
}