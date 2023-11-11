#ifndef TGLANG_VECTORIZER_H
#define TGLANG_VECTORIZER_H

#include <fstream>
#include <iostream>
#include <sstream>
#include <regex>

class Vectorizer {
public:
    using IdfVector = std::vector<std::pair<std::string, double>>;

    static IdfVector loadVocabulary(const std::string &filePath);

    static std::vector<double> vectorize(const std::string &inputString, const IdfVector &idfVector);

private:
    static constexpr auto preprocessRegex = R"(\b([A-Za-z])\1+\b|\b[A-Za-z]\b)";
    static constexpr auto tokenizeRegex = R"(\b[A-Za-z_]\w*\b|[!\#\$%\&\*\+:\-\./<=>\?@\\\^_\|\~]+|[ \t\(\),;\{\}\[\]`"'])";

    static std::string preprocess(const std::string &inputString) {
        const std::regex pattern(preprocessRegex);
        return std::regex_replace(inputString, pattern, "");
    }
};

#endif //TGLANG_VECTORIZER_H
