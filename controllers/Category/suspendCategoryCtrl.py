from entities.category import Category
from database.db_config import get_session

class SuspendCategoryCtrl:
    def __init__(self):
        self.session = get_session()

    def suspendCategory(self, categoryID):

        category = Category.findById(self.session, categoryID)
        if not category:
            return 0 # User not found
        
        result = category.suspendCategory(self.session)

        return result # 1: Already suspended, 2: Successfully suspended
        
    def activateCategory(self, categoryID):
    
        category = Category.findById(self.session, categoryID)
        if not category:
            return 0 # User not found
        
        result = category.activateCategory(self.session)

        return result # 1: Already active, 2: Successfully activated