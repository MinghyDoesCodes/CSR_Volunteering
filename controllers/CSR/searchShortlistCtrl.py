from entities.shortlist import Shortlist
from database.db_config import get_session

class searchShortlistCtrl:
    def __init__(self):
        self.session = get_session()

    def searchShortlist(self, userID, keyword=None, categoryID= None):
        return Shortlist.searchShortlist(self.session, userID, keyword, categoryID)