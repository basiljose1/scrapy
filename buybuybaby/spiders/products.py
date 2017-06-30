# from datetime import datetime, timedelta, date
# # from amazon_spider.config import clean_text, clean_text_list, clean_string
# import re
# import ast


# def clean_string(string):
#     if string:
#         string = re.sub(r'[^\x00-\x7F]+', '', string)
#         string = re.sub('\s+', ' ', string).strip()

#         return string

#     # return re.sub('\s+', ' ', string).strip() if string else None


# def clean_text(string):
#     formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
#     formatted_data = " ".join(formatted_data).strip()
#     formatted_data = re.sub(r'[^\x00-\x7F]+', '', formatted_data)
#     return formatted_data


# def clean_text_list(string):
#     formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
#     formatted_data = [re.sub(r'[^\x00-\x7F]+', '', str(f).strip()) for f in formatted_data]
#     return str(formatted_data)

# def clean_string(string):
#     if string:
#         string = re.sub(r'[^\x00-\x7F]+', '', string)
#         string = re.sub('\s+', ' ', string).strip()

#         return string

#     # return re.sub('\s+', ' ', string).strip() if string else None


# def clean_text(string):
#     formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
#     formatted_data = " ".join(formatted_data).strip()
#     formatted_data = re.sub(r'[^\x00-\x7F]+', '', formatted_data)
#     return formatted_data


# def clean_text_list(string):
#     formatted_data = [re.sub('\s+', ' ', str(s)).strip() for s in string]
#     formatted_data = [re.sub(r'[^\x00-\x7F]+', '', str(f).strip()) for f in formatted_data]
#     return str(formatted_data)


# class AmazonPdpParser(object):
#     def __init__(self, data, response):
#         self.data = data
#         self.response = response

#     @property
#     def productname(self):
#         productnames = []
#         xpath1 = clean_text(self.response.xpath('.//*[@id="productTitle"]/text()').extract())
#         xpath2 = clean_text(self.response.xpath('.//*[@id="title_feature_div"]/h1/text()').extract())
#         xpath3 = clean_text(self.response.xpath('.//*[@id="ebooksProductTitle"]/text()').extract())
#         productnames.append(xpath1)
#         productnames.append(xpath2)
#         productnames.append(xpath3)
#         return clean_text_list(productnames)

#     @property
#     def producturl(self):
#         product_url = []
#         product_url.append(self.response.url)
#         return clean_text_list(product_url)

#     @property
#     def consumerprice(self):
#         consumerprice_xpath = []
#         xpath1 = clean_string(self.response.xpath('.//*[@id="priceblock_ourprice"]/text()').extract_first())
#         xpath2 = clean_string(self.response.xpath('.//*[@id="actualPriceValue"]/text()').extract_first())
#         xpath3 = clean_string(self.response.xpath('.//*[@id="priceblock_saleprice"]/text()').extract_first())
#         xpath4 = clean_string(self.response.xpath('.//*[@id="a-autoid-1-announce"]/span[2]/span/text()').extract_first())
#         xpath7 = clean_string(self.response.xpath('.//*[@id="color_name_0_price"]/span/text()').extract_first())
#         xpath8 = clean_string(self.response.xpath('.//*[@id="olp_feature_div"]/div/span/a/text()').extract_first())
#         xpath9 = clean_string(self.response.xpath('.//*[@id="_price"]/span/text()').extract_first())
        
#         xpath5 = clean_string(self.response.xpath('.//*[@id="availability"]/span/text()').extract_first())
#         xpath6 = clean_string(self.response.xpath('.//*[@id="outOfStock"]/div/span/text()').extract_first())
#         xpath10 = '//*[@id="pantry-availability"]/text()'

        
#         consumerprice_xpath.append(xpath1)
#         consumerprice_xpath.append(xpath2)
#         consumerprice_xpath.append(xpath3)
#         consumerprice_xpath.append(xpath4)
#         consumerprice_xpath.append(xpath7)
#         consumerprice_xpath.append(xpath8)
#         consumerprice_xpath.append(xpath9)

        
#         consumerprice_xpath.append(xpath5)
#         consumerprice_xpath.append(xpath6)

#         return clean_text_list(consumerprice_xpath)