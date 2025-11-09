from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db_config import init_database
from controllers.authentication_controller import AuthenticationController
from controllers.CSR.shortlistRequestCtrl import ShortlistRequestCtrl
from controllers.viewHistoryCtrl import ViewHistoryCtrl, AuthError
from boundaries.pin_boundary import PINBoundary
from controllers.CSR.searchShortlistCtrl import searchShortlistCtrl
from controllers.Category.viewCategoryCtrl import ViewCategoryCtrl

import os

# Import boundaries
from boundaries.user_account_boundary import (
    ListUserAccountUI,
    CreateUserAccountUI,
    ViewUserAccountUI,
    UpdateUserAccountUI,
    SuspendUserAccountUI,
    SearchUserAccountUI
)

from boundaries.user_profile_boundary import (
    ListUserProfileUI,
    CreateUserProfileUI,
    ViewUserProfileUI,
    UpdateUserProfileUI,
    SuspendUserProfileUI,
    SearchUserProfileUI
)

from boundaries.request_boundary import (
    ListRequestUI,
    CreateRequestUI,
    ViewRequestUI,
    UpdateRequestUI,
    DeleteRequestUI,
    SearchRequestUI
)

from boundaries.platform_manager_boundary import (
    ListCategoryUI,
    CreateCategoryUI,
    ViewCategoryUI,
    UpdateCategoryUI,
    SuspendCategoryUI,
    SearchCategoryUI,
    DailyReportUI,
    WeeklyReportUI,
    MonthlyReportUI,
)

# Initialize Boundaries
listUserUI = ListUserAccountUI()
createUserUI = CreateUserAccountUI()
viewUserUI = ViewUserAccountUI()
updateUserUI = UpdateUserAccountUI()
suspendUserUI = SuspendUserAccountUI()
searchUserUI = SearchUserAccountUI()

listUPUI = ListUserProfileUI()
createUPUI = CreateUserProfileUI()
viewUPUI = ViewUserProfileUI()
updateUPUI = UpdateUserProfileUI()
suspendUPUI = SuspendUserProfileUI()
searchUPUI = SearchUserProfileUI()

listRequestUI = ListRequestUI()
createRequestUI = CreateRequestUI()
viewRequestUI = ViewRequestUI()
updateRequestUI = UpdateRequestUI()
deleteRequestUI = DeleteRequestUI()
searchRequestUI =SearchRequestUI()

listCategoryUI = ListCategoryUI()
createCategoryUI = CreateCategoryUI()
viewCategoryUI = ViewCategoryUI()
updateCategoryUI = UpdateCategoryUI()
suspendCategoryUI = SuspendCategoryUI()
searchCategoryUI = SearchCategoryUI()
dailyReportUI = DailyReportUI()
weeklyReportUI = WeeklyReportUI()
monthlyReportUI = MonthlyReportUI()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'csr_volunteering_secret_key_change_in_production'  # Change in production!

# Initialize controllers
auth_controller = AuthenticationController()
shortlistRequestCtrl = ShortlistRequestCtrl()
pin_boundary = PINBoundary()
searchShortList = searchShortlistCtrl()
listCategory = ViewCategoryCtrl()

# ==================== HELPER FUNCTIONS ====================

def require_login(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_controller.is_logged_in():
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_user_admin(f):
    """Decorator to require User Admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_controller.is_logged_in():
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        if not auth_controller.has_profile('User Admin'):
            flash('You do not have permission to access this page', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    if auth_controller.is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = auth_controller.login(username, password)
            if user:
                flash(f"Welcome, {user.first_name}!", 'success')
                return redirect(url_for('dashboard'))
            else:
                flash("Login failed. Please try again.", 'error')
        except ValueError as ve:
            flash(str(ve), 'error')
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    session.clear()
    flash(f"{username} logged out successfully ", 'success')
    return redirect(url_for('index'))

# ==================== DASHBOARD ====================

@app.route('/dashboard')
@require_login
def dashboard():
    """Main dashboard after login"""
    user = auth_controller.get_current_user()
    print("User:", user)
    return render_template('dashboard.html', user=user)

# ==================== USER ACCOUNT MANAGEMENT ====================

@app.route('/user-accounts')
@require_user_admin
def list_user_accounts():
    return listUserUI.displayPage()

@app.route('/user-accounts/create', methods=['GET', 'POST'])
@require_user_admin
def create_user_account():
    return createUserUI.createUserAccount(request)

@app.route('/user-accounts/<int:user_id>')
@require_user_admin
def view_user_account(user_id):
    return viewUserUI.viewUserAccount(user_id)

@app.route('/user-accounts/<int:user_id>/edit', methods=['GET', 'POST'])
@require_user_admin
def updateUserAccount(user_id):
    return updateUserUI.updateUserAccount(user_id)

@app.route('/user-accounts/<int:user_id>/suspend', methods=['POST'])
@require_user_admin
def suspendUserAccount(user_id):
    return suspendUserUI.suspendUserAccount(user_id)

@app.route('/user-accounts/<int:user_id>/activate', methods=['POST'])
@require_user_admin
def activateUserAccount(user_id):
    return suspendUserUI.activateUserAccount(user_id)

@app.route('/user-accounts/search')
@require_user_admin
def search_user_accounts():
    return searchUserUI.onClick()

# ==================== USER PROFILE MANAGEMENT ====================

@app.route('/user-profiles')
@require_user_admin
def list_user_profiles():
    return listUPUI.displayPage()

@app.route('/user-profiles/create', methods=['GET', 'POST'])
@require_user_admin
def create_user_profile():
    return createUPUI.handle_create_user_profile(request)

@app.route('/user-profiles/<int:profile_id>')
@require_user_admin
def view_user_profile(profile_id):
    return viewUPUI.handle_view_user_profile(profile_id)

@app.route('/user-profiles/<int:profile_id>/edit', methods=['GET', 'POST'])
@require_user_admin
def edit_user_profile(profile_id):
    return updateUPUI.onClick(profile_id)

@app.route('/user-profiles/<int:profile_id>/suspend', methods=['POST'])
@require_user_admin
def suspend_user_profile(profile_id):
    return suspendUPUI.onClick(profile_id)

@app.route('/user-profiles/<int:profile_id>/activate', methods=['POST'])
@require_user_admin
def activate_user_profile(profile_id):
    return suspendUPUI.activateProfile(profile_id)

@app.route('/user-profiles/search')
@require_user_admin
def search_user_profiles():
    return searchUPUI.onClick()

# ==================== REQUEST MANAGEMENT ====================

@app.route('/requests')
@require_login
def listRequests():
    return listRequestUI.DisplayPage()

@app.route('/requests/create', methods=['GET', 'POST'])
@require_login
def createRequest():
    return createRequestUI.createRequest(request)
    
@app.route('/requests/<int:request_id>')
@require_login
def viewRequest(request_id):
    return viewRequestUI.viewRequest(request_id)
    
@app.route('/requests/<int:request_id>/edit', methods=['GET', 'POST'])
@require_login
def updateRequest(request_id):
    return updateRequestUI.onClick(request_id)

@app.route('/requests/<int:request_id>/delete', methods=['POST'])
@require_login
def deleteRequest(request_id):
    return deleteRequestUI.onClick(request_id)
    
@app.route('/requests/search')
@require_login
def searchRequests():
    return searchRequestUI.onClick()

@app.route('/requests/<int:request_id>/shortlist', methods=['POST'])
@require_login
def shortlistRequest(request_id):
    """Shortlist a request"""
    current_user = auth_controller.get_current_user()
    
    success, message = shortlistRequestCtrl.shortlistRequest(request_id, current_user.id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('viewRequest', request_id=request_id))

@app.route('/requests/<int:request_id>/removeShortlist', methods=['POST'])
@require_login
def removeShortlist(request_id):
    current_user = auth_controller.get_current_user()
    result = shortlistRequestCtrl.removeShortlist(request_id, current_user.id)

    if result == 1:
        flash(f"Request with ID {request_id} is not part of your shortlist", 'error')
    elif result == 2:
        flash(f"Request with ID '{request_id}' successfully removed from your shortlist", 'success')
    else: 
        flash("Error removing request from shortlist", 'error')

    return redirect(url_for('viewRequest', request_id=request_id))

@app.route('/shortlists')
@require_login
def searchShortlists():
    current_user = auth_controller.get_current_user()
    if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
        flash("Access denied. Only CSR Reps can view shortlists.", 'error')
        return redirect(url_for('dashboard'))

    keyword = request.args.get('keyword', '').strip()
    categoryID = request.args.get('category_id', '').strip()
    shortlist = searchShortList.searchShortlist(current_user.id, keyword, categoryID)
    print("Requests: ", shortlist)

    categories = listCategory.listCategories()

    return render_template(
            'shortlist.html',
            requests=shortlist,
            keyword=keyword,
            categories=categories
        )

# ==================== CATEGORY MANAGEMENT ====================

@app.route('/categories')
@require_login
def listCategories():
    return listCategoryUI.DisplayPage()

@app.route('/categories/create', methods=['GET', 'POST'])
@require_login
def createCategory():
    return createCategoryUI.createCategory(request)

@app.route('/categories/<int:category_id>')
@require_login
def viewCategory(category_id):
    return viewCategoryUI.viewCategory(category_id)

@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@require_login
def updateCategory(category_id):
    return updateCategoryUI.onClick(category_id)

@app.route('/category/<int:category_id>/suspend', methods=['POST'])
@require_login
def suspendCategory(category_id):
    return suspendCategoryUI.onClick(category_id)

@app.route('/category/<int:category_id>/activate', methods=['POST'])
@require_login
def activateCategory(category_id):
    return suspendCategoryUI.activateCategory(category_id)

@app.route('/categories/search')
@require_login
def searchCategories():
    return searchCategoryUI.onClick()

# ==================== REPORTS ====================

@app.route('/reports/daily')
@require_login
def createDailyReport():
    return dailyReportUI.handle_create_daily_report()


@app.route('/reports/weekly')
@require_login
def createWeeklyReport():
    return weeklyReportUI.handle_create_weekly_report()


@app.route('/reports/monthly')
@require_login
def createMonthlyReport():
    return monthlyReportUI.handle_create_monthly_report()

# ==================== COMPLETED MATCH HISTORY ====================

@app.route('/completed-history')
@require_login
def viewCompletedHistory():
    """View completed match history for PIN users - Using Boundary Pattern"""
    current_user = auth_controller.get_current_user()
    
    # Check if user is PIN
    if not current_user or current_user.user_profile.profile_name != 'PIN':
        flash('Only PIN users can view completed match history', 'error')
        return redirect(url_for('dashboard'))
    
    # Get page number from query parameter
    page = request.args.get('page', 1, type=int)
    
    # Call Boundary method (matches BCE diagram: onClickHistory())
    result = pin_boundary.onClickHistory(page=page, current_user=current_user)
    
    if result is None:
        # Boundary handles errors internally; show generic error
        flash('Unable to load completed history. Please try again.', 'error')
        return redirect(url_for('dashboard'))
    
    items, total_count, page_meta, user = result
    
    # Boundary prepares data for rendering (matches BCE: renderList())
    render_data = pin_boundary.renderList(items, total_count, page_meta, user)
    
    # Route passes data to template
    return render_template('completed_history/list.html', **render_data)

@app.route('/completed-history/search', methods=['GET'])
@require_login
def searchCompletedHistory():
    """Search/filter completed match history for PIN users - Using Boundary Pattern"""
    current_user = auth_controller.get_current_user()
    
    # Check if user is PIN
    if not current_user or current_user.user_profile.profile_name != 'PIN':
        flash('Only PIN users can view completed match history', 'error')
        return redirect(url_for('dashboard'))
    
    # Get filter parameters from query string
    service_type = request.args.get('serviceType', '').strip() or None
    from_date = request.args.get('from', '').strip() or None
    to_date = request.args.get('to', '').strip() or None
    page = request.args.get('page', 1, type=int)
    
    # Call Boundary method (matches BCE diagram: onSearchClick())
    result = pin_boundary.onSearchClick(
        serviceType=service_type,
        fromDate=from_date,
        toDate=to_date,
        page=page,
        current_user=current_user
    )
    
    if result is None:
        flash('Unable to search completed history. Please check your filters and try again.', 'error')
        return redirect(url_for('viewCompletedHistory'))
    
    items, total_count, page_meta, user, filters = result
    
    # Boundary prepares data for rendering (matches BCE: renderList())
    render_data = pin_boundary.renderList(items, total_count, page_meta, user, filters=filters)
    
    # Route passes data to template
    return render_template('completed_history/list.html', **render_data)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message='Internal server error'), 500


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('csr_volunteering.db'):
        print("Database not found. Initializing...")
        init_database()
        print("Please run: python -m database.init_db")
        print("Then restart the application.")
    else:
        print("\n" + "="*60)
        print("CSR VOLUNTEERING SYSTEM - WEB PORTAL")
        print("="*60)
        print("\nServer starting...")
        print("Access the portal at: http://localhost:5000")
        print("\nDefault admin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nPress CTRL+C to stop the server")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)