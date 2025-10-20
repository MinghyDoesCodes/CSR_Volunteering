"""
CSR Volunteering System - Flask Web Application
Main application file for the web portal
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db_config import init_database, get_session
from controllers.authentication_controller import AuthenticationController
from controllers.user_account_controller import UserAccountController
from controllers.user_profile_controller import UserProfileController
from controllers.updateUserAccountCtrl import UpdateUserAccountCtrl
from controllers.suspendUserAccountCtrl import SuspendUserAccountCtrl
from controllers.createUserProfileCtrl import CreateUserProfileCtrl
from controllers.viewUserProfileCtrl import ViewUserProfileCtrl
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'csr_volunteering_secret_key_change_in_production'  # Change in production!

# Initialize controllers
auth_controller = AuthenticationController()
account_controller = UserAccountController()
profile_controller = UserProfileController()
updateUserAccountCtrl = UpdateUserAccountCtrl()
suspendUserAccountCtrl = SuspendUserAccountCtrl()
createUserProfileCtrl = CreateUserProfileCtrl()
viewUserProfileCtrl = ViewUserProfileCtrl()


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
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_profile'] = user.user_profile.profile_name
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
    auth_controller.current_user = None
    session.clear()
    flash(f"{username} logged out successfully ", 'success')
    return redirect(url_for('index'))


# ==================== DASHBOARD ====================

@app.route('/dashboard')
@require_login
def dashboard():
    """Main dashboard after login"""
    user = auth_controller.get_current_user()
    return render_template('dashboard.html', user=user)


# ==================== USER ACCOUNT MANAGEMENT ====================

@app.route('/user-accounts')
@require_user_admin
def list_user_accounts():
    """List all user accounts"""
    users = account_controller.get_all_user_accounts()
    return render_template('user_accounts/list.html', users=users)


@app.route('/user-accounts/create', methods=['GET', 'POST'])
@require_user_admin
def create_user_account():
    """Create a new user account"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        user_profile_id = request.form.get('user_profile_id')
        
        success, message, user = account_controller.create_user_account(
            username, email, password, first_name, last_name,
            int(user_profile_id), phone_number if phone_number else None
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('list_user_accounts'))
        else:
            flash(message, 'error')
    
    # Get active profiles for dropdown
    profiles = profile_controller.get_active_user_profiles()
    return render_template('user_accounts/create.html', profiles=profiles)


@app.route('/user-accounts/<int:user_id>')
@require_user_admin
def view_user_account(user_id):
    """View user account details"""
    success, message, user = account_controller.view_user_account(user_id)
    
    if not success:
        flash(message, 'error')
        return redirect(url_for('list_user_accounts'))
    
    return render_template('user_accounts/view.html', user=user)


@app.route('/user-accounts/<int:user_id>/edit', methods=['GET', 'POST'])
@require_user_admin
def updateUserAccount(user_id):
    if request.method == 'POST':
        email = request.form.get('email')
        userName = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        user_profile_id = request.form.get('user_profile_id')
        
        result = updateUserAccountCtrl.updateAccount(
            userID = user_id,
            email = email if email else None,
            userName = userName if userName else None,
            firstName = first_name if first_name else None,
            lastName = last_name if last_name else None,
            phoneNumber = phone_number if phone_number else None,
            userProfileID = int(user_profile_id) if user_profile_id else None
        )
        
        if result == 0:
            flash(f"User account with ID {user_id} not found", 'error')
        elif result == 1:
            flash("Email already in use", 'error')
        elif result == 2:
            flash("Username already in use", 'error')
        elif result == 3:
            flash("Invalid or inactive user profile selected", 'error')
        elif result == 4:
            flash("User account updated successfully", 'success')
            return redirect(url_for('view_user_account', user_id=user_id))
    
    # Get user details
    success, message, user = account_controller.view_user_account(user_id)
    if not success:
        flash(message, 'error')
        return redirect(url_for('list_user_accounts'))
    
    # Get profiles for dropdown
    profiles = profile_controller.get_active_user_profiles()
    return render_template('user_accounts/edit.html', user = user, profiles = profiles)


@app.route('/user-accounts/<int:user_id>/suspend', methods=['POST'])
@require_user_admin
def suspendUserAccount(user_id):
    result = suspendUserAccountCtrl.suspendUser(userID = user_id)
    if result == 0:
        flash(f"User account with ID {user_id} not found", 'error')
    elif result == 1:
        flash("User account is already suspended", 'info')
    elif result == 2:
        flash("User account suspended successfully", 'success')
        return redirect(url_for('view_user_account', user_id = user_id))

@app.route('/user-accounts/<int:user_id>/activate', methods=['POST'])
@require_user_admin
def activateUserAccount(user_id):
    result = suspendUserAccountCtrl.activateUser(userID = user_id)
    if result == 0:
        flash(f"User account with ID {user_id} not found", 'error')
    elif result == 1:
        flash("User account is already active", 'info')
    elif result == 2:
        flash("User account activated successfully", 'success')
        return redirect(url_for('view_user_account', user_id = user_id))

@app.route('/user-accounts/search')
@require_user_admin
def search_user_accounts():
    """Search user accounts"""
    keyword = request.args.get('keyword', '')
    profile_id = request.args.get('profile_id', '')
    status = request.args.get('status', '')
    
    # Convert to appropriate types
    profile_id = int(profile_id) if profile_id else None
    is_active = None
    if status == 'active':
        is_active = True
    elif status == 'suspended':
        is_active = False
    
    # Search
    success, message, users = account_controller.search_user_accounts(
        keyword if keyword else None,
        profile_id,
        is_active
    )
    
    # Get profiles for filter dropdown
    profiles = profile_controller.get_all_user_profiles()
    
    return render_template('user_accounts/search.html', 
                         users=users, 
                         profiles=profiles,
                         keyword=keyword,
                         selected_profile=profile_id,
                         selected_status=status)


# ==================== USER PROFILE MANAGEMENT ====================

@app.route('/user-profiles')
@require_user_admin
def list_user_profiles():
    """List all user profiles"""
    profiles = profile_controller.get_all_user_profiles()
    return render_template('user_profiles/list.html', profiles=profiles)


@app.route('/user-profiles/create', methods=['GET', 'POST'])
@require_user_admin
def create_user_profile():
    """Create a new user profile"""
    if request.method == 'POST':
        profile_name = request.form.get('profile_name')
        description = request.form.get('description')
        
        result = createUserProfileCtrl.createProfile(
            profile_name, description if description else None
        )
        
        if result == 2:  # Success
            flash(f"User profile '{profile_name}' created successfully", 'success')
            return redirect(url_for('list_user_profiles'))
        elif result == 1:  # Already exists
            flash(f"Profile '{profile_name}' already exists", 'error')
        else:  # Error
            flash("Error creating user profile", 'error')
    
    return render_template('user_profiles/create.html')


@app.route('/user-profiles/<int:profile_id>')
@require_user_admin
def view_user_profile(profile_id):
    """View user profile details"""
    result, profile = viewUserProfileCtrl.viewProfile(profile_id)
    
    if result == 0:  # Not found or error
        flash(f"User profile with ID {profile_id} not found", 'error')
        return redirect(url_for('list_user_profiles'))
    
    return render_template('user_profiles/view.html', profile=profile)


@app.route('/user-profiles/<int:profile_id>/edit', methods=['GET', 'POST'])
@require_user_admin
def edit_user_profile(profile_id):
    """Edit user profile"""
    if request.method == 'POST':
        profile_name = request.form.get('profile_name')
        description = request.form.get('description')
        
        success, message, profile = profile_controller.update_user_profile(
            profile_id,
            profile_name=profile_name if profile_name else None,
            description=description if description else None
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('view_user_profile', profile_id=profile_id))
        else:
            flash(message, 'error')
    
    # Get profile details
    result, profile = viewUserProfileCtrl.viewProfile(profile_id)
    if result == 0:  # Not found or error
        flash(f"User profile with ID {profile_id} not found", 'error')
        return redirect(url_for('list_user_profiles'))
    
    return render_template('user_profiles/edit.html', profile=profile)


@app.route('/user-profiles/<int:profile_id>/suspend', methods=['POST'])
@require_user_admin
def suspend_user_profile(profile_id):
    """Suspend user profile"""
    success, message = profile_controller.suspend_user_profile(profile_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('view_user_profile', profile_id=profile_id))


@app.route('/user-profiles/<int:profile_id>/activate', methods=['POST'])
@require_user_admin
def activate_user_profile(profile_id):
    """Activate user profile"""
    success, message = profile_controller.activate_user_profile(profile_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('view_user_profile', profile_id=profile_id))


@app.route('/user-profiles/search')
@require_user_admin
def search_user_profiles():
    """Search user profiles"""
    keyword = request.args.get('keyword', '')
    status = request.args.get('status', '')
    
    # Convert status
    is_active = None
    if status == 'active':
        is_active = True
    elif status == 'suspended':
        is_active = False
    
    # Search
    success, message, profiles = profile_controller.search_user_profiles(
        keyword if keyword else None,
        is_active
    )
    
    return render_template('user_profiles/search.html', 
                         profiles=profiles,
                         keyword=keyword,
                         selected_status=status)


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

