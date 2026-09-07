import time

from utils.database import Database
from utils.tools import printc, bold, top_10, separator
from config import database_path, result_output_path
from utils.nlp import encode_data, analyze_sent
from termcolor import colored
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import joblib
import pandas as pd
import numpy as np

def predict_category(text=""):
    """
    categories = 'business', 'entertainment', 'politics', 'sport', 'tech'
    """
    text = encode_data(text.lower(), nlp_en)
    labels = sorted(["tech", "sport", "business", "entertainment" ,"politics"])
    pred = model.predict(text)[0]
    return labels[pred]

uuid, bodies, urls, dates, heads, topics, sentiments, entities, scandal =[], [], [], [], [], [], [], [],[]

try :
    printc("---------- Starting engine ----------", color="blue", attrs=["bold"])
    model = joblib.load("topic_classifier.pkl")
    embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    nlp_en = spacy.load("en_core_web_lg")
    nlp_fr = spacy.load("fr_core_news_lg")

    keywords = pd.read_csv("data/keywords.csv")["Keywords"].values
    embedded_kw = embedder.encode(keywords)

    db = Database(database_path)
    articles = db.fetch_all_articles()

    for i, article in enumerate(articles, start=1):
        print(f"{i}. Enriching <{colored(article.url, "blue", attrs=["bold", "underline"])}>:")
        print("\rCleaning document...", end="", flush=True)
        body = article.body.strip()
        headline = article.headline.strip()
        heads.append(headline)
        bodies.append(body)
        dates.append(article.date)
        uuid.append(article.uuid)
        urls.append(article.url)

        printc("\rCleaning document✅ ", color="green", attrs=["bold"])

        printc("\n---------- Detect entities ----------\n", color="blue", attrs=["bold"])
        h_entities = nlp_fr(headline).ents
        doc = nlp_fr(body)
        body_entities = doc.ents

        sent_entities = []
        for s in doc.sents:
            for e in s.ents:
                if e.label_ == "ORG":
                    sent_entities.append(str(s))
                    break

        h_orgs = [e.text for e in h_entities if e.label_.__eq__("ORG")]
        b_orgs = [e.text for e in body_entities if e.label_.__eq__("ORG")]
        orgs = list(set(h_orgs + b_orgs))[::-1]
        entities.append(orgs)

        ent = [f"'{x[::-1]}'" for x in orgs]
        if len(orgs) > 0:

            printc(f"Detected {f"{len(orgs)}"} companies which are {", ".join(ent[::-1]).replace(", ", " dna ", 1)[::-1]}", color="yellow", attrs=["bold"])
        else:
            printc(f"No ORG entity has been Detected", color="red", attrs=["bold"])


        printc("\n---------- Topic detection ---------\n", color="blue", attrs=["bold"])
        print("\rText preprocessing...", end="", flush=True)

        pred_topic = predict_category(article.body)
        topics.append(pred_topic)

        printc("\rText preprocessing✅ ", color="green", attrs=["bold"])
        printc(f"The topic of the article is '{pred_topic}'", color="yellow", attrs=["bold"])
        time.sleep(1)

        printc("\n---------- Sentiment analysis ----------", color="blue", attrs=["bold"])
        print("\rText preprocessing...", end="", flush=True)

        article_sentiment = analyze_sent(article.body)
        sentiments.append(article_sentiment[1])

        printc("\rText preprocessing✅ ", color="green", attrs=["bold"])

        printc(f"The article '{headline}' has a {article_sentiment[0]} sentiment", "yellow", attrs=["bold"])
        time.sleep(1)

        printc("\n---------- Scandal detection ----------", color="blue", attrs=["bold"])
        if len(sent_entities) == 0:
            scandal.append(0.0)
            print(colored("There is no ORG entity in article body for scandal detection", "red", attrs=["bold"]))
            separator(model="~")
            continue

        print("\rComputing embeddings and distance...", end="", flush=True)

        embedded_sent = embedder.encode(sent_entities)
        similarity = cosine_similarity(embedded_sent, embedded_kw)
        unify_metric = np.mean(similarity.max(axis=1))
        scandal.append(unify_metric)

        printc("\rComputing embeddings and distance✅ ", "green", attrs=["bold"])

        print(
            colored(
                f"Environmental scandal alert detected for : {", ".join(ent[::-1]).replace(", ", " dna ", 1)[::-1]}",
                      "yellow", attrs=["bold"])\
              if unify_metric >= 0.4\
              else colored("No environmental scandal detected", "yellow")
              )
        separator("~")
        time.sleep(1)
except KeyboardInterrupt:
    printc("\n\rEngine has been interrupted❌ !", color="red", attrs=["bold"])
finally:
    max_size =max(len(uuid), len(bodies), len(urls),len(dates), len(heads), len(topics), len(sentiments), len(entities), len(scandal))
    tabs =[uuid, bodies, urls,dates, heads, topics, sentiments, entities, scandal]

    if max_size == 0:
        printc("No article has been processed❌ ", "red", attrs=["bold"])
    else:
        for i, t in enumerate(tabs):
            if len(t) < max_size:
                tabs[i] = t+[np.nan]* (max_size - len(t))

        table = pd.DataFrame({
             "Unique ID": tabs[0],
             "URL": tabs[2],
             "Date scraped" : tabs[3],
             "body": tabs[1],
             "headline": tabs[4],
             "Org": tabs[7],
             "Topics": tabs[5],
             "Sentiment": tabs[6],
             "Scandal_distance": tabs[8],
         })

        if len(table) > 10:
            table.sort_values(by="Scandal_distance", ascending=False, inplace=True)
            table["Top_10"] = [True] *10 + [False] * (len(table) - 10)
            table.sort_index(inplace=True)

        table.to_csv(result_output_path, index=True)
        print(colored(f"{len(table)} articles have been processed\nResults have been save in ", "green") + \
             colored(f"{result_output_path}", "green", attrs=["bold", "underline"])+ \
               colored(" successfully✅ ", "green") )