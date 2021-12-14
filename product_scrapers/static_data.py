
"""
Scraping-Hub Login:
username: patrolmantim@gmail.com
password: YnYYJKTP@M5gCw7
"""

from datetime import datetime

crawlera_api_key = "638eb0d636b74dc49a18f67c89a3d908"
s3_path_taxi_scrape = "s3://impairscrapinghub/taxi/new_scrape/"

today_date = datetime.now().strftime('%d%b%y')

handle_httpstatus_list = [
    400, 401, 402, 403, 404, 405, 406, 407, 409,
    500, 501, 502, 503, 504, 505, 506, 507, 509,
]

req_meta = {
    'handle_httpstatus_list': handle_httpstatus_list,
}
