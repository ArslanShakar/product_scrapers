import re
import time


def clean(text):
    if text and isinstance(text, str):
        for c in ['\r\n', '\n\r', u'\n', u'\r', u'\t', u'\xa0']:
            text = text.replace(c, ' ')
        return re.sub(' +', ' ', text).strip()

    return text


def get_discount_percentage(item):
    if item['regular_price'] > item['sale_price']:
        return round(((item['regular_price'] - item['sale_price']) / item['regular_price'] * 100), 2)
    return 0


def update_discount_percentage(item):
    item['discount_percentage'] = 0

    if item['regular_price'] > item['sale_price']:
        item['discount_percentage'] = round(((item['regular_price'] - item['sale_price']) / item['regular_price'] * 100), 2)


def retry_invalid_response(callback):
    def wrapper(spider, response):
        if response.status >= 400:
            if response.status == 404:
                spider.logger.info('Page not found.')
                return

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(3)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            spider.logger.info("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)
            return

        return callback(spider, response)

    return wrapper
