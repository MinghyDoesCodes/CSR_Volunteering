from entities.user_account import UserAccount as UA
from database.db_config import get_session

class ViewUserAccountCtrl:
    def __init__(self, session=None):
        self.session = session or get_session()

    def viewAccount(self, userID):
        user = UA.findById(self.session, userID)
        if not user:
            return None  # Not found
        return user
