import scrapy


class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.buybuybaby.com/store/category/strollers/strollers/32572/',
    ]

    def parse(self, response):
        #follow links to product pages
        for href in response.css('a.prodImg::attr(href)'):
            yield response.follow(href, self.parse_product)

        # follow pagination links
        for href in response.css('a.pageNumber::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_product(self, response):

        def extract_with_css(query):
            resp = response.css(query).extract_first()
            if resp:
                return resp.strip()
            return None
        def extract_with_xpath(query):
            resp = response.xpath(query).extract_first()
            if resp:
                return resp.strip()
            return None

        yield {
            'name': extract_with_xpath('//*[@id="productTitle"]/text()'),
            'price': extract_with_css('.isPrice span.visuallyhidden::text'),
            'ratings': extract_with_xpath('//*[@id="prodSummaryContainer"]/span/span/text()'),
            'reviews': extract_with_css('span.bvTotalReviewCountClass::text'),
            'product url': response.url,
        }