# Telegram-LanguageML

## Datasets

| Source                                                                   | Samples |
|--------------------------------------------------------------------------|---------|
| [Telegram](https://data-static.usercontent.dev/ml2023-r1-dataset.tar.gz) | 21738   |
| [RosettaCode](https://github.com/acmeism/RosettaCodeData)                | 19820   |
| [GitHub](https://www.kaggle.com/datasets/github/github-repos)            | 106836  |
| [Generated](https://github.com/tzador/tglang/tree/main/data/snippets)    | 30165   |

1. **Telegram**: code snippets from the first round of the competition (available labels are `CODE` and `OTHER`)
2. **RosettaCode**: code snippets from  https://rosettacode.org/ (missing languages
   are `CSS`, `DOCKER`, `FUNC`, `HTML`, `NGINX`, `OTHER`, `SOLIDITY`, `TL` and `XML`)
3. **GitHub**: code snippets from GitHub using a modification of the original
   [Kaggle Notebook](https://www.kaggle.com/code/amalhasni/creating-labeled-code-snippets-dataset)
   based on GitHub Repos dataset (`TL` and `FUNC` languages are excluded).
4. **Generated**: code snippets generated via ChatGPT by [tzador](https://github.com/tzador) for the first round of the
   competition.
