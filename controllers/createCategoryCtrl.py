from entities.category import Category
from database.db_config import get_session

class CreateCategoryCtrl:
    def __init__(self, session=None):
        self.session = get_session()

    def createCategory(self, userID, title, description=None):
        
        result = Category.createCategory(
            self.session,
            userID=userID,
            title=title,
            description=description
        )
        return result # 0: User does not exist, 1: Success