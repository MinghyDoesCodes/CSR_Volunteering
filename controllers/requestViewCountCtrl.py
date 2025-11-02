from entities.request import Request
from database.db_config import get_session

class RequestViewCountCtrl:
    def __init__(self, session=None):
        self.session = session or get_session()

    def requestViewCount(self, requestID):
        request = Request.findById(self.session, requestID)
        if not request:
            return None
        
        if request.view_count is None:
            request.view_count = 0
        
        request.view_count += 1
        self.session.commit()
        return request