import requests
from review import TrustPilotReview
from helpers import getSearchCategoryLink, post_scraped_review, get_all_categories




#response = requests.get(getSearchCategoryLink('smm panel'))




#print (response.text)









print (
    post_scraped_review(
        TrustPilotReview(5,'this was really good man','alex kimchey','https://someurl.com','https://someotherurl.com',51)
    )

)


