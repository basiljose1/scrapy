import scrapy
import json
from scrapy_splash import SplashRequest


class ProductSpider(scrapy.Spider):
    name = "productsrisk"
    start_urls = [
        'https://www.buybuybaby.com/store/category/strollers/strollers/32572/',
    ]

    def parse(self, response):

        script = """
        function main(splash)
            assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
            local url = splash.args.url
            splash:go(url)
            splash:wait(50)
            splash:runjs('document.getElementById("closeButton").click()')
            splash:wait(10)
            splash:runjs('document.getElementById("prodViewDefault-tab2").click()')
            splash:wait(20)
            local scroll_to = splash:jsfunc("window.scrollTo")
            scroll_to(0, 400)
            return {
              html = splash:html(),
              png = splash:png(),
            }
        end
        """
        #follow links to product pages
        for href in response.css('a.prodImg::attr(href)').extract():
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, self.parse_product, meta={
                'splash': {
                    'args': {'lua_source': script,'timeout': 3600},
                    'endpoint': 'execute',
                }
            })

        # follow pagination links
        for href in response.css('a.redirPage::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_product(self, response):
        # self.log('res %s' % response)

        print 'res',response.body

        # fetch base URL because response url is the Splash endpoint
        # baseurl = response.meta["_splash_processed"]["args"]["url"]

        # decode JSON response
        # splash_json = json.loads(response.body_as_unicode())

        # and build a new selector from the response "html" key from that object
        # selector = scrapy.Selector(text=response["html"], type="html")
        # def extract_with_css(query):
        #     return response.css(query).extract_first().strip()
        # def extract_with_xpath(query):
        #     return response.xpath(query).extract_first().strip()

        # yield {
        #     'name': extract_with_xpath('//*[@id="productTitle"]/text()'),
        #     'price': extract_with_css('.isPrice span.visuallyhidden::text'),
        #     # 'ratings': extract_with_css('.author-description::text'),
        #     # 'reviews': extract_with_css('.author-description::text'),
        #     'producturl': response.url,
        # }