import scrapy
from scrapy import Request


class Sales0919Spider(scrapy.Spider):
    name = 'sales_09_19'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://denver.craigslist.org/search/gms?sale_date=2020-09-26/']

    def parse(self, response):
        # Scrape all the result-info wrappers
        sales = response.xpath('//p[@class="result-info"]')

        for sale in sales:
            relative_url = sale.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            hood = sale.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            yield Request(absolute_url, callback=self.parse_page,
                          meta={'URL': absolute_url, 'Hood': hood})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        hood = response.meta.get('Hood')
        lat = response.xpath('//div[@id="map"]/@data-latitude').extract_first()
        long = response.xpath('//div[@id="map"]/@data-longitude').extract_first()

        yield {'URL': url, 'Hood': hood, 'Latitude': lat, 'Longitude': long}