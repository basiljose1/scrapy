import scrapy
import csv
from scrapy.xlib.pydispatch import dispatcher

def clean_string(string):
    if string:
        string = re.sub(r'[^\x00-\x7F]+', '', string)
        string = re.sub('\s+', ' ', string).strip()

        return string

    # return re.sub('\s+', ' ', string).strip() if string else None


def clean_text(string):
    formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
    formatted_data = " ".join(formatted_data).strip()
    formatted_data = re.sub(r'[^\x00-\x7F]+', '', formatted_data)
    return formatted_data


def clean_text_list(string):
    formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
    formatted_data = [re.sub(r'[^\x00-\x7F]+', '', str(f).strip()) for f in formatted_data]
    return str(formatted_data)


class ProductSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    def __init__(self):
        self.agent_name = 'amazon-pdp-daily'

    def start_requests(self):
        file_name='/home/basil/Projects/buybuybaby/products_exported.csv'
        with open(file_name, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            firstline = True
            for row in spamreader:
                if firstline: #skip first line
                    firstline = False
                    continue
                yield scrapy.Request(url=row[0][1:-1], headers=self.headers, callback=self.parse_product, dont_filter=True)


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

        def productname():
            productname = clean_text_list(response.xpath(".//*[@id='productTitle']/text()").extract_first())
            return productname

            urll = row[0][1:-1]
            if 'https://www.walmart.com' not in urll:
                urll = 'https://www.walmart.com'+urll
        # @property
        # def productprice():
        #     productprices = []
        #     xpath1 = extract_with_xpath('//*[@id="priceblock_ourprice"]/text()')
        #     # xpath2 = extract_with_xpath('//*[@id="olp_feature_div"]/div/span/a/text()')
        #     xpath3 = extract_with_xpath('//*[@id="actualPriceValue"]/text()')
        #     # xpath4 = extract_with_xpath('//*[@id="buybox"]/div/table/tbody/tr[1]/td[2]/text()')
        #     xpath5 = extract_with_xpath('//*[@id="a-autoid-1-announce"]/span[2]/span/text()')
        #     csspath = extract_with_css('span.a-color-price::text')
        #     # csspath1 = extract_with_css('td.a-color-price::text')
        #     xpath6 = '//*[@id="color_name_0_price"]/span/text()'
        #     '//*[@id="color_name_1_price"]/span/text()'




        #     productprices.append(xpath1)
        #     # productprices.append(xpath2)
        #     productprices.append(xpath3)
        #     # productprices.append(xpath4)
        #     productprices.append(xpath5)
        #     productprices.append(csspath)

        #     return next((item for item in productprices if item is not None),None)


        # name = //*[@id="title_feature_div"]/h1/text()
        # name = //*[@id="ebooksProductTitle"]/text()

        yield {
            'name': extract_with_xpath('//*[@id="productTitle"]/text()'),
            # 'price': extract_with_xpath('//*[@id="priceblock_ourprice"]/text()'),
            # 'product url': response.url,
        }