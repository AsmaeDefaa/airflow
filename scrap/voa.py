
 
from selenium.webdriver.common.by import By
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin
from datetime import datetime
import w3lib

class Voaspider(scrapy.Spider):
    name = "voa"

    start_urls = ["https://www.voaafrique.com/Maroc"]
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(Voaspider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        self.driver = webdriver.Chrome()
       

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Attendez que la page soit complètement chargée (ajustez selon vos besoins)

        while True:
            # Scraper les titres, les dates et les liens de la page actuelle
            body = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

            articles = response.xpath('//*[@id="ordinaryItems"]/li/div')
            for article in articles:
                title = article.xpath('.//div/a/h4/text()').extract_first().strip()
                date = article.xpath('.//span/text()').extract_first().strip()
                link = article.xpath('.//div/a/@href').extract_first().strip()

                # Rendre l'URL absolue
                absolute_url = urljoin(response.url, link)

                yield scrapy.Request(url=absolute_url, callback=self.parse_article, meta={'title': title, 'date': date, 'link': absolute_url})

            # Vérifiez s'il y a un bouton de pagination et cliquez dessus
            next_button_element = self.driver.find_element(By.CSS_SELECTOR, 'p.buttons.btn--load-more > a')
            if next_button_element:
                next_button_element.click()
                time.sleep(20)  # Attendez que la nouvelle page soit complètement chargée (ajustez selon vos besoins)
            else:
                break

    def parse_article(self, response):
        title = response.meta['title']
        date = response.meta['date']
        link = response.meta['link']
        content = w3lib.html.remove_tags(''.join(response.xpath('//div[@class="col-xs-12 col-sm-12 col-md-8 col-lg-8 pull-left bottom-offset content-offset"]//p').extract()))

        yield {
            'title': title,
            'url': link,
            'date': date,
            
            'content': content,
            'source': self.name
        }

    def closed(self, reason):
        self.driver.quit()
"""from selenium.webdriver.common.by import By
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin

class NytimesSpider(scrapy.Spider):
    name = "voa"

    start_urls = ["https://www.voaafrique.com/Maroc"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        super(NytimesSpider, self).__init__()

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Attendez que la page soit complètement chargée (ajustez selon vos besoins)

        while True:
            # Scraper les titres, les dates et les liens de la page actuelle
            body = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

            articles = response.xpath('//*[@id="ordinaryItems"]/li/div')
            for article in articles:
                title = article.xpath('.//div/a/h4/text()').extract_first().strip()
                date = article.xpath('.//span/text()').extract_first().strip()
                link = article.xpath('.//div/a/@href').extract_first().strip()

                # Rendre l'URL absolue
                absolute_url = urljoin(response.url, link)

                yield scrapy.Request(url=absolute_url, callback=self.parse_article, meta={'title': title, 'date': date, 'link': absolute_url})

            # Vérifiez s'il y a un bouton de pagination et cliquez dessus
            next_button_element = self.driver.find_element(By.CSS_SELECTOR, 'p.buttons.btn--load-more > a')
            if next_button_element:
                next_button_element.click()
                time.sleep(20)  # Attendez que la nouvelle page soit complètement chargée (ajustez selon vos besoins)
            else:
                break

    def parse_article(self, response):
        title = response.meta['title']
        date = response.meta['date']
        link = response.meta['link']
        content = response.xpath('//div[@id="article-content"]//p/text()').extract()

        yield {
            'title': title,
            'date': date,
            'link': link,
            'content': content
        }

    def closed(self, reason):
        self.driver.quit()"""
