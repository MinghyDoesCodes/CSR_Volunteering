from entities.user_account import UserAccount as UA
from database.db_config import get_session

class SuspendUserAccountCtrl:
    def __init__(self):
        self.session = get_session()

    def suspendUser(self, userID):

        user = UA .findById(self.session, userID)
        if not user:
            return 0 # User not found
        
        result = user.suspendUser(self.session)

        return result # 1: Already suspended, 2: Successfully suspended
        
    def activateUser(self, userID):
    
        user = UA .findById(self.session, userID)
        if not user:
            return 0 # User not found
        
        result = user.activate(self.session)

        return result # 1: Already active, 2: Successfully activated