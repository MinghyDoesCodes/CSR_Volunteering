from flask import render_template, request, redirect, url_for, flash
from database.db_config import close_session
from controllers.authentication_controller import AuthenticationController
from controllers.Category.createCategoryCtrl import CreateCategoryCtrl
from controllers.Category.viewCategoryCtrl import ViewCategoryCtrl
from controllers.Category.updateCategoryCtrl import UpdateCategoryCtrl
from controllers.Category.suspendCategoryCtrl import SuspendCategoryCtrl
from controllers.Category.searchCategoryCtrl import SearchCategoryCtrl
from controllers.PM.createDailyReportCtrl import CreateDailyReportCtrl
from controllers.PM.createWeeklyReportCtrl import CreateWeeklyReportCtrl
from controllers.PM.createMonthlyReportCtrl import CreateMonthlyReportCtrl
from datetime import datetime

class ListCategoryUI:
    def __init__(self):
        self.c = ViewCategoryCtrl()

    def DisplayPage(self):
        categories = self.c.listCategories()
        close_session()
        return render_template('categories/list.html', categories=categories)

class CreateCategoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = CreateCategoryCtrl()

    def createCategory(self, request):
        if request.method == 'POST':
            user_id = self.a.get_current_user().id
            title = request.form.get('category_title')
            description = request.form.get('category_description')

            result = self.c.createCategory(
                userID=user_id,
                title=title,
                description=description
            )
            close_session()
            if result == 0:
                flash("User does not exist", 'error')
            elif result == 1:
                flash("Category created successfully", 'success')
                return redirect(url_for('listCategories'))
        
        return render_template('categories/create.html')

class ViewCategoryUI:
    def __init__(self):
        self.c = ViewCategoryCtrl()
        self.a = AuthenticationController()

    def viewCategory(self, category_id):
        current_user = self.a.get_current_user()
        user_profile = current_user.user_profile.profile_name if current_user else None
        category = self.c.viewCategory(category_id)
        if not category:  # Not found
            flash(f"Category with ID {category_id} not found", 'error')
            return redirect(url_for('listCategories'))
        
        render = render_template('categories/view.html', category=category, user_profile=user_profile)
        close_session()
        return render
    
class UpdateCategoryUI:
    def __init__(self):
        self.c = UpdateCategoryCtrl()
        self.v = ViewCategoryCtrl()

    def onClick(self, category_id):
        if request.method == 'POST':
            title = request.form.get('category_title')
            description = request.form.get('category_description')

            result = self.c.updateCategory(
                categoryID=category_id,
                title=title,
                description=description
            )

            if result == 0:
                flash(f"Category with ID {category_id} not found", 'error')
            elif result == 1:
                flash("Category updated successfully", 'success')
                return redirect(url_for('listCategories'))
            
        category = self.v.viewCategory(category_id)
        if not category:
            flash(f"Category with ID {category_id} not found", 'error')
            return redirect(url_for('listCategories'))

        render = render_template('categories/edit.html', category=category)
        close_session()
        return render
    
class SuspendCategoryUI:
    def __init__(self):
        self.c = SuspendCategoryCtrl()
        self.v = ViewCategoryCtrl()

    def onClick(self, category_id):
        category = self.v.viewCategory(category_id)
        if not category:
            flash(f"Category with ID {category_id} not found", 'error')
            return redirect(url_for('listCategories'))
        result = self.c.suspendCategory(category_id)
        
        if result == 0:
            flash(f"Category with ID {category_id} not found", 'error')
        elif result == 1:
            flash(f"Category '{category.title}' is already suspended", 'info')
        elif result == 2:
            flash(f"Category '{category.title}' suspended successfully", 'success')
        close_session()
        return redirect(url_for('listCategories'))
    
    def activateCategory(self, category_id):
        category = self.v.viewCategory(category_id)
        if not category:
            flash(f"Category with ID {category_id} not found", 'error')
            return redirect(url_for('listCategories'))
        result = self.c.activateCategory(category_id)
        
        if result == 0:
            flash(f"Category with ID {category_id} not found", 'error')
        elif result == 1:
            flash(f"Category '{category.title}' is already active", 'info')
        elif result == 2:
            flash(f"Category '{category.title}' activated successfully", 'success')
        close_session()
        return redirect(url_for('listCategories'))
    
class SearchCategoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = SearchCategoryCtrl()

    def onClick(self):
        keyword = request.args.get('keyword', '')
        current_user = self.a.get_current_user()
        user_profile = current_user.user_profile.profile_name if current_user else None
        categories = self.c.searchCategory(keyword or None, None)

        render = render_template('categories/search.html',
                        categories=categories,
                        keyword=keyword,
                        user_profile=user_profile)
        close_session()
        return render

class DailyReportUI:
    def __init__(self):
        self.c = CreateDailyReportCtrl()

    def handle_create_daily_report(self):
        """Generate daily report"""
        date_param = request.args.get('date', None)
        report_date = None
        if date_param:
            try:
                report_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                try:
                    report_date = datetime.strptime(f"{date_param}-01", '%Y-%m-%d').date()
                except ValueError:
                    flash("Invalid date format. Use YYYY-MM or YYYY-MM-DD", 'error')
                    report_date = None

        report_data = self.c.createDailyReport(report_date)
        return render_template('reports/daily.html', report=report_data)


class WeeklyReportUI:
    def __init__(self):
        self.c = CreateWeeklyReportCtrl()

    def handle_create_weekly_report(self):
        """Generate weekly report"""
        date_param = request.args.get('date', None)
        report_date = None
        if date_param:
            try:
                report_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                try:
                    report_date = datetime.strptime(f"{date_param}-01", '%Y-%m-%d').date()
                except ValueError:
                    flash("Invalid date format. Use YYYY-MM or YYYY-MM-DD", 'error')
                    report_date = None

        report_data = self.c.createWeeklyReport(report_date)
        return render_template('reports/weekly.html', report=report_data)


class MonthlyReportUI:
    def __init__(self):
        self.c = CreateMonthlyReportCtrl()

    def handle_create_monthly_report(self):
        """Generate monthly report"""
        date_param = request.args.get('date', None)
        report_date = None
        if date_param:
            try:
                report_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                try:
                    report_date = datetime.strptime(f"{date_param}-01", '%Y-%m-%d').date()
                except ValueError:
                    flash("Invalid date format. Use YYYY-MM or YYYY-MM-DD", 'error')
                    report_date = None

        report_data = self.c.createMonthlyReport(report_date)
        return render_template('reports/monthly.html', report=report_data)