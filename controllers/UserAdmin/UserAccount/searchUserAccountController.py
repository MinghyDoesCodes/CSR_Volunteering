from entities.user_account import UserAccount as UA
from database.db_config import get_session

class SearchUserAccountController:
    def __init__(self):
        self.session = get_session()

    def searchUserAccount(self, keyword, profile_id, is_active):
        users = UA.searchUserAccount(self.session, keyword, profile_id, is_active)
        return users