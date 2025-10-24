from entities.request import Request
from database.db_config import get_session

class SearchRequestCtrl:
    def __init__(self):
        self.session = get_session()

    def searchRequests(self, keyword, status):
        request = Request.searchRequests(self.session, keyword, status)
        return request # Return the list of matching requests