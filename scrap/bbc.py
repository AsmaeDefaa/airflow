"""from urllib.parse import urljoin
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import w3lib
from datetime import datetime

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/news/topics/cx1m7zg0gylt"]
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(BbcSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        self.driver = webdriver.Chrome()  # Ensure the path to your driver is correct



    def parse(self, response):
        self.driver.get(response.url)
        while True:
            # Attendre que le bouton de pagination suivant soit cliquable
            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pagination-next-button"]'))
            )
            # Cliquer sur le bouton de pagination suivant
            next_button.click()
            # Attendre que la page suivante soit chargée
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h2[@data-testid="card-headline"]'))
            )
            # Créer une réponse HTML à partir de la page actuelle
            html = self.driver.page_source
            response_obj = HtmlResponse(url=self.driver.current_url, body=html.encode('utf-8'))
            # Extraire les titres, les liens, les dates et le contenu de chaque article
            articles = Selector(response=response_obj).xpath('//h2[@data-testid="card-headline"]')
            for article in articles:
                title = article.xpath('text()').get()
                link = article.xpath('ancestor::a/@href').get()
                date = article.xpath('ancestor::div/div/div/div/span/text()').get()
                # Suivre le lien de l'article pour extraire le contenu
                
                absolute_url = urljoin(response.url, link)

                yield scrapy.Request(url=absolute_url, callback=self.parse_article, meta={'title': title, 'date': date, 'link': absolute_url})

            # Vérifier s'il y a un bouton de pagination suivant
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@data-testid="pagination-next-button"]')
            except NoSuchElementException:
                break

    def parse_article(self, response):
        title = response.meta['title']
        date = response.meta['date']
        link = response.meta['link']
        
        #content = response.xpath('//section[@data-component="text-block"]/p/text()').get()
        content = w3lib.html.remove_tags(''.join(response.xpath('//div[@class="ssrcss-7uxr49-RichTextContainer e5tfeyi1"]//p').extract()))

        yield {'title': title,'url':link, 'date': date, 'content': content}

    def closed(self, reason):
        self.driver.quit()"""


from urllib.parse import urljoin
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import w3lib
from datetime import datetime

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/news/topics/cx1m7zg0gylt"]

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(BbcSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        self.driver = webdriver.Chrome()  # Ensure the path to your driver is correct

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            # Wait for the pagination next button to be clickable
            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pagination-next-button"]'))
            )
            # Click the next pagination button
            next_button.click()
            # Wait for the next page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h2[@data-testid="card-headline"]'))
            )
            # Create an HTML response from the current page
            html = self.driver.page_source
            response_obj = HtmlResponse(url=self.driver.current_url, body=html.encode('utf-8'))
            # Extract titles, links, dates, and content of each article
            articles = Selector(response=response_obj).xpath('//h2[@data-testid="card-headline"]')
            for article in articles:
                title = article.xpath('text()').get()
                link = article.xpath('ancestor::a/@href').get()
                date_str = article.xpath('ancestor::div/div/div/div/span/text()').get()
                if date_str:
                    date = self.convert_date(date_str)
                    print(f"Extracted date: {date}, Start date: {self.start_date}, End date: {self.end_date}")  # Debugging line
                    if self.start_date <= date <= self.end_date:
                        # Follow the article link to extract the content
                        absolute_url = urljoin(response.url, link)
                        yield scrapy.Request(url=absolute_url, callback=self.parse_article, meta={'title': title, 'date': date_str, 'link': absolute_url})

            # Check if there is a next pagination button
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@data-testid="pagination-next-button"]')
            except NoSuchElementException:
                break

    def parse_article(self, response):
        title = response.meta['title']
        date = response.meta['date']
        link = response.meta['link']
        content = w3lib.html.remove_tags(''.join(response.xpath('//div[@class="ssrcss-7uxr49-RichTextContainer e5tfeyi1"]//p').extract()))
        yield {'title': title, 'url': link, 'date': date, 'content': content,
               'source': self.name,
               }

    def convert_date(self, date_str):
        # Attempt different date formats
        for fmt in ('%d %B %Y', '%d %b %Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")

    def closed(self, reason):
        self.driver.quit()









"""from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import scrapy

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/news/topics/cx1m7zg0gylt"]

    def __init__(self):
        self.driver = webdriver.Chrome() # Assurez-vous que le chemin vers votre propre driver est correct

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            # Attendre que le bouton de pagination suivant soit cliquable
            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pagination-next-button"]'))
            )
            # Cliquer sur le bouton de pagination suivant
            next_button.click()
            # Attendre que la page suivante soit chargée
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h2[@data-testid="card-headline"]'))
            )
            # Créer une réponse HTML à partir de la page actuelle
            html = self.driver.page_source
            response_obj = HtmlResponse(url=self.driver.current_url, body=html.encode('utf-8'))
            # Extraire les titres, les liens et les dates de la page actuelle
            titles_and_links = Selector(response=response_obj).xpath('//h2[@data-testid="card-headline"]')
            dates = Selector(response=response_obj).xpath('//span[@data-testid="card-metadata-lastupdated"]')  # XPath pour la date
            for title_and_link, date in zip(titles_and_links, dates):
                title = title_and_link.xpath('text()').get()
                link = title_and_link.xpath('@href').get()
                date = date.xpath('text()').get()
                yield {'title': title, 'link': response.urljoin(link), 'date': date}
            # Vérifier s'il y a un bouton de pagination suivant
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@data-testid="pagination-next-button"]')
            except NoSuchElementException:
                break

    def closed(self, reason):
        self.driver.quit()"""
















"""from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import scrapy

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/news/topics/cx1m7zg0gylt"]

    def __init__(self):
        self.driver = webdriver.Chrome() # Assurez-vous que le chemin vers votre propre driver est correct

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            # Attendre que le bouton de pagination suivant soit cliquable
            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pagination-next-button"]'))
            )
            # Cliquer sur le bouton de pagination suivant
            next_button.click()
            # Attendre que la page suivante soit chargée
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h2[@data-testid="card-headline"]'))
            )
            # Créer une réponse HTML à partir de la page actuelle
            html = self.driver.page_source
            response_obj = HtmlResponse(url=self.driver.current_url, body=html.encode('utf-8'))
            # Extraire les titres, les liens et les dates de la page actuelle
            titles_and_links = Selector(response=response_obj).xpath('//h2[@data-testid="card-headline"]')
            dates = Selector(response=response_obj).xpath('//span[@data-testid="card-metadata-lastupdated"]')  # XPath pour la date
            for title_and_link, date in zip(titles_and_links, dates):
                title = title_and_link.xpath('text()').get()
                link = title_and_link.xpath('@href').get()
                date = date.xpath('text()').get()
                yield {'title': title, 'link': response.urljoin(link), 'date': date}
            # Vérifier s'il y a un bouton de pagination suivant
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@data-testid="pagination-next-button"]')
            except NoSuchElementException:
                break

    def closed(self, reason):
        self.driver.quit()
"""
