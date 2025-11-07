from entities.request import Request
from database.db_config import get_session

class ViewRequestCtrl:
    def __init__(self, session=None):
        self.session = session or get_session()

    def viewRequest(self, requestID):
        request = Request.findById(self.session, requestID)
        if not request:
            return None  # Not found
        request.increment_view(self.session)
        return request
    
    def listRequests(self):
        return Request.getAllRequests(self.session)