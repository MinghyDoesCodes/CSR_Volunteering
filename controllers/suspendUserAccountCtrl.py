from entities.user_account import UserAccount as UA
from database.db_config import get_session

class SuspendUserAccountCtrl:
    def __init__(self):
        self.session = get_session()

    def suspendUser(self, userID):
    
        try:
            user = UA.findById(self.session, userID)
            if not user:
                return (False, f"User account with ID {userID} not found")
            
            success = user.suspendUser(self.session)

            if success:
                return (True, f"User account '{user.username}' suspended successfully")
            else:
                return (False, "Failed to suspend user account")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error suspending user account: {str(e)}")
        
    def activateUser(self, userID):
    
        try:
            user = UA.findById(self.session, userID)
            if not user:
                return (False, f"User account with ID {userID} not found")
            
            success = user.activate(self.session)

            if success:
                return (True, f"User account '{user.username}' activated successfully")
            else:
                return (False, "Failed to activate user account")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error activating user account: {str(e)}")