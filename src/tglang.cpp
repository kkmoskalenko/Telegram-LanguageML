#include "tglang.h"

#include <fstream>
#include <iostream>
#include <sstream>
#include <regex>

using IdfVector = std::vector<std::pair<std::string, double>>;

IdfVector readIDF(const std::string &filePath) {
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

std::string preprocess(const std::string &inputString) {
    const std::regex pattern(R"(\b([A-Za-z])\1+\b|\b[A-Za-z]\b)");
    return std::regex_replace(inputString, pattern, "");
}

std::vector<double> vectorize(const std::string &inputString, const IdfVector &idfVector) {
    std::unordered_map<std::string, int> termCount;
    std::vector<double> tfidf;

    const std::regex pattern(R"(\b[A-Za-z_]\w*\b|[!\#\$%\&\*\+:\-\./<=>\?@\\\^_\|\~]+|[ \t\(\),;\{\}\[\]`"'])");
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

enum TglangLanguage tglang_detect_programming_language(const char *text) {
    const auto idf_map = readIDF("../../resources/idf.txt");

    const auto input = preprocess(text);
    const auto vector = vectorize(input, idf_map);

    std::cout << "Input vector: ";
    for (const auto value: vector) {
        std::cout << value << ' ';
    }
    std::cout << std::endl;

    return TGLANG_LANGUAGE_OTHER;
}