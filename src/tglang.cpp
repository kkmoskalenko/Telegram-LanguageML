#include <regex>
#include <unordered_map>

#include "tglang.h"

#include "generated/vocabulary.generated.h"
#include "generated/trees.generated.h"

constexpr auto tokenizeRegex = R"((\b[A-Za-z_]\w*\b|[!#$%&*+:\-./<=>?@\\^_|~]+|[ \t(),;{}\[\]`"\']))";

std::vector<double> vectorize(const std::string &inputString) {
    std::unordered_map<std::string, int> termCount;
    std::vector<double> tfidf;

    const std::regex pattern(tokenizeRegex);
    const auto words_begin = std::sregex_iterator(inputString.begin(), inputString.end(), pattern);
    const auto words_end = std::sregex_iterator();

    size_t totalTerms = 0;
    for (std::sregex_iterator it = words_begin; it != words_end; it++) {
        termCount[(*it).str()]++;
        totalTerms++;
    }

    for (const auto &feature: vocabulary) {
        double tf;
        try {
            tf = termCount.at(feature.term);
        } catch (const std::out_of_range &) {
            tf = 0;
        }

        tfidf.push_back(tf * feature.idf);
    }

    return tfidf;
}

enum TglangLanguage tglang_detect_programming_language(const char *text) {
    constexpr int N_LANGUAGES = TGLANG_LANGUAGE_XML + 1;
    int votes[N_LANGUAGES] = {0};

    const auto features = vectorize(text);
    for (const auto tree: trees) {
        votes[tree(features.data())]++;
    }

    const auto max_element = std::max_element(votes, votes + N_LANGUAGES);
    return static_cast<TglangLanguage>(std::distance(votes, max_element));
}
