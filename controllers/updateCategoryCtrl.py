from entities.category import Category
from database.db_config import get_session

class UpdateCategoryCtrl:
    def __init__(self):
        self.session = get_session()

    def updateCategory(self, title,description,status, categoryID):
        
        category = Category.findById(self.session, categoryID)
        if not category:
            return 0 # User not found
            
        result = category.updateCategory(self.session,title,description,status)
        
        return result # Success