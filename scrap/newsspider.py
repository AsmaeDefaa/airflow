import scrapy
from datetime import datetime
class NewsspiderSpider(scrapy.Spider):
    name = "skift"
    allowed_domains = ["skift.com"]
    start_urls = ["https://skift.com/tourism/"]
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(NewsspiderSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    
    

    def parse(self, response):
        articles = response.xpath('//*[@id="archive"]/div/div/div/div/div/a')

        for article in articles:
            titre = article.xpath('.//h3/text()').get()
            lien = article.xpath('./@href').get()

            if titre and 'moroc' in titre.lower():  # Vérifie si le titre contient "maroc"
                date_publication = article.xpath('./p[3]/text()').get()
                if lien and date_publication:
                    yield scrapy.Request(response.urljoin(lien), callback=self.parse_article, meta={'titre': titre, 'date_publication': date_publication})

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        contenu_article = response.xpath('//*[@id="article-wrapper"]/article/section[3]/div[1]/div/div/div[1]/div[3]')
        
        if contenu_article:
            contenu_texte = ''.join(contenu_article.xpath('.//text()').getall())
            titre_article = response.meta.get('titre')
            date_publication = response.meta.get('date_publication')

            yield {
                'titre': titre_article.strip(),
                'url': response.url,
                'date': date_publication.strip(),
                
                'contenu': contenu_texte.strip(),
                'source': self.name
            }
























"""import scrapy

class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["skift.com"]
    start_urls = ["https://skift.com/tourism/"]

    def parse(self, response):
        articles = response.xpath('//*[@id="archive"]/div/div/div/div/div/a')

        for article in articles:
            titre = article.xpath('.//h3/text()').get()
            lien = article.xpath('./@href').get()

            if titre and 'moroc' in titre.lower():  # Vérifie si le titre contient "maroc"
                date_publication = article.xpath('./p[3]/text()').get()
                if lien and date_publication:
                    yield scrapy.Request(response.urljoin(lien), callback=self.parse_article, meta={'titre': titre, 'date_publication': date_publication})

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        contenu_article = response.xpath('//*[@id="article-wrapper"]/article/section[3]/div[1]/div/div/div[1]/div[3]')
        
        if contenu_article:
            contenu_texte = ''.join(contenu_article.xpath('.//text()').getall())
            titre_article = response.meta.get('titre')
            date_publication = response.meta.get('date_publication')

            yield {
                'titre': titre_article.strip(),
                'date_publication': date_publication.strip(),
                'lien': response.url,
                'contenu': contenu_texte.strip()
            }"""




























"""
import scrapy


class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["skift.com"]
    start_urls = ["https://skift.com/tourism/"]

    def parse(self, response):
        # Sélectionnez tous les éléments correspondant aux articles
        articles = response.xpath('//*[@id="archive"]/div/div/div/div/div/a')

        # Parcourez les articles
        for article in articles:
            # Extrayez le titre de l'article
            titre = article.xpath('.//h3/text()').get()
            
            # Extrayez le lien de l'article
            lien = article.xpath('./@href').get()

            # Vérifiez si le titre contient le mot "can"
            if titre and 'morocco' in titre.lower():
                # Extrayez la date de publication
                date_publication = article.xpath('./p[3]/text()').get()

                # Assurez-vous que le titre, le lien et la date de publication ne sont pas vides
                if titre and lien and date_publication:
                    yield scrapy.Request(response.urljoin(lien), callback=self.parse_article, meta={'titre': titre, 'date_publication': date_publication})

        # Suivre le lien de la page suivante si elle existe
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        # Extraire le contenu de l'article en utilisant le xpath fourni
        contenu_article = response.xpath('//*[@id="article-wrapper"]/article/section[3]/div[1]/div/div/div[1]/div[3]')
        
        # Assurez-vous que le contenu de l'article n'est pas vide
        if contenu_article:
            # Joindre le contenu texte
            contenu_texte = ''.join(contenu_article.xpath('.//text()').getall())
            # Récupérer le titre de l'article de la méta-donnée
            titre_article = response.meta.get('titre')
            # Récupérer la date de publication de la méta-donnée
            date_publication = response.meta.get('date_publication')

            yield {
                'titre': titre_article.strip(),  # Retirez les espaces inutiles autour du titre
                 
                'date_publication': date_publication.strip(),  # Retirez les espaces inutiles autour de la date de publication
                'lien': response.url,  # Lien de l'article
                'contenu': contenu_texte.strip()
            }"""
