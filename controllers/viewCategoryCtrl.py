from entities.category import Category
from database.db_config import get_session

class ViewCategoryCtrl:
    def __init__(self, session=None):
        self.session = session or get_session()

    def viewCategory(self, categoryID):
        category = Category.findById(self.session, categoryID)
        if not category:
            return None  # Not found
        return category
    
    def listCategories(self):
        return Category.getAllCategories(self.session)
    
    def listActiveCategories(self):
        return Category.getActiveCategories(self.session)