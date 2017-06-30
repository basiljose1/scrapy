import scrapy


class ProductSpider(scrapy.Spider):
    name = "scotchsele"
    urls = [
        "https://www.target.com/p/scotch-174-moving-and-storage-packaging-tape-1-88-x-38-2yds-3pk/-/A-13356376",
        "https://www.target.com/p/scotch-174-masking-tape-70-in-x-54-6-yd/-/A-13356386",
        "https://www.target.com/p/scotch-shipping-packaging-tape-heavy-duty-2-x-38yds-3pk/-/A-13356388",
        "https://www.target.com/p/scotch-153-bubble-mailer-8-5-x-11-6pk/-/A-13356393",
        "https://www.target.com/p/scotch-153-bubble-mailer-9-5-x-13-75-6pk/-/A-13356404",
        "https://www.target.com/p/scotch-174-large-storage-box-18-x-18-x-16-brown/-/A-13356407",
        "https://www.target.com/p/scotch-153-tape-clear-50m/-/A-13356873",
        "https://www.target.com/p/scotch-153-bubble-mailer-6-x-9-6pk/-/A-13356881",
        "https://www.target.com/p/scotch-153-cushion-wrap-clear-16-in-x-15-ft/-/A-13356908",
        "https://www.target.com/p/scotch-174-magic-153-tape-3-4-x-350-3pk/-/A-13356914",
    ]

    script = """
        function main(splash)
            assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
            local url = splash.args.url
            splash:go(url)
            splash:wait(50)
            local scroll_to = splash:jsfunc("window.scrollTo")
            scroll_to(0, 400)
            return {
              html = splash:html(),
              png = splash:png(),
            }
        end
    """

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={
                'splash': {
                    'args': {'lua_source': script,'timeout': 3600},
                    'endpoint': 'execute',
                }
            })

    def parse(self, response):

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
            'name': extract_with_xpath('//*[@id="pdpMainContainer"]/div[2]/h2/span/text()'),
            'names': response.xpath('//*[@id="pdpMainContainer"]/div[2]/h2/span/text()').extract(),
            'product url': response.url,
        }