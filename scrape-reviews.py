import constants
import requests
from helpers import get_all_categories, retrieve_json_from_category_businesses, retrieve_json_from_reviews_page
# Get categories by lowest hierarchy
import json
from contextlib import nullcontext
from proxy_handler import ProxyHandler


businessses_response = requests.get(
        constants.ENDPOINT,
        params={
            'fetch': 'businesses',
        }
    ).text


categories = json.loads(
    businessses_response
)

proxy_handler = ProxyHandler()


def begin(business):
    proxy = proxy_handler.getProxy()
    print (f"Fetching reviews for {business['displayName']} with proxy {proxy.ip}")
    
    
    # There are 20 reviews per page. So we take the amount of total reviews and we divide on 20
    
    total_pages = (business['numberOfReviews'] / 20) + 1 # Always +1
    
    
    for current_page in range(1,total_pages+1):
        # Retrieve the page
        url = f"https://www.trustpilot.com/review/{business['identifyingName']}?languages=en"
        exit(url)
        raw = requests.get(
            url,
            proxies={
                'https':f"https://{proxy.user}:{proxy.password}@{proxy.ip}:{proxy.port}"
            }
        ).text
        exit(raw)
        data = json.loads(
            retrieve_json_from_reviews_page(raw)
        )
    
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
pool = ThreadPool(1)

pool.map(begin,categories)
    
    
    
    
    
    
