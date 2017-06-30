# import scrapy
# import re
# import time
# import csv
# import uuid
# from datetime import datetime, timedelta, date
# from amazon_spider.items import PdpVariables
# from amazon_spider.config import db_connection
# from psycopg2.extensions import AsIs
# from scrapy.selector import HtmlXPathSelector
# #from  amazon_spider.settings import headers
# from amazon_exception_products import AmazonPdpParser
# from bs4 import BeautifulSoup
# from amazon_spider.settings import CURRENT_DATE
# from models.logs import ScrapyMonitoringLog
# import sys
# csv.field_size_limit(sys.maxsize)
# from amazon_spider.config import clean_text, clean_text_list, clean_string, upload_csv_s3
# from config import settings
# from models.db import create_session
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# import boto3
# from models.agents import ScrapySpiderDetails
# from models.logs import AmazonProcessLog

# BUCKET_NAME = settings.get('BUCKET_NAME')
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(BUCKET_NAME)

# file_path = settings.get('DOWNLOAD_FILE_PATH')
# log_file_path = settings.get('LOG_FILE_PATH')

# import os

# captcha_count = 0


# class AmazonPdpSpider(scrapy.Spider):
#     name = "amazon-pdp-daily-All-items"
#     allowed_domains = ["amazon.com"]

#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.8",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
#     }

#     def __init__(self):
#         self.agent_name = 'amazon-pdp-daily'
#         self.details = ScrapySpiderDetails.get_process(self.session, self.agent_name)
#         dispatcher.connect(self.spider_closed, signals.spider_closed)

#     def start_requests(self):
#         values = {}
#         values['id'] = str(uuid.uuid4())
#         values['day'] = CURRENT_DATE
#         values['agent_id'] = self.details.agent_id
#         values['agent_name'] = self.agent_name
#         values['status'] = 'Running'
#         values['start_time'] = datetime.now()
#         ScrapyMonitoringLog.insert_row(self.session, values)

#         self.update_process_log({
#             "scrapy_pdp_spider_status": 'Running',
#             "scrapy_pdp_spider_starttime": datetime.now()
#         })

#         self.session.commit()

#         url_count = 0

#         pdp_key = 'amazon_pdp_collection_%s.csv' % CURRENT_DATE

#         pdp_file = list(bucket.objects.filter(Prefix=pdp_key))

#         if len(pdp_file) > 0:
#             key = pdp_file[0].key
#             file_name = '%s/%s' % (file_path, key)
#             if not os.path.exists(file_name):
#                 s3.meta.client.download_file(BUCKET_NAME, key, file_name)

#         with open(file_name, 'rb') as csvfile:
#             spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#             for row in spamreader:
#                 url_count += 1
#                 filepath = '%surl_count_pdp_%s.txt' % (log_file_path,CURRENT_DATE)
#                 with open(filepath, 'w') as u:
#                     u.write("url count is %s \n" % url_count)
#                 yield scrapy.Request(url=row[0], headers=self.headers, callback=self.parse, dont_filter=True)

#     def parse(self, response):
#         global captcha_count
#         try:
#             content = response.xpath('//*[@id="a-page"]')
#             kill_page = response.xpath('//*[@id="g"]')
#             date_time = [datetime.now()]
#             if content:
#                 data = AmazonPdpParser(content, response)
#                 item = PdpVariables(
#                     productname=data.productname,
#                     producturl=str(data.producturl),
#                     consumerprice=data.consumerprice,
#                 )
#                 yield item

#             elif kill_page:
#                 item = PdpVariables(
#                     producturl=response.url,
#                     kill=datetime.now().date(),
#                 )
#                 yield item
#             else:
#                 captcha = response.xpath('//*[@id="captchacharacters"]/@id').extract()
#                 if captcha:
#                     captcha_count += 1
#                     filepath = '%scaptcha_url_pdp_%s.txt' % (log_file_path,CURRENT_DATE)
#                     with open(filepath, 'a') as c:
#                         c.write("Captcha url is %s \n" % response.url)
#                     if captcha_count > 5:
#                         filepath = '%scaptcha_url_retry_pdp_%s.txt' % (log_file_path,CURRENT_DATE)
#                         with open(filepath, 'a') as cc:
#                             cc.write("Captcha url is %s \n" % response.url)
#                         captcha_count = 0
#                         sys.exit(0)
#                     yield scrapy.Request(response.url, callback=self.parse)

#         except Exception as e:
#             filepath = '%sexception_pdp_%s.txt' % (log_file_path,CURRENT_DATE)
#             with open(filepath, 'a') as p:
#                 p.write("pdp_exception url is %s \n" % response.url)
#                 p.write("exception is %s \n" % e.message)

#     def update_process_log(self, values):
#         table = eval('AmazonProcessLog')
#         process = table.get_for_date(self.session, datetime.now().date())
#         table.update_row(self.session, process.process_id.strip(), values)
#         self.session.commit()

#     def spider_closed(self, spider):
#         #filepath = '/home/sudheesh/projects3/amazon_spider/amazon-pdp-daily-All-items-%s.CSV' % CURRENT_DATE
#         filepath = '%s/amazon-pdp-daily-All-items-%s.CSV' % (file_path, CURRENT_DATE)

#         upload_csv_s3(name="amazon-pdp-daily-All-items-%s.CSV" % CURRENT_DATE,
#                       file_name=filepath)

#         self.update_process_log({
#             "scrapy_pdp_spider_status": 'Done',
#             "scrapy_pdp_spider_endtime": datetime.now()
#         })
#         self.session.commit()
#         update_values = {}
#         check_status = ScrapyMonitoringLog.get_process_for_agent_id(self.session, CURRENT_DATE, self.details.agent_id,
#                                                                     'Amazon')
#         if check_status:
#             update_values['status'] = 'Done'
#             update_values['end_time'] = datetime.now()
#             ScrapyMonitoringLog.update_row(self.session, CURRENT_DATE,
#                                            self.details.agent_id, update_values)
#             self.session.commit()

#     @property
#     def session(self):
#         session = getattr(self, '_session', None)
#         if session is None:
#             # logger.info('[Monitoring] Creating DB session')
#             session = create_session()
#             self._session = session
#         return session
