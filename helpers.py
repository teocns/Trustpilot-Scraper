from urllib.parse import urlencode, quote_plus
import requests
import constants
import json


def getSearchCategoryLink(category,page = 1):
    category = category.lower()
    url_params_array = {
        'query':category,
        'page':page
    }
    url_params_str = urlencode(url_params_array, quote_via=quote_plus)
    return f"https://www.trustpilot.com/search?{url_params_str}"


def get_all_categories(hierarchy = 0):
    return json.loads( 
        requests.get(
            constants.ENDPOINT,
            params={
                "fetch":"categories",
                "hierarchy":hierarchy
            }
        ).text
    )


def post_scraped_review(review):
    return requests.post(
        constants.ENDPOINT,
        data=json.dumps(review.__dict__)
    ).text
    

    
def retrieve_json_from_category_businesses(body):
    first_search = '<script id="__NEXT_DATA__" type="application/json">'
    first_cut_index = body.find(first_search) + len(first_search)
    first_part = body[first_cut_index:len(body)]
    second_search = '</script>'
    second_cut = first_part.find(second_search)
    return first_part[0:second_cut]


def retrieve_json_from_reviews_page(body):
    first_search = '<script type="application/ld+json" data-business-unit-json-ld>'
    first_cut_index = body.find(first_search) + len(first_search)
    first_part = body[first_cut_index:len(body)]
    second_search = '</script>'
    second_cut = first_part.find(second_search)
    return first_part[0:second_cut]