from entities.user_profile import UserProfile as UP
from database.db_config import get_session

class ViewUserProfileCtrl:
    def __init__(self):
        self.session = get_session()

    def viewProfile(self, profileID):
        profile = UP.findById(self.session, profileID)
        if not profile:
            return None # Not found
        return profile