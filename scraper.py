import requests
import yaml
from bs4 import BeautifulSoup
import concurrent.futures
import os
import threading

from csv_maker import CsvMaker
from parsers.parser import Parser

PER_PAGE_DATA = "250"
COURSE = "COURSE"
PAGES = "PAGE_LIMIT"
BASE_URL = "BASE_URL"

class Scraper(object):

    def __init__(self):
        self.__load_config()
        self.parser = Parser()
        self.csv_maker = CsvMaker()
        self.page_number = 1
        self.lock = threading.Lock()  # Lock for thread-safe access to data
        self.data = []

    def scrape(self):
        max_threads = 10
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            future_to_page = {executor.submit(self.scrape_page, page_no): page_no for page_no in range(1, self.config[PAGES])}

            for future in concurrent.futures.as_completed(future_to_page):
                page_no = future_to_page[future]
                try:
                    page_data = future.result()
                    with self.lock:
                        self.data += page_data
                except Exception as e:
                    print(f"Error scraping page {page_no}: {e}")

        self.csv_maker.make(self.data)

    def scrape_page(self, page_no):
        print("Scraping Page No: {}".format(page_no))
        resp = requests.get(self.__url_endpoint(), self.__query_dict(page_no))
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.findAll(True, {'class': 'row mb-2'})
        return self.parser.parse(table)

    def __load_config(self):
        self.config = yaml.safe_load(open('config.yaml'))

    def __url_endpoint(self):
        return self.config[BASE_URL]

    def __query_dict(self, page_no):
        return {'pp': PER_PAGE_DATA, 'p': page_no}