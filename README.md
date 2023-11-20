# Telegram-LanguageML

The repository contains a library for classifying programming and markup languages, submitted to the second round
of the [Telegram ML Competition 2023](https://contest.com/docs/ML-Competition-2023-r2).

## Solution

1. Preprocessing
    - Tokenize the input string with the following regular expression:
      ```regexp
      (\b[A-Za-z_]\w*\b|[!#$%&*+:\-./<=>?@\\^_|~]+|[ \t(),;{}\[\]`"'])
      ```
    - Using a predefined vocabulary, calculate a **TF-IDF** value for each known token

2. Prediction
    - The **random forest** model was used for classification
    - Each decision tree was ported to C code consisting of `if/else` statements

##### Model Configuration

- 1000 TF-IDF features
- 50 decision trees
- maximum tree depth of 50

##### Estimated Metrics

- **Accuracy**: `94.55%`
- **F1**: `94.77%`
- **Inference time**: `3.95 ms`

Keep in mind that these metrics were measured on a similar dataset to the original training dataset
and may differ significantly when measured on different data. For more details about the trained classifier,
the confusion matrix can be found in [the notebook](./train/notebooks/evaluate.ipynb).

## Datasets

| Source                                                                   | Samples |
|--------------------------------------------------------------------------|---------|
| [Telegram](https://data-static.usercontent.dev/ml2023-r1-dataset.tar.gz) | 21738   |
| [RosettaCode](https://github.com/acmeism/RosettaCodeData)                | 19820   |
| [GitHub](https://www.kaggle.com/datasets/github/github-repos)            | 106836  |
| [Generated](https://github.com/tzador/tglang/tree/main/data/snippets)    | 30165   |
| Manual                                                                   | 526     |

1. **Telegram**: code snippets from the first round of the competition (available labels are `CODE` and `OTHER`)
2. **RosettaCode**: code snippets from  https://rosettacode.org/ (missing languages
   are `CSS`, `DOCKER`, `FUNC`, `HTML`, `NGINX`, `OTHER`, `SOLIDITY`, `TL` and `XML`)
3. **GitHub**: code snippets from GitHub using a modification of the original
   [Kaggle Notebook](https://www.kaggle.com/code/amalhasni/creating-labeled-code-snippets-dataset)
   based on GitHub Repos dataset (`TL` and `FUNC` languages are excluded).
4. **Generated**: code snippets generated via ChatGPT by [tzador](https://github.com/tzador) for the first round of the
   competition.
5. **Manual**: `TL` and `FUNC` snippets were gathered semi-manually from GitHub.

The combined training dataset has an unbalanced class distribution with a predominance of the `OTHER` class.
More information about the collected data can be found in [the notebook](./train/notebooks/dataset.ipynb).

## Building

To export a shared library `libtglang.so` built for Debian GNU/Linux 10 (buster) run the following command:

```shell
DOCKER_BUILDKIT=1 docker build --no-cache --target export-lib --output out .
```

> **NOTE**: Due to the generated C files with large nested if/else statements,
> the compilation stage may take approximately 15 minutes.

To evaluate metrics of the built library on a test dataset, run:

```shell
docker run --rm -it $(docker build -q .)
```