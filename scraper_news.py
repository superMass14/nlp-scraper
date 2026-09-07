from termcolor import colored
from config import website_address, number_of_post,  driver_version, database_path
from utils.scraper import Scraper
from utils.database import Database
from utils.tools import printc

db = Database(database_path)
try:
    webscrapper = Scraper()
    data = webscrapper.scrap(url=website_address, number=number_of_post)
    urls = Scraper.get_post_urls(posts_tab=data, css_selector="a")
    print(colored("Post's url fetched successfully", "green", attrs=["bold"]))
    n = webscrapper.get_articles(urls, db)
    print(colored(f"{n} articles have been successfully stored✅ ", "green", attrs=["bold"]))
except KeyboardInterrupt:
    printc(f"\nScraper engine has been stopped❌ ", "red", attrs=["bold"])