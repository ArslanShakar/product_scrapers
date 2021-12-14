# # -*- coding: utf-8 -*-
# import json
# from copy import deepcopy
# from datetime import datetime
#
# from scrapy import Spider, Request
# from selenium.webdriver import Chrome, ChromeOptions
# from webdriver_manager.chrome import ChromeDriverManager
#
# from ..static_data import crawlera_api_key, req_meta
#
#
# class WalmartDealsSpider(Spider):
#     name = 'walmart_deals_spider'
#     base_url = 'https://www.walmart.com/'
#     deals_url = "https://www.walmart.com/shop/deals"
#     output_file_name = f'../output/walmart_products_{datetime.now().strftime("%d%b%y")}.csv'
#     seen_products = set()
#
#     handle_httpstatus_list = [
#         400, 401, 402, 403, 404, 405, 406, 407, 409,
#         500, 501, 502, 503, 504, 505, 506, 507, 509,
#     ]
#
#     csv_headers = [
#         "title", "regular_price", "sale_price", "discount_percentage", "category",
#         "main_image_url",  "product_url"
#     ]
#
#     custom_settings = {
#         'FEED_FORMAT': 'csv',
#         'FEED_URI': output_file_name,
#         'FEED_EXPORT_FIELDS': csv_headers,
#         # 'CONCURRENT_REQUESTS': 50,
#         'CRAWLERA_ENABLED': True,
#         'CRAWLERA_APIKEY': crawlera_api_key,
#
#         'DOWNLOADER_MIDDLEWARES': {
#             'scrapy_crawlera.CrawleraMiddleware': 610,
#         },
#     }
#
#     meta = {
#         # 'dont_merge_cookies': True,
#         'handle_httpstatus_list': handle_httpstatus_list,
#     }
#
#     headers = {
#         'authority': 'www.walmart.com',
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'service-worker-navigation-preload': 'true',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-user': '?1',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-US,en;q=0.9',
#         'X-Crawlera-Session': 'create',
#         'X-Crawlera-Cookies': 'disable'
#     }
#
#     def start_requests(self):
#         yield Request(self.deals_url, headers=self.headers)
#
#     def parse(self, response):
#         product_selectors = response.css('.mb1.ph1.pa0-xl.bb.b--near-white.w-25')
#         for sel in product_selectors[:]:
#             item = {}
#             item['title'] = self.get_title(sel)
#             item['main_image_url'] = self.get_image_url(sel)
#             item['regular_price'] = self.get_regular_price(sel)
#             item["sale_price"] = self.get_sale_price(sel)
#             item['discount_percentage'] = self.get_discount_percentage(item)
#             item["product_url"] = self.get_product_url(response, sel)
#
#             meta = deepcopy(req_meta)
#             meta['item'] = item
#             yield Request(item["product_url"], callback=self.parse_details, headers=self.headers, meta=meta)
#
#         yield from response.follow_all(css='a[aria-label="Next Page"]', headers=self.headers, meta=req_meta)
#
#     def parse_details(self, response):
#         item = response.meta['item']
#         item['category'] = self.get_categories(response)
#         return item
#
#     def get_title(self, sel):
#         return sel.css('a.absolute.w-100 span::Text').get()
#
#     def get_regular_price(self, sel):
#         return self.clean_price(sel.css('.w_CW:contains("was")::text').get()) or self.get_sale_price(sel)
#
#     def get_sale_price(self, sel):
#         return self.clean_price(sel.css('.w_CW:contains("current price")::text').get())
#
#     def clean_price(self, raw_price):
#         return float(((raw_price or '').split() or ['0'])[-1].replace('$', '').strip())
#
#     def get_image_url(self, sel):
#         return sel.css('img::attr(src)').get()
#
#     def get_product_url(self, response, sel):
#         return response.urljoin(sel.css('a.absolute.w-100::attr(href)').get())
#
#     def get_discount_percentage(self, item):
#         if item['regular_price'] > item['sale_price']:
#             return round(((item['sale_price'] / item['regular_price']) * 100), 2)
#         return 0
#
#     def get_product(self, response):
#         # raw = json.loads(response.css('#__NEXT_DATA__::text').get())
#         raw = json.loads(response.css('[type="application/json"]::text').get())
#         return raw['props']['pageProps']['initialData']['data']['product']
#
#     def get_categories(self, response):
#         return ' > '.join(response.css('[itemprop="name"]::text').getall()[1:-1])
#
#     def get_webdriver(self):
#         options = ChromeOptions()
#         options.add_argument("--disable-extensions")
#         # options.add_argument("--headless")
#         options.add_argument('--disable-gpu')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_experimental_option("useAutomationExtension", False)
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#
#         driver = Chrome(executable_path=ChromeDriverManager().install(), options=options)
#         driver.maximize_window()
#         return driver
