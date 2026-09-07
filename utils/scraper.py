import sys

from selenium.common import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import driver_path
from termcolor import colored
import time, random
from sqlite3 import IntegrityError
from utils.article import Article
from utils.tools import progress_bar, separator


class Scraper:
    def __init__(self):
        """
        if ChromeDriver is not installed in your machine
        uncomment the following and comment the 'service = Service(driver_path)' line
        """

        # print("Installing chrome driver...", end="", flush=True)
       # service = Service(ChromeDriverManager(driver_version=driver_version).install())
       # print("\rInstalling chrome driver ✅\n")
        service = Service(driver_path)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        print("Connecting webdriver...", end="", flush=True)
        self.driver =  webdriver.Chrome(service=service, options=options)
        print(colored("\rWebdriver connected✅ ", color="green", attrs=["bold"]))

    def scrap(self, url="", number=0) ->list[WebElement]:
        if number % 10 != 0:
            print(colored("number of post must be a multiple of 10❌ ", "red", attrs=["bold"]))
        posts_tab = []
        try:
            self.driver.get(url)

            print("Starting the scraping\nFetching urls....", flush=True)
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                posts_tab = self.driver.find_elements(By.CSS_SELECTOR, "#posts-container > .post-card")
                progress_bar(current=len(posts_tab), total=number, model="|", comment="post url")
                if len(posts_tab) >= number:
                    break
                else:
                    time.sleep(random.uniform(2, 3))
            print(f"\n'{self.driver.title}' website has been found", flush=True)
        except WebDriverException as e :
            print(colored(f"scraper engine has been stopped❌ \n\r{e.msg}", "red", attrs=["bold"]), flush=True)
            sys.exit(1)
        return posts_tab


    @staticmethod
    def get_post_urls(posts_tab, css_selector="") -> list[tuple[str, str]]:
        return [(post.find_elements(By.CSS_SELECTOR, css_selector)[0].get_attribute("href"), post.get_attribute("id")) for post in posts_tab]

    def get_articles(self, link_tab, db) -> int:
        n =0
        for i, link in enumerate(link_tab):
            separator()
            print(f"{i+1}. scraping <{colored(link[0], attrs=["underline"])}>")

            # requesting
            print("\t- requesting...", end="", flush=True)

            try:
                self.driver.get(link[0])
            except WebDriverException as e :
                print(colored(f"scraper engine has been stopped❌ \n\r{e.msg}", "red", attrs=["bold"]), flush=True)
                sys.exit(1)

            print(colored("\r\t- requesting✅ ", "green", attrs=["bold"]))

            # parsing
            print("\t- parsing...", end="", flush=True)
            art = self.driver.find_elements(By.CSS_SELECTOR, f"#{link[1]}")[0]
            date = art.find_elements(By.TAG_NAME, "time")[0].get_attribute("datetime")
            body = art.find_elements(By.CLASS_NAME, "article-detail-content123")[0].text
            headline = self.driver.title
            url = link[0]
            print(colored("\r\t- parsing✅ ", "green", attrs=["bold"]))

            # inserting
            if not headline.__contains__("(vidéo)"):
                try :
                    db.insert(Article(_id="", url=url, date=date, headline=headline, body=body))
                    n +=1
                    print(colored(f"\t- saved in {db.db_path}✅ ", "green", attrs=["bold"]))
                except IntegrityError:
                    print(colored(f"\t- can't be inserted, it already exists❌ ", "red", attrs=["bold"]))
            else:
                print(colored(f"\t- it is not a valid article, contains video❌ ", "red", attrs=["bold"]))

            # pause between requests
            time.sleep(random.uniform(2.0, 4.0))
        separator()
        print("end of scraping")
        self.driver.quit()
        return n