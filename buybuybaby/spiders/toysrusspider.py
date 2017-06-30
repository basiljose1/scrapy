import scrapy
import csv
import urlparse
from ..items import BabiesrusItem
from scrapy.loader import ItemLoader

class BabiesSpider(scrapy.Spider):
    name = "toysrus-exception"
    allowed_domains = ["toysrus.com"]

    headers = {
                'Host': 'www.toysrus.com',
                'Connection': 'close',
                'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
                'Accept-Encoding': 'gzip',
                'Accept-Charset': 'ISO-8859-1,UTF-8;q=0.7,*;q=0.7',
                'Cache-Control': 'no-cache',
                'Accept-Language': 'de,en;q=0.7,en-us;q=0.3',
         }

    def start_requests(self):
        with open('/home/basil/Babiesrus_urls.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            firstline = True
            for row in spamreader:
                if firstline: #skip first line
                    firstline = False
                    continue
                urll = row[0][1:-1]
                yield scrapy.Request(url=urll, headers=None, callback=self.parse, dont_filter=True)

    def parse(self, response):
        
        # follow pagination links
        if response.xpath("//a[@class='results']/span[@class='next']").extract_first():
            next = response.xpath("//a[@class='results']/@href").extract()[-1]
            full_url = urlparse.urljoin(response.url, next)  
            yield scrapy.Request(url=full_url, headers=self.headers, callback= self.parse, dont_filter=True)

        l = ItemLoader(item=BabiesrusItem(), response=response)
        l.add_xpath('name', "//a[contains(@class, 'prodtitle')]/text()")
        l.add_xpath('price', "//span[contains(@class, 'ourPrice2')]/text()")
        l.add_xpath('ratings', "//span[contains(@class, 'pr-rounded')]/text()")
        l.add_xpath('producturl', "//a[contains(@class, 'prodtitle')]/@href") 
        l.add_value('pageurl', response.url) 
        
        names = l.get_output_value('name')
        prices = l.get_output_value('price')
        ratingss = l.get_output_value('ratings')
        producturls = l.get_output_value('producturl')
        pageurl = response.url

        for i in range(len(names)):
            yield {
                'name':names[i],
                'price':prices[i],
                'ratings':ratingss[i],
                'producturl':producturls[i],
                'pageurl':pageurl
                }


        # yield l.load_item()

