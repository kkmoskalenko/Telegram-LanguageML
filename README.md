# Telegram-LanguageML

## Datasets

| Source                                                                   | Samples |
|--------------------------------------------------------------------------|---------|
| [Telegram](https://data-static.usercontent.dev/ml2023-r1-dataset.tar.gz) | 21738   |
| [RosettaCode](https://github.com/acmeism/RosettaCodeData)                | 19820   |
| GitHub                                                                   | 23887   |

1. **Telegram**: code snippets from the first round of the competition (available labels are `CODE` and `OTHER`)
2. **RosettaCode**: code snippets from  https://rosettacode.org/ (missing languages
   are `CSS`, `DOCKER`, `FUNC`, `HTML`, `NGINX`, `OTHER`, `SOLIDITY`, `TL` and `XML`)
3. **GitHub**: code snippets from GitHub using
   the [Kaggle Notebook](https://www.kaggle.com/code/amalhasni/creating-labeled-code-snippets-dataset)
   (at most 1000 for each language). 
