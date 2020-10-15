import asyncio


class TrustPilotReview:
    def __init__(self, rating, comment, user_fullname, user_profile_url,subject_url,user_total_ratings):
        self.comment = comment
        self.user_fullname =  user_fullname
        self.user_profile_url = user_profile_url
        self.subject_url = subject_url
        self.rating = rating
        self.user_total_ratings = user_total_ratings
        

