import scrapy


class Sales0919Spider(scrapy.Spider):
    name = 'sales_09_19'
    allowed_domains = ['https://denver.craigslist.org/search/gms?sale_date=2020-09-19']
    start_urls = ['http://https://denver.craigslist.org/search/gms?sale_date=2020-09-19/']

    def parse(self, response):
        pass
