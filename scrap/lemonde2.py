import scrapy
from datetime import datetime

class JaziraSpider(scrapy.Spider):
    name = "lemonde2"
    start_urls = ["https://www.lemonde.fr/seisme-au-maroc-2023/"]
    
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(JaziraSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None


    def parse(self, response):
        # Extraire les liens et les titres de tous les articles
        articles = response.css('a.teaser__link')

        for article in articles:
            article_title = article.css('h3.teaser__title::text').get().strip()
            article_link = article.css('a::attr(href)').get()
            
            # Créer une requête pour accéder à l'article et extraire son contenu
            yield scrapy.Request(response.urljoin(article_link), callback=self.parse_article, meta={'title': article_title})
        next_page = response.xpath('//section[@class="river__pagination"]/a[contains(@class, "river__pagination--focus")]/following-sibling::a/@href')
        if next_page:
            next_page_url = response.urljoin(next_page.get())
            self.logger.info(f'Next page found: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info('No next page found')
    def parse_article(self, response):
        # Extraire le contenu de l'article
        article_content = response.css('article.article__content p.article__paragraph::text').getall()
        article_content = ' '.join(article_content).strip()

        # Extraire la date de l'article
        #article_date = response.css('section.meta__date-reading span.meta__date::text').get().strip()
        article_date = response.css('section.meta__date-reading span.meta__date::text').get()
        if article_date:
            article_date = article_date.strip()
        else:
            article_date = None  # Ou toute autre valeur par défaut que vous préférez

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': article_date,
            
            
            'content': article_content,
            'source': self.name
        }
























"""import scrapy


class JaziraSpider(scrapy.Spider):
    name = "lemonde2"
    start_urls = ["https://www.lemonde.fr/seisme-au-maroc-2023/"]

    def parse(self, response):
        # Extraire les liens et les titres de tous les articles
        articles = response.css('a.teaser__link')

        for article in articles:
            article_title = article.css('h3.teaser__title::text').get().strip()
            article_link = article.css('a::attr(href)').get()
            
            # Créer une requête pour accéder à l'article et extraire son contenu
            yield scrapy.Request(response.urljoin(article_link), callback=self.parse_article, meta={'title': article_title})
        next_page = response.xpath('//section[@class="river__pagination"]/a[contains(@class, "river__pagination--focus")]/following-sibling::a/@href')
        if next_page:
            next_page_url = response.urljoin(next_page.get())
            self.logger.info(f'Next page found: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info('No next page found')
    def parse_article(self, response):
        # Extraire le contenu de l'article
        article_content = response.css('article.article__content p.article__paragraph::text').getall()
        article_content = ' '.join(article_content).strip()

        # Extraire la date de l'article
        article_date = response.css('section.meta__date-reading span.meta__date::text').get().strip()

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': article_date,
            'content': article_content
        }
"""



















"""import scrapy


class JaziraSpider(scrapy.Spider):
    name = "lemonde2"
    start_urls = ["https://www.lemonde.fr/seisme-au-maroc-2023/"]

    def parse(self, response):
        # Extraire les liens et les titres de tous les articles
        articles = response.css('a.teaser__link')

        for article in articles:
            article_title = article.css('h3.teaser__title::text').get().strip()
            article_link = article.css('a::attr(href)').get()
            
            # Créer une requête pour accéder à l'article et extraire son contenu
            yield scrapy.Request(response.urljoin(article_link), callback=self.parse_article, meta={'title': article_title})
        #next_page = response.xpath('//section[@class="river__pagination"]/a[contains(@class, "river__pagination--focus")]/following-sibling::a/@href')
        #if next_page:
            #next_page_url = response.urljoin(next_page.get())
            #self.logger.info(f'Next page found: {next_page_url}')
            #yield scrapy.Request(url=next_page_url, callback=self.parse)
        #else:
            #self.logger.info('No next page found')
    def parse_article(self, response):
        # Extraire le contenu de l'article
        article_content = response.css('article.article__content p.article__paragraph::text').getall()
        article_content = ' '.join(article_content).strip()

        # Extraire la date de l'article
        article_date = response.css('section.meta__date-reading span.meta__date::text').get().strip()

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': article_date,
            'content': article_content
        }"""


    
    
    
    
""" allowed_domains = ["www.aljazeera.com"]
    start_urls = ["https://www.aljazeera.com/tag/tourism/"]



    def parse(self, response):
        articles = response.xpath('//h3[@class="gc__title"]/a/span/text()').getall()
        
        for titre in articles:
            yield {
                'titre': titre.strip()
            }
       
"""
