# Changed all boundaries to be their own classes instead of 1 class multiple functions
# Pushed all app.py logic here so app.py can just be an entry point and router
# Need to check with teacher if boundaries also need to be their own classes too
# If need, then need to refactor every existing function in app.py to follow this format in this file
# I will push all these into user_admin_boundary.py and add in the user profile functions
# The other functions will go into their respective boundary

from flask import render_template, request, redirect, url_for, flash
from database.db_config import close_session
from controllers.viewUserAccountCtrl import ViewUserAccountCtrl
from controllers.viewUserProfileCtrl import ViewUserProfileCtrl
from controllers.createUserAccountCtrl import CreateUserAccountCtrl
from controllers.updateUserAccountCtrl import UpdateUserAccountCtrl
from controllers.suspendUserAccountCtrl import SuspendUserAccountCtrl
from controllers.searchUserAccountController import SearchUserAccountController


class ListUserAccountUI:
    def __init__(self):
        self.c = ViewUserAccountCtrl()

    def displayPage(self):
        users = self.c.listAccounts()
        close_session()
        return render_template('user_accounts/list.html', users=users)
    
class CreateUserAccountUI:
    def __init__(self):
        self.c = CreateUserAccountCtrl()
        self.p = ViewUserProfileCtrl()

    def createUserAccount(self, request):
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone_number = request.form.get('phone_number')
            user_profile_id = request.form.get('user_profile_id')
            password = request.form.get('password')
            
            result = self.c.createAccount(
                email, username, first_name, last_name, 
                phone_number if phone_number else None,
                int(user_profile_id), password
            )
            close_session()
        
            if result == 1:
                flash("Email already in use", 'error')
            elif result == 2:
                flash("Username already in use", 'error')
            elif result == 3:
                flash("Invalid or inactive user profile selected", 'error')
            elif result == 4:
                flash("User account created successfully", 'success')
                return redirect(url_for('list_user_accounts'))
    
        # Get active profiles for dropdown
        profiles = self.p.getActiveProfiles()
        return render_template('user_accounts/create.html', profiles=profiles)
    
class ViewUserAccountUI:
    def __init__(self):
        self.c = ViewUserAccountCtrl()

    def viewUserAccount(self, user_id):
        user = self.c.viewAccount(user_id)
        close_session()
        if not user: # Not Found
            flash(f"User account with ID {user_id} not found", 'error')
            return redirect(url_for('list_user_accounts'))
        
        return render_template('user_accounts/view.html', user = user)
    
class UpdateUserAccountUI:
    def __init__(self):
        self.c = UpdateUserAccountCtrl()
        self.vc = ViewUserAccountCtrl()
        self.p = ViewUserProfileCtrl()

    def updateUserAccount(self, user_id):
        if request.method == 'POST':
            email = request.form.get('email')
            userName = request.form.get('username')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone_number = request.form.get('phone_number')
            user_profile_id = request.form.get('user_profile_id')

            result = self.c.updateAccount(
                userID = user_id,
                email = email if email else None,
                userName = userName if userName else None,
                firstName = first_name if first_name else None,
                lastName = last_name if last_name else None,
                phoneNumber = phone_number if phone_number else None,
                userProfileID = int(user_profile_id) if user_profile_id else None
            )

            close_session()

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
        user = self.vc.viewAccount(user_id)
        
        if not user:  # Not found
            flash(f"User account with ID {user_id} not found", 'error')
            return redirect(url_for('list_user_accounts'))
        
        # Get profiles for dropdown
        profiles = self.p.getActiveProfiles()
        return render_template('user_accounts/edit.html', user = user, profiles = profiles)
    
class SuspendUserAccountUI:
    def __init__(self):
        self.c = SuspendUserAccountCtrl()

    def suspendUserAccount(self, user_id):
        result = self.c.suspendUser(user_id)
        close_session()
        if result == 0:
            flash(f"User account with ID {user_id} not found", 'error')
        elif result == 1:
            flash("User account is already suspended", 'info')
        elif result == 2:
            flash("User account suspended successfully", 'success')
            return redirect(url_for('view_user_account', user_id = user_id))
        
    def activateUserAccount(self, user_id):
        result = self.c.activateUser(user_id)
        close_session()
        if result == 0:
            flash(f"User account with ID {user_id} not found", 'error')
        elif result == 1:
            flash("User account is already active", 'info')
        elif result == 2:
            flash("User account activated successfully", 'success')
            return redirect(url_for('view_user_account', user_id = user_id))
        
class SearchUserAccountUI:
    def __init__(self):
        self.c = SearchUserAccountController()
        self.p = ViewUserProfileCtrl()

    def onClick(self):
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
        users = self.c.searchUserAccount(
            keyword if keyword else None,
            profile_id,
            is_active
        )

        profiles = self.p.getAllProfiles()
        return render_template('user_accounts/search.html',
                               users = users,
                               profiles = profiles,
                               keyword = keyword,
                               selected_profile = profile_id,
                               selected_status = status)