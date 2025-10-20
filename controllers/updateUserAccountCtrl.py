from entities.user_account import UserAccount as UA
from database.db_config import get_session

class UpdateUserAccountCtrl:
    def __init__(self):
        self.session = get_session()

    def updateAccount(self, userID, email, userName, firstName,
                lastName, phoneNumber, userProfileID):
        
        user = UA.findById(self.session, userID)
        if not user:
            return 0 # User not found
            
        result = user.updateAccount(self.session, email, userName, firstName,
            lastName, phoneNumber, userProfileID)
        
        return result # 1: Email in use, 2: Username in use, 3: Invalid profile, 4: Success