import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from scrapy import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SearchSpider(scrapy.Spider):
    name = "search"

    start_urls = ['https://www.staples.com/georgia+pacific/directory_georgia+pacific?fids=&pn=0&sr=true&sby=&min=&max=']

    def __init__(self, filename=None):
        # wire us up to selenium
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
    	# close the selenium
        self.driver.close()

    def parse(self, response):
     
        # Load the current page into Selenium
        self.driver.get(response.url)

        element = self.driver.find_element_by_id('load-more-results')

        while True:
        	is_disabled = "disabled" in element.get_attribute("class")
        	# self.log('is_disabled %s' % is_disabled)
        	if not is_disabled:
        		element.click()
        	else:
        		break

        # Sync scrapy and selenium so they agree on the page we're looking at then let scrapy take over
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        
        for href in resp.css('a.product-title::attr(href)'):
        	yield response.follow(href, self.parse_product)

    def parse_product(self, response):

    	self.driver.get(response.url)

    	resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        # pass css query to extract first()
        def extract_with_css(query):
            result = resp.css(query).extract_first()
            if result:
                return result.strip()
            return None

        # pass xpath query to extract first()
        def extract_with_xpath(query):
            result = resp.xpath(query).extract_first()
            if result:
                return result.strip()
            return None

        yield {
            'name': extract_with_xpath('//*[@id="mainNgApp"]/div/div[2]/div[1]/div[1]/h1/text()'),
            'price': extract_with_css('span.stp--price-discounted::text'),
            'ratings': extract_with_xpath('//*[@id="reviewsContainer"]/div/span[1]/span/@title'),
            'reviews': extract_with_css('span.stp--Review::text'),
            'product url': response.url,
        }
        