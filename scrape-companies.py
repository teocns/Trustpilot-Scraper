import constants
import requests
from helpers import get_all_categories, retrieve_json_from_category_businesses
# Get categories by lowest hierarchy
import json
from contextlib import nullcontext
from proxy_handler import ProxyHandler


categories_fetch_response = requests.get(
        constants.ENDPOINT,
        params={
            'fetch': 'categories',
            'is_scrape_completed': '0'
        }
    ).text

categories = json.loads(
    categories_fetch_response
)

proxy_handler = ProxyHandler()


def begin(category):
    proxy = proxy_handler.getProxy()
    print (f"Fetching category {category['displayName']} with proxy {proxy.ip}")
    url = f"https://www.trustpilot.com/categories/{category['categoryId']}?numberofreviews=0&status=all&timeperiod=0"
    raw = requests.get(
        url,
        proxies={
            'https':f"https://{proxy.user}:{proxy.password}@{proxy.ip}:{proxy.port}"
        }
    ).text
    
    js = retrieve_json_from_category_businesses(raw)
    
    data = json.loads(js)
    
    
    
    for business in data['props']['pageProps']['businesses']['recentlyReviewedBusinessUnits']['businessUnits']:
        response = requests.post(
            constants.ENDPOINT,
            json={
                'action':'store_business',
                'business':business
            }
        )
        print (response.text)


from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(10)

pool.map(begin,categories)
    
    
    
    
    
    
