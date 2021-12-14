# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urljoin

from scrapy import Spider, Request

from ..static_data import crawlera_api_key, req_meta
from ..utils import get_discount_percentage


class AdidasSaleSpider(Spider):
    name = 'adidas_sale_spider'
    base_url = 'https://www.adidas.com'
    listing_url_t = "https://www.adidas.com/api/plp/content-engine?sitePath=us&query={query}-sale&start={start}"
    product_api_t = "https://www.adidas.com/api/search/product/{product_id}?sitePath=us"
    output_file_name = f'../output/adidas_products_{datetime.now().strftime("%d%b%y")}.csv'

    start_urls = [
        # "https://www.adidas.com/us/men-sale",
        # "https://www.adidas.com/us/women-sale",
        # "https://www.adidas.com/us/kids-sale"
    ]

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    csv_headers = [
        "title", "regular_price", "sale_price", "discount_percentage",
        "category", "main_image_url", "product_url"
    ]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_file_name,
        'FEED_EXPORT_FIELDS': csv_headers,
        # 'CONCURRENT_REQUESTS': 50,
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': crawlera_api_key,

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610,
        },
    }

    headers = {
        'authority': 'www.adidas.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'x-instana-s': '6c64e188572bdfc3',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en;q=0.9',
    }

    def start_requests(self):
        for q in ['men', 'women', 'kids']:
            meta = {"query": q, "start": 0, **req_meta}
            yield Request(self.listing_url_t.format(**meta), headers=self.headers, meta=meta)

    def parse(self, response):
        products = self.get_products(response)

        for p in products['items']:
            item = {}
            item['product_id'] = p['productId']
            item['title'] = p['displayName']
            item['category'] = p['category']
            item['main_image_url'] = p['image']['src'].replace('w_280,h_280', 'w_1024,h_1024')
            item['product_url'] = urljoin(self.base_url, p['link'])

            meta = {'item': item, **item}
            yield Request(self.product_api_t.format(product_id=p['productId']),
                          callback=self.parse_product, headers=self.headers, meta=meta)

        if products['items']:
            response.meta['start'] += 48
            yield Request(self.listing_url_t.format(**response.meta), headers=self.headers, meta=response.meta)

    def parse_product(self, response):
        product = json.loads(response.text)

        item = response.meta['item']
        item['regular_price'] = product['price']
        item['sale_price'] = product['salePrice']
        item['discount_percentage'] = get_discount_percentage(item)
        return item

    def get_products(self, response):
        return json.loads(response.text)['raw']['itemList']
