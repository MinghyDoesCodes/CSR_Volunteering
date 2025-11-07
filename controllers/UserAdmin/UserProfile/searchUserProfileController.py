from entities.user_profile import UserProfile as UP
from database.db_config import get_session

class SearchUserProfileController :
    def __init__(self):
        self.session = get_session()

    def searchUserProfile(self, keyword=None, is_active=None):
        profiles = UP.searchUserProfile(self.session, keyword, is_active)
        return profiles
    