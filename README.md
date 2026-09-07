# 📰 NLP-SCRAPER

## 📌 Overview

This project aims to build an NLP-enriched News Intelligence platform that automatically scrapes news,
detects organizations, classifies topics, analyzes sentiment, and identifies environmental scandals 🌍.
It supports analysts by reducing information overload and highlighting the most relevant content 📊.

---

## 🎯 Objectives

- 🕸️ Scrape and store recent news articles
- 🏢 Detect organizations (entities) using NLP
- 🧠 Classify articles by topic (Tech, Sport, Business, Entertainment, Politics)
- 😊 Perform sentiment analysis (positive, neutral, negative)
- ⚠️ Detect environmental scandals related to organizations
- 📈 Analyze news sources and trends over time

---

## 📁 Project Structure
```
📁nlp-scraper
|__________📁data
|          |____articles.db
|          |____keywords.csv
|__________📁results
|          |_______📁plots
|                  |____(plots image...)
|          |_______enhanced_news.csv 
|          |_______source analysis.ipynb
|          |_______training_model.ipynb
|          |_______xgboost_learning curve.png
|__________📁utils
|          |_____article.py
|          |_____database.py
|          |_____nlp.py
|          |_____scraper.py
|          |_____tools.py    
|__________.gitignore
|__________config.py
|__________nlp-enriched_news.py
|__________README.md
|__________requirements.txt
|__________scraper_news.py
|__________topic_classifier.pkl
```
***
## ⚙️ Installation
### 1. Clone repo
```bash
git clone https://learn.zone01dakar.sn/git/mthiaw/nlp-scraper.git
cd nlp-scraper
```

### 2. create a conda environment and install dependencies
```bash
conda create --name 01env --file "requirements.txt"
```

### 3. Download necessary models (_beware having enough space_)
```bash
//for sentence embedding
python -m spacy 
pip install sentence-transformers

// download all necessary modules for nltk package
python -c "import nltk; nltk.download()"

// nlp models
python -m spacy download fr_core_news_lg 571mb
python -m spacy download en_core_web_lg 400mb
```
***
## 🚀How to use ?
### a. specify parameters in `[config.py]`(config.py)
```python
#config.py
website_address = "do not modify"
driver_version = "specify your chrome driver version"
driver_path = "driver path with 'driver.path' after installation"
number_of_post = 300 #must be a power of 10
database_path = "data/articles.db" # can be modified
result_output_path = "results/enhanced_news.csv" # can be modified
```

### b. run the scraper to retrieves articles
```bash
python scraper_news.py
```

### c. run the nlp engine to analyze articles
```bash
python nlp-enriched_news.py
```
### d. check your results in the given `result_output_path `
***
## 🔍 Embeddings & Similarity Method
For scandal detection:

| 🧩 element | 🏷️ Name              | 📝explanation |
|------------|-----------------------|-------------|
| 🔤Embedding  | Sentence Transformers | it casts long text into vectors by capturing the context.Allowing a better classification |
| 📏Similarity | Cosine_similarity     | useful to compare semantic closeness and easy to use with the available documentation |

The scandal score is based on how close the news content is to a set of environmental 
disaster keywords.

***
## 📊 Insights
You can check some insights in [results/source analysis.ipynb](results/source%20analysis.ipynb)
***
## 🤝Contribution
| Author |[![mthiaw](https://img.shields.io/badge/Zone01-mthiaw-blue)](http://learn.zone01dakar.sn/git/mthiaw) |
|--------|-----------------------------------------------------------------------------------------------------|
| Peer   | [![alogou](https://img.shields.io/badge/Zone01-alogou-darkgreen)](http://learn.zone01dakar.sn/git/alogou)|
