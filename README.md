# KGDescription


This repository serves as an automatic detailed description generator for Knowledge Graphs (KGs). It is a pivotal component within the [Anchoring Path Sentence Transformer (APST)](https://github.com/AAAI2024AnonymousSubmission13023/APST) detailed description retrieval process.

## Supported Datasets

The current applicable datasets for description generation include:

- FB15k-237
- NELL-995
- WN18RR

If you wish to generate descriptions for other datasets, you can extend the functionality by providing a file named `entity2text.txt`. This file should contain the following information:

- Entity name (or ID)
- A brief description

## Data Sources

KGDescription utilizes various sources to generate descriptions:

- **GoogleWikipedia**: Utilizes the Google Custom Search API to find Wikipedia pages matching specified keywords.
- **GoogleWiktionary**: Utilizes the Google Custom Search API to find Wiktionary pages matching specified keywords.
- **Wikipedia**: Directly searches provided keywords on Wikipedia.
- **Wiktionary**: Directly searches provided keywords on Wiktionary.
- **OpenAI**: Utilizes the GPT-3.5-turbo API to generate descriptions for provided keywords.

Please note that certain sources require additional API keys, which must be provided in the following files:

- `.api_key_google`: Obtain this API key by referring to the official documentation: [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- `.cx_google`: Create a custom search engine [here](https://programmablesearchengine.google.com/controlpanel/all)
- `.api_key_openAI`: Generate an API key from OpenAI [here](https://platform.openai.com/account/api-keys)

Be aware that these API keys may involve costs. Please manage your usage responsibly.

## Getting Started

```bash
python get_descriptions.py --dataset $dataset --char_len $char_len --source $source
