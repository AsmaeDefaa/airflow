"""import scrapy
from scrapy_splash import SplashRequest
import w3lib.html
class AfricaspiderSpider(scrapy.Spider):
    name = "africaspider"
    allowed_domains = ["northafricapost.com"]
    start_urls = ["https://northafricapost.com/category/headlines/morocco"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Utilisez XPath pour extraire tous les titres de la page actuelle
        titles = response.xpath('//h3[@class="item-title"]/a')
        
        for title in titles:
            title_text = title.xpath('./text()').get().strip()  # Texte du titre
            article_link = title.xpath('./@href').get()  # Lien de l'article
           # if 'touri' in title_text.lower():  # Vérifier si le titre contient "touri" (en ignorant la casse)
                # Extraction de la date
            article_date = title.xpath('../../span[@class="item-meta"]/a/text()').get().strip()  # Date de l'article

                

                # Scraping du contenu de l'article
            yield SplashRequest(article_link, self.parse_article_content, meta={'title': title_text, 'date': article_date})

        # Récupérer le nombre total de pages
        total_pages = self.get_total_pages(response)

        # Générer les URLs de pagination et les envoyer pour le scraping
        for page_number in range(2, total_pages + 1):
            pagination_url = f"https://northafricapost.com/category/headlines/morocco/page/{page_number}"
            yield SplashRequest(pagination_url, self.parse, args={'wait': 2})

    def parse_article_content(self, response):
        title = response.meta['title']
        article_link = response.url
        article_date = response.meta['date']
        paragraphs= ""
    
    # Récupérer tous les paragraphes <p> sous la balise <div class="entry-body">
        paragraphs = w3lib.html.remove_tags(''.join(response.xpath('//div[@class="entry-body"]//p').extract()))
    
    
    
    
        yield {
            'title': title,
            'url': article_link,
            'date': article_date,
            
            'content': paragraphs
        }

    def get_total_pages(self, response):
        # Extraire le nombre total de pages à partir de la pagination
        # Dans cet exemple, nous supposons que le nombre total de pages est 975
        # Vous pouvez remplacer cette logique par la vôtre pour extraire le nombre total de pages
        return 975"""
        
        


import scrapy
from scrapy_splash import SplashRequest
import w3lib.html
from datetime import datetime

class AfricaspiderSpider(scrapy.Spider):
    name = "africa"
    allowed_domains = ["northafricapost.com"]
    start_urls = ["https://northafricapost.com/category/headlines/morocco"]

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(AfricaspiderSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        titles = response.xpath('//h3[@class="item-title"]/a')
        
        for title in titles:
            title_text = title.xpath('./text()').get().strip()
            article_link = title.xpath('./@href').get()
            article_date_text = title.xpath('../../span[@class="item-meta"]/a/text()').get().strip()
            article_date = datetime.strptime(article_date_text, '%B %d, %Y')
            
            # Filtrer par date
            if self.start_date and self.end_date:
                if not (self.start_date <= article_date <= self.end_date):
                    continue
            
            yield SplashRequest(article_link, self.parse_article_content, meta={'title': title_text, 'date': article_date_text})

        total_pages = self.get_total_pages(response)
        
        for page_number in range(2, total_pages + 1):
            pagination_url = f"https://northafricapost.com/category/headlines/morocco/page/{page_number}"
            yield SplashRequest(pagination_url, self.parse, args={'wait': 2})

    def parse_article_content(self, response):
        title = response.meta['title']
        article_link = response.url
        article_date = response.meta['date']
        paragraphs = w3lib.html.remove_tags(''.join(response.xpath('//div[@class="entry-body"]//p').extract()))
    
        yield {
            'title': title,
            'url': article_link,
            'date': article_date,
            'content': paragraphs,
            'source': self.name,
        }

    def get_total_pages(self, response):
        return 975  # Ajustez cette logique pour extraire le nombre total de pages de manière dynamique
        







"""import scrapy  #hada khdam 
from scrapy_splash import SplashRequest

class AfricaspiderSpider(scrapy.Spider):
    name = "africaspider"
    allowed_domains = ["northafricapost.com"]
    start_urls = ["https://northafricapost.com/category/headlines/morocco"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Utilisez XPath pour extraire tous les titres de la page actuelle
        titles = response.xpath('//h3[@class="item-title"]/a')
        
        for title in titles:
            title_text = title.xpath('./text()').get().strip()  # Texte du titre
            article_link = title.xpath('./@href').get()  # Lien de l'article
           # if 'touri' in title_text.lower():  # Vérifier si le titre contient "touri" (en ignorant la casse)
                # Extraction de la date
            article_date = title.xpath('../../span[@class="item-meta"]/a/text()').get().strip()  # Date de l'article

                

                # Scraping du contenu de l'article
            yield SplashRequest(article_link, self.parse_article_content, meta={'title': title_text, 'date': article_date})

        # Récupérer le nombre total de pages
        total_pages = self.get_total_pages(response)

        # Générer les URLs de pagination et les envoyer pour le scraping
        for page_number in range(2, total_pages + 1):
            pagination_url = f"https://northafricapost.com/category/headlines/morocco/page/{page_number}"
            yield SplashRequest(pagination_url, self.parse, args={'wait': 2})

    def parse_article_content(self, response):
        title = response.meta['title']
        article_link = response.url
        article_date = response.meta['date']
    
    # Récupérer tous les paragraphes <p> sous la balise <div class="entry-body">
        paragraphs = response.xpath('//div[@class="entry-body"]//p')
    
    # Initialiser une liste pour stocker le texte de chaque paragraphe
        article_content = []
    
    # Parcourir chaque paragraphe et extraire son texte
        for paragraph in paragraphs:
            paragraph_text = paragraph.xpath('./text()').get()
            if paragraph_text:
                article_content.append(paragraph_text.strip())
    
    # Concaténer tous les textes des paragraphes en une seule chaîne de caractères
        article_content = "\n".join(article_content).strip() if article_content else None
    
        yield {
            'title': title,
            'link': article_link,
            'date': article_date,
            'content': article_content
        }

    def get_total_pages(self, response):
        # Extraire le nombre total de pages à partir de la pagination
        # Dans cet exemple, nous supposons que le nombre total de pages est 975
        # Vous pouvez remplacer cette logique par la vôtre pour extraire le nombre total de pages
        return 975"""






"""import scrapy
from scrapy_splash import SplashRequest

class AfricaspiderSpider(scrapy.Spider):
    name = "africaspider"
    allowed_domains = ["northafricapost.com"]
    start_urls = ["https://northafricapost.com/category/headlines/morocco"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Utilisez XPath pour extraire tous les titres de la page actuelle
        titles = response.xpath('//h3[@class="item-title"]/a')
        
        for title in titles:
            title_text = title.xpath('./text()').get().strip()  # Texte du titre
            article_link = title.xpath('./@href').get()  # Lien de l'article
           # if 'touri' in title_text.lower():  # Vérifier si le titre contient "touri" (en ignorant la casse)
                # Extraction de la date
            article_date = title.xpath('../../span[@class="item-meta"]/a/text()').get().strip()  # Date de l'article

                

                # Scraping du contenu de l'article
            yield SplashRequest(article_link, self.parse_article_content, meta={'title': title_text, 'date': article_date})

        # Récupérer le nombre total de pages
        total_pages = self.get_total_pages(response)

        # Générer les URLs de pagination et les envoyer pour le scraping
        for page_number in range(2, total_pages + 1):
            pagination_url = f"https://northafricapost.com/category/headlines/morocco/page/{page_number}"
            yield SplashRequest(pagination_url, self.parse, args={'wait': 2})

    def parse_article_content(self, response):
        title = response.meta['title']
        article_link = response.url
        article_content = response.xpath('//div[@class="entry-body"]/p/text()').get()
        article_date = response.meta['date']
        
        yield {
            'title': title,
            'link': article_link,
            'date': article_date,
            'content': article_content.strip() if article_content else None
        }

    def get_total_pages(self, response):
        # Extraire le nombre total de pages à partir de la pagination
        # Dans cet exemple, nous supposons que le nombre total de pages est 975
        # Vous pouvez remplacer cette logique par la vôtre pour extraire le nombre total de pages
        return 975"""
