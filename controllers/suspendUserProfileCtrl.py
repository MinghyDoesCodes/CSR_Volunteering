from entities.user_account import UserProfile as UP
from database.db_config import get_session

class SuspendUserProfileCtrl:
    def __init__(self):
        self.session = get_session()

    def suspendProfile(self, profileID):

        profile = UP.findById(self.session, profileID)
        if not profile:
            return False # Profile not found
        
        result = profile.suspendProfile(self.session)

        return result # True if suspended, False if already suspended
        
    def activateProfile(self, profileID):
    
        profile = UP.findById(self.session, profileID)
        if not profile:
            return False # Profile not found
        
        result = profile.activateProfile(self.session)

        return result # True if activated, False if already active