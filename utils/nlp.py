from transformers import MarianMTModel, MarianTokenizer
from utils.tools import remove_punctuation
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# uncomment here
#import nltk
#nltk.download()

import numpy as np

def remove_stopwords(text):
    tokens=word_tokenize(text)
    return  " ".join(
        [x for x in tokens if not x in stopwords.words("english")]
    )

def process_text(text) -> list[str]:
    text = text.lower()
    text = remove_punctuation(text)
    sent_tokens = sent_tokenize(text)
    sent_tokens = [remove_stopwords(s) for s in sent_tokens]
    return sent_tokens

def analyze_sent(text="") -> tuple[str, float]:
    sentences = process_text(text)
    analyzer = SentimentIntensityAnalyzer()
    compound = [analyzer.polarity_scores(s)["compound"] for s in sentences]
    mean_compound = np.mean(compound).astype(float)
    return \
        ("Positif", mean_compound) if mean_compound > 0.05 \
            else ("Negative", mean_compound) if mean_compound < -0.05 \
            else ("Neutral", mean_compound)


def translate(text, source_lang="fr", target_lang="en"):
    name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(name)
    translator = MarianMTModel.from_pretrained(name)
    # Encode & translation
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    trans_ids = translator.generate(**inputs)
    translation = tokenizer.batch_decode(trans_ids, skip_special_tokens=True)[0]

    return translation

def encode_data(text, engine):
    return engine(
        remove_punctuation(translate(text))
        ).vector.reshape(1, -1)