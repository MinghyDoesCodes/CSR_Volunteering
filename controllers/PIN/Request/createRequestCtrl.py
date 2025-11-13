from entities.request import Request
from database.db_config import get_session

class CreateRequestCtrl:
    def __init__(self, session=None):
        self.session = get_session()

    def createRequest(self, userAccountID, title, categoryID, description):
        
        result = Request.createRequest(
            self.session,
            userID=userAccountID,
            title=title,
            categoryID=categoryID,
            description=description
        )
        return result # 0: User does not exist, 1: Success