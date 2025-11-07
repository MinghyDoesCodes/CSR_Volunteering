from entities.request import Request
from database.db_config import get_session

class UpdateRequestCtrl:
    def __init__(self):
        self.session = get_session()

    def updateRequest(self, requestID, title, categoryID, description, status):
        request = Request.findById(self.session, requestID)
        if not request:
            return 0 # Request not found
            
        request.updateRequest(self.session, title, categoryID, description, status)
        
        return 1 # Success