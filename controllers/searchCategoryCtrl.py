from entities.category import Category
from database.db_config import get_session

class SearchCategoryCtrl:
    def __init__(self):
        self.session = get_session()

    def searchCategory(self, keyword, status):
        category = Category.searchCategory(self.session, keyword, status)
        return category # Return the list of categories