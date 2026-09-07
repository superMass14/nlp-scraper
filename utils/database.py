import sqlite3
import uuid

from termcolor import colored

from utils.article import Article
class Database:
    def __init__(self, db_name=""):
        self.db_path = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ARTICLE (
            id TEXT PRIMARY KEY NOT NULL,
            url TEXT NOT NULL,
            date TEXT NOT NULL,
            headline TEXT UNIQUE NOT NULL,
            body TEXT NOT NULL
            )
            """
        )
        self.connection.commit()
        print(colored("Database connected successfully✅ ", "green", attrs=["bold"]))

    def insert(self, article = Article):
        article.uuid= str(uuid.uuid4())
        self.cursor.execute(
            """
            INSERT INTO ARTICLE
            (id, url, date, headline, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            (article.uuid, article.url, str(article.date), article.headline, article.body)
        )
        self.connection.commit()

    def fetch_all_articles(self) -> list[Article]:
        self.cursor.execute(
            """
            SELECT * FROM ARTICLE
            """
        )
        raw_articles = self.cursor.fetchall()
        parsed_articles = []
        for article in raw_articles:
            parsed_articles.append(Article(article[0], article[1], article[2], article[3], article[4]))
        return parsed_articles

    def fetch_articles(self, number=1):
        self.cursor.execute(
            """
            SELECT * FROM ARTICLE
            LIMIT ? 
            """,
            (number,)
        )
        raw_articles = self.cursor.fetchall()
        parsed_articles = []
        for article in raw_articles:
            parsed_articles.append(Article(article[0], article[1], article[2], article[3], article[4]))
        return parsed_articles
