from entities.request import Request
from database.db_config import get_session

class DeleteRequestCtrl:
    def __init__(self):
        self.session = get_session()

    def deleteRequest(self, requestID):
        """Delete a request by its ID"""
        request = Request.findById(self.session, requestID)
        if not request:
            return 0  # Request does not exist
        
        if request.status == 'Completed':
            return 1  # Cannot delete a completed request

        result = request.deleteRequest(self.session)
        return result  # 2: Successfully deleted