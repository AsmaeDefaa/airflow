import scrapy
from datetime import datetime

class AtalyarspiderSpider(scrapy.Spider):
    name = "atalyar"
    allowed_domains = ["www.atalayar.com"]
    start_urls = ["https://www.atalayar.com/en/tags/marruecos/"]
    
    
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(AtalyarspiderSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    def parse(self, response):
        # Extract data from current page
        articles = response.xpath('//article')
        for article in articles:
            relative_link = article.xpath('.//h2/a/@href').get()
            full_link = response.urljoin(relative_link)
            title = article.xpath('.//h2/a/text()').get()

            # Request to scrape the article title, link, and content
            yield scrapy.Request(url=full_link, callback=self.parse_article, meta={'title': title, 'link': full_link})

        # Check for next page
        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_article(self, response):
        # Extract title, content, and date from the article page
        title = response.meta['title']
        content = response.xpath('//div[@class="content-body inner-article-data"]//p//text()').getall()
        content = ' '.join(content).strip()
        link = response.meta['link']
        
        # Try different XPath selectors for the date
        date_xpath = [
            '//span[@class="content-meta-date content-meta-date-updated"]/text()',  # XPath 1
            '//span[@class="content-meta-date content-meta-date-created"]/text()'  # XPath 2
        ]

        date = None
        for xpath in date_xpath:
            date = response.xpath(xpath).get()
            if date:
                break

        yield {
            'title': title,
            'url': link,
            'date': date,
            'content': content,
            'source': self.name,
            
            
        }











"""import scrapy


class AtalyarspiderSpider(scrapy.Spider):
    name = "atalyarspider"
    allowed_domains = ["www.atalayar.com"]
    start_urls = ["https://www.atalayar.com/fr/tags/marruecos/"]

    def parse(self, response):
        # Extract data from current page
        articles = response.xpath('//article')
        for article in articles:
            relative_link = article.xpath('.//h2/a/@href').get()
            full_link = response.urljoin(relative_link)
            title = article.xpath('.//h2/a/text()').get()

            # Request to scrape the article title, link, and content
            yield scrapy.Request(url=full_link, callback=self.parse_article, meta={'title': title, 'link': full_link})

        # Check for next page
        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_article(self, response):
        # Extract title, content, and date from the article page
        title = response.meta['title']
        content = response.xpath('//div[@class="content-body inner-article-data"]//p//text()').getall()
        content = ' '.join(content).strip()
        link = response.meta['link']
        
        # Extracting date
        date = response.xpath('//div[@class="content-header-data"]//span[@class="content-meta-date content-meta-date-updated"]//text()').get()

        yield {
            'title': title,
            'date': date,
            'content': content,
            'link': link,
            
        }"""









"""import scrapy


class AtalyarspiderSpider(scrapy.Spider):
    name = "atalyarspider"
    allowed_domains = ["www.atalayar.com"]
    #start_urls = ["https://www.atalayar.com/fr/tags/tourisme/"]
    start_urls = ["https://www.atalayar.com/fr/tags/marruecos/"]

    def parse(self, response):
        # Extraction des titres et des liens de la page actuelle
        articles = response.xpath('//div[contains(@class, "item")]')
        for article in articles:
            titre = article.xpath('.//h2/a/text()').get()
            lien = article.xpath('.//h2/a/@href').get()
            if titre and lien: #and any(keyword in titre.lower() for keyword in ["maroc", "marocaine", "essaouira"]):
                article_url = response.urljoin(lien.strip())
                yield scrapy.Request(url=article_url, callback=self.parse_article, meta={'titre': titre})

        # Extraction des liens des autres pages de pagination
        next_pages = response.xpath('//ul[@class="pagination"]/li[@class="next"]/a/@href').get()
        if next_pages:
            next_page_url = response.urljoin(next_pages)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_article(self, response):
        # Extraction du contenu de l'article
        contenu = response.xpath('//div[@class="content-body inner-article-data"]//p//text()').getall()
        contenu = " ".join(contenu).strip()
        
        # Extraction de l'auteur de l'article
        auteur = response.xpath('//span[@class="author-name agency"]/a/text()').get()

        # Extraction de la date de l'article
        date_raw = response.xpath('//span[@class="content-meta-date content-meta-date-created mr-2"]/text()').get()
        date = date_raw.split('-')[0].strip() if date_raw else None
        
        # Extraction du titre de l'article
        titre = response.meta['titre']

        yield {
            
            'titre': titre,
            'contenu': contenu,
            'date': date,
            #'auteur': auteur.strip() if auteur else None,
            'url': response.url
            
        }"""
