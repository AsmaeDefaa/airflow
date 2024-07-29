
import scrapy
from scrapy import Request
import re
import time
from datetime import datetime
class LiberationSpider(scrapy.Spider):
    name = "theguardian"
    allowed_domains = ["www.theguardian.com"]
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(LiberationSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    

    # Méthode pour générer les URLs des pages de pagination
    def start_requests(self):
        base_url = "https://www.theguardian.com/world/morocco?page={}"
        # Générer les URLs pour les pages de 1 à 36
        for page_number in range(1, 37):
            yield Request(url=base_url.format(page_number), callback=self.parse, meta={'page_number': page_number})
            time.sleep(1)  # Attendre 1 seconde entre chaque requête

    def parse(self, response):
        # Utiliser XPath pour extraire tous les titres et liens
        articles = response.xpath('//div[@class="fc-container__inner"]//a[@class="u-faux-block-link__overlay js-headline-text"]')

        # Suivre chaque lien d'article pour extraire le contenu de l'article
        for article in articles:
            article_link = article.xpath('@href').get()
            article_title = article.xpath('text()').get()

            # Extraire la date à partir de l'URL de l'article
            article_date = self.extract_date_from_url(article_link)

            yield response.follow(article_link, callback=self.parse_article, meta={'title': article_title, 'date': article_date})
            time.sleep(1)  # Attendre 1 seconde entre chaque requête

    def parse_article(self, response):
        # Utiliser XPath pour extraire le contenu de l'article
        article_content = response.xpath('//*[@data-gu-name="body"]/div//p//text()').extract()
        article_text = '\n'.join(article_content)

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': response.meta['date'],
            
            
            'content': article_text.strip(),
            'source': self.name
            
        }

    def extract_date_from_url(self, url):
        # Utiliser une expression régulière pour extraire la date de l'URL
        date_match = re.search(r'/(\d{4})/(\w{3})/(\d{1,2})/', url)
        if date_match:
            year = date_match.group(1)
            month = date_match.group(2)
            day = date_match.group(3)
            return f"{day}/{month}/{year}"
        else:
            return None


"""import scrapy
from scrapy import Request
import time

class LiberationSpider(scrapy.Spider):
    name = "theguardian"
    allowed_domains = ["www.theguardian.com"]
    seen_titles = set()

    def start_requests(self):
        base_url = "https://www.theguardian.com/world/morocco?page={}"
        for page_number in range(1, 37):
            yield Request(url=base_url.format(page_number), callback=self.parse, meta={'page_number': page_number})
            time.sleep(1)

    def parse(self, response):
        articles = response.xpath('//div[@class="fc-container__inner"]//a[@class="u-faux-block-link__overlay js-headline-text"]')

        for article in articles:
            article_link = article.xpath('@href').get()
            article_title = article.xpath('text()').get()
            if article_title not in self.seen_titles:
                self.seen_titles.add(article_title)
                yield response.follow(article_link, callback=self.parse_article, meta={'title': article_title})
            else:
                self.logger.info(f"Duplicate article found: {article_title}")

            time.sleep(1)

    def parse_article(self, response):
        article_content = response.xpath('//div[@class="article-body-commercial-selector article-body-viewer-selector  dcr-1g5o3j6"]//p//text()').extract()
        article_text = '\n'.join(article_content)
        article_date = response.xpath('/html/body/main/article/div/div/aside[4]/div/div/div/div[1]/div/details/summary/span/text()').get()

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': article_date,
            'content': article_text.strip()
        }
"""