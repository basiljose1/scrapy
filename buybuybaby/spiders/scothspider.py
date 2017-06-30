import scrapy


class ProductSpider(scrapy.Spider):
    name = "scotch"
    urls = [
        "https://www.amazon.com/All-Clad-7112NSR2-Professional-Stainless-Nonstick/dp/B00005AL48/ref=sr_1_159?s=kitchen&ie=UTF8&qid=1498546150&sr=1-159&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/Sharpie-Permanent-Marker-Brush-Assorted/dp/B00MZ6WNGQ/ref=sr_1_586?s=office-products&ie=UTF8&qid=1498458042&sr=1-586&keywords=Sharpie",
        "https://www.amazon.com/SyPen-Touchscreen-Multi-Function-Capacitive-Flashlight/dp/B01K3U456G/ref=sr_1_1396?s=office-products&ie=UTF8&qid=1496125822&sr=1-1396&refinements=p_n_availability%3A1248831011",
        "https://www.amazon.com/All-Clad-6108SS-Copper-Dishwasher-Cookware/dp/B00005AL1C/ref=sr_1_221?s=kitchen&ie=UTF8&qid=1498460138&sr=1-221&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Copper-Dishwasher-Cookware-10-Inch/dp/B00005AL1D/ref=sr_1_182?s=kitchen&ie=UTF8&qid=1496905048&sr=1-182&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Copper-Dishwasher-Cookware-12-Inch/dp/B00005AL1E/ref=sr_1_161?s=kitchen&ie=UTF8&qid=1491893489&sr=1-161&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Dishwasher-Saucepan-Cookware-1-5-Quart/dp/B00005AL1F/ref=sr_1_158?s=kitchen&ie=UTF8&qid=1497941846&sr=1-158&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Dishwasher-Saucepan-Cookware-2-Quart/dp/B00005AL1G/ref=sr_1_123?s=kitchen&ie=UTF8&qid=1498460224&sr=1-123&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Dishwasher-Saucier-Cookware-2-Quart/dp/B00005AL1J/ref=sr_1_85?s=kitchen&ie=UTF8&qid=1498546242&sr=1-85&refinements=p_n_availability%3A1248816011",
        "https://www.amazon.com/All-Clad-Dishwasher-Saucepan-Cookware-4-Quart/dp/B00005AL1I/ref=sr_1_89?s=kitchen&ie=UTF8&qid=1498546242&sr=1-89&refinements=p_n_availability%3A1248816011",
    ]

    # script = """
    #     function main(splash)
    #         assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
    #         local url = splash.args.url
    #         splash:go(url)
    #         splash:wait(50)
    #         local scroll_to = splash:jsfunc("window.scrollTo")
    #         scroll_to(0, 400)
    #         return {
    #           html = splash:html(),
    #           png = splash:png(),
    #         }
    #     end
    # """

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
            'name': extract_with_xpath('//*[@id="productTitle"]/text()'),
            'names': response.xpath('//*[@id="productTitle"]/text()').extract(),
            'product url': response.url,
        }