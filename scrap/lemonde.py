"""import scrapy
from datetime import datetime

class NytimesSpider(scrapy.Spider):
    name = "lemonde"
    
    start_urls = ["https://www.lemonde.fr/en/morocco/"]
    
    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(NytimesSpider, self).__init__(*args, **kwargs)
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
            article_date = None

        yield {
            'title': response.meta['title'],
            'url': response.url,
            'date': article_date,
            
            
            'content': article_content,
            
        }"""
        
        
        
import scrapy
from datetime import datetime

class LeMondeSpider(scrapy.Spider):
    name = 'lemonde'
    start_urls = ["https://www.lemonde.fr/en/morocco/"]

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(LeMondeSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    def parse(self, response):
        articles = response.css('a.teaser__link')
        for article in articles:
            article_title = article.css('h3.teaser__title::text').get().strip()
            article_link = article.css('a::attr(href)').get()
            yield scrapy.Request(response.urljoin(article_link), callback=self.parse_article, meta={'title': article_title})
        
        next_page = response.xpath('//section[@class="river__pagination"]/a[contains(@class, "river__pagination--focus")]/following-sibling::a/@href')
        if next_page:
            next_page_url = response.urljoin(next_page.get())
            self.logger.info(f'Next page found: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info('No next page found')

    def parse_article(self, response):
        article_content = response.css('article.article__content p.article__paragraph::text').getall()
        article_content = ' '.join(article_content).strip()

        article_date_str = response.css('section.meta__date-reading span.meta__date::text').get()
        if article_date_str:
            article_date = self.parse_date(article_date_str)
            if self.start_date <= article_date <= self.end_date:
                yield {
                    'title': response.meta['title'],
                    'url': response.url,
                    'date': article_date.strftime('%Y-%m-%d'),
                    'content': article_content,
                    'source': self.name,
                }
            else:
                self.logger.info(f"Article '{response.meta['title']}' is out of the date range: {article_date_str}")
        else:
            self.logger.info(f"No date found for article '{response.meta['title']}'")

    def parse_date(self, date_str):
        try:
            date_str = date_str.split("Published on ")[-1].split(", at")[0].strip()
            return datetime.strptime(date_str, '%B %d, %Y')
        except ValueError as e:
            self.logger.error(f"Error parsing date: {date_str} - {e}")
            return None

        




"""

import scrapy
from datetime import datetime, timedelta

class MySpider(scrapy.Spider):
    name = 'lemonde'
    
    def start_requests(self):
        # Définir la date de début comme le 1er janvier 2000
        start_date = datetime(2024, 1, 1)
        # Définir la date de fin comme aujourd'hui
        end_date = datetime.now()
        
        # Générer les URL pour chaque jour entre la date de début et la date de fin
        current_date = start_date
        while current_date <= end_date:
            # Construire l'URL avec le format de date requis
            url = f'https://www.lemonde.fr/archives-du-monde/{current_date.strftime("%d-%m-%Y")}/'
            self.logger.info(f'Scraping URL: {url}')
            # Faire une demande pour cette URL
            yield scrapy.Request(url=url, callback=self.parse)
            # Passer à la prochaine date
            current_date += timedelta(days=1)
    
    def parse(self, response):
        self.logger.info(f'Parsing page: {response.url}')
        # Sélectionnez tous les éléments correspondant à l'XPath des titres des articles
        titres_elements = response.xpath('//*[@id="river"]/section/a/h3')
        
        # Parcourez les éléments et extrayez les titres
        for titre_element in titres_elements:
            # Utilisez .//text() pour extraire le texte des éléments enfants
            titre = titre_element.xpath('.//text()').get()
            
            # Assurez-vous que le titre n'est pas vide
            if titre:
                yield {
                    'titre': titre.strip()  # Retirez les espaces inutiles autour du titre
                }
        
        # Pagination
        next_page = response.xpath('//section[@class="river__pagination"]/a[contains(@class, "river__pagination--focus")]/following-sibling::a/@href')
        if next_page:
            next_page_url = response.urljoin(next_page.get())
            self.logger.info(f'Next page found: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info('No next page found')



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss


    def parse(self, response):
        # Récupérer les liens des années
        years_links = response.css('.page__button-sitemap.button.button--year::attr(href)').getall()
        for year_link in years_links:
            yield scrapy.Request(response.urljoin(year_link), callback=self.parse_year)

    def parse_year(self, response):
        # Récupérer les liens des mois
        months_links = response.css('.page__button-sitemap.button.button--month::attr(href)').getall()
        for month_link in months_links:
            yield scrapy.Request(response.urljoin(month_link), callback=self.parse_month)

    def parse_month(self, response):
        # Récupérer les liens des jours
        days_links = response.css('.page__button-sitemap.button.button--day::attr(href)').getall()
        for day_link in days_links:
            yield scrapy.Request(response.urljoin(day_link), callback=self.parse_day)

    def parse_day(self, response):
        # Sélectionnez tous les éléments correspondant à l'XPath des titres des articles
        titres_elements = response.css('.page__title')
        
        # Parcourez les éléments et extrayez les titres
        for titre_element in titres_elements:
            # Utilisez .extract_first() pour extraire le texte des éléments
            titre = titre_element.css('::text').extract_first()
            
            # Assurez-vous que le titre n'est pas vide
            if titre:
                yield {
                    'titre': titre.strip()  # Retirez les espaces inutiles autour du titre
                }
"""


































"""
import scrapy
from scrapy_splash import SplashRequest

class AfricaspiderSpider(scrapy.Spider):
    name = "lemonde"
    allowed_domains = ["northafricapost.com"]
    start_urls = ["https://northafricapost.com/category/headlines/morocco"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Utilisez XPath pour extraire tous les titres de la page actuelle
        titles = response.xpath('//h3[@class="item-title"]/a')

        for title in titles:
            title_text = title.xpath('.//text()').get().strip()
            title_url = title.xpath('./@href').get()
            if 'touri' in title_text.lower():
                article_date = title.xpath('../../span[@class="item-meta"]/a/text()').get().strip()  # Date de l'article
                
                # Envoyer une requête pour l'URL du lien et extraire son contenu
                yield SplashRequest(title_url, self.parse_article_content,
                                    meta={'title': title_text, 'url': title_url,'date': article_date},
                                    args={'wait': 2})

        # Récupérer le nombre total de pages
        total_pages = self.get_total_pages(response)

        # Générer les URLs de pagination et les envoyer pour le scraping
        for page_number in range(2, total_pages + 1):
            pagination_url = f"https://northafricapost.com/category/headlines/morocco/page/{page_number}"
            yield SplashRequest(pagination_url, self.parse, args={'wait': 2})

    def get_total_pages(self, response):
        # Extraire le nombre total de pages à partir de la pagination
        # Dans cet exemple, nous supposons que le nombre total de pages est 975
        # Vous pouvez remplacer cette logique par la vôtre pour extraire le nombre total de pages
        return 975

    def parse_article_content(self, response):
        # Utilisez XPath pour extraire le contenu de l'article
        article_content = response.xpath('//div[@class="entry-body"]//p/text()').getall()
        
        # Concaténer le contenu de l'article en un seul texte
        article_text = ' '.join(article_content).strip()
        
        # Utilisez XPath pour extraire la date de l'article
        article_date = response.meta['date']
        yield {
            'title': response.meta['title'],
            'url': response.meta['url'],
            'content': article_text,
            'date': article_date
            
        }"""
