from entities.user_account import UserProfile as UP
from database.db_config import get_session

class SuspendUserAccountCtrl:
    def __init__(self):
        self.session = get_session()

    def suspendProfile(self, userID):

        user = UP.findById(self.session, userID)
        if not user:
            return False # Profile not found
        
        result = user.suspendUser(self.session)

        return result # True if suspended, False if already suspended
        
    def activateProfile(self, userID):
    
        user = UP.findById(self.session, userID)
        if not user:
            return False # Profile not found
        
        result = user.activate(self.session)

        return result # True if activated, False if already active