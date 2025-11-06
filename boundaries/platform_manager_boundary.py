"""
BOUNDARY: PlatformManagerBoundary
User interface for Platform Manager operations
Handles all user interactions and displays (Web-based)
"""

from controllers.createCategoryCtrl import CreateCategoryCtrl
from controllers.viewCategoryCtrl import ViewCategoryCtrl
from controllers.updateCategoryCtrl import UpdateCategoryCtrl
from controllers.suspendCategoryCtrl import SuspendCategoryCtrl
from controllers.createDailyReportCtrl import CreateDailyReportCtrl
from controllers.authentication_controller import AuthenticationController


class PlatformManagerBoundary:
    """
    Boundary class for Platform Manager interface
    
    This is the user interface layer for Platform Manager users
    to interact with category management and reporting operations.
    """
    
    def __init__(self):
        self.auth_controller = AuthenticationController()
        self.create_category_ctrl = CreateCategoryCtrl()
        self.view_category_ctrl = ViewCategoryCtrl()
        self.update_category_ctrl = UpdateCategoryCtrl()
        self.suspend_category_ctrl = SuspendCategoryCtrl()
        self.create_daily_report_ctrl = CreateDailyReportCtrl()
    
    # ==================== CATEGORY MANAGEMENT ====================
    
    def handle_create_category(self, user_id, title, description):
        """
        Handle creating a new category
        
        Args:
            user_id (int): ID of the Platform Manager creating the category
            title (str): Category title
            description (str): Category description
            
        Returns:
            int: Result code (0: User does not exist, 1: Success)
        """
        return self.create_category_ctrl.createCategory(
            userID=user_id,
            title=title,
            description=description
        )
    
    def handle_view_category(self, category_id):
        """
        Handle viewing a category
        
        Args:
            category_id (int): ID of the category to view
            
        Returns:
            Category: Category object or None if not found
        """
        return self.view_category_ctrl.viewCategory(category_id)
    
    def handle_list_categories(self):
        """
        Handle listing all categories
        
        Returns:
            list: List of all categories
        """
        return self.view_category_ctrl.listCategories()
    
    def handle_list_active_categories(self):
        """
        Handle listing active categories
        
        Returns:
            list: List of active categories
        """
        return self.view_category_ctrl.listActiveCategories()
    
    def handle_update_category(self, category_id, title, description, status):
        """
        Handle updating a category
        
        Args:
            category_id (int): ID of the category to update
            title (str): New title (optional)
            description (str): New description (optional)
            status (str): New status (optional)
            
        Returns:
            int: Result code (0: Not found, 1: Success)
        """
        return self.update_category_ctrl.updateCategory(
            categoryID=category_id,
            title=title,
            description=description,
            status=status
        )
    
    def handle_suspend_category(self, category_id):
        """
        Handle suspending a category
        
        Args:
            category_id (int): ID of the category to suspend
            
        Returns:
            int: Result code (0: Not found, 1: Already suspended, 2: Success)
        """
        return self.suspend_category_ctrl.suspendCategory(categoryID=category_id)
    
    def handle_activate_category(self, category_id):
        """
        Handle activating a category
        
        Args:
            category_id (int): ID of the category to activate
            
        Returns:
            int: Result code (0: Not found, 1: Already active, 2: Success)
        """
        return self.suspend_category_ctrl.activateCategory(categoryID=category_id)
    
    # ==================== REPORT GENERATION ====================
    
    def handle_create_daily_report(self, report_date=None):
        """
        Handle creating a daily report
        
        Args:
            report_date (date, optional): Date for the report. Defaults to today.
            
        Returns:
            dict: Report data containing statistics, changes, and category breakdown
        """
        return self.create_daily_report_ctrl.createDailyReport(report_date)
    
    def render_daily_report(self, report_data):
        """
        Prepare data for rendering the daily report template
        
        Args:
            report_data (dict): Report data from controller
            
        Returns:
            dict: Data structure for template rendering
        """
        return {
            'report': report_data
        }

