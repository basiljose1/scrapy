import scrapy
import json
from scrapy_splash import SplashRequest
from ..items import BuybuybabyItem


class ProductSpider(scrapy.Spider):
    name = "staples"
    start_urls = [
        'https://www.staples.com/chair/directory_chair?autocompletesearchkey=chair',
    ]


    def parse(self, response):

        #follow links to product pages
        for href in response.css('a.product-title::attr(href)'):
            yield response.follow(href, self.parse_product)

        # follow pagination links
        # for href in response.css('a.redirPage::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_product(self, response):

        # and build a new selector from the response "html" key from that object
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'name': extract_with_xpath('//*[@id="mainNgApp"]/div/div[2]/div[1]/div[1]/h1/text()'),
            'price': extract_with_css('.isPrice span.visuallyhidden::text'),
            # 'ratings': extract_with_css('.author-description::text'),
            # 'reviews': extract_with_css('.author-description::text'),
            'product url': response.url,
        }