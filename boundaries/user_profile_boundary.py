from flask import render_template, request, redirect, url_for, flash
from database.db_config import close_session
from controllers.UserAdmin.UserProfile.viewUserProfileCtrl import ViewUserProfileCtrl
from controllers.UserAdmin.UserProfile.createUserProfileCtrl import CreateUserProfileCtrl
from controllers.UserAdmin.UserProfile.updateUserProfileCtrl import UpdateUserProfileCtrl
from controllers.UserAdmin.UserProfile.suspendUserProfileCtrl import SuspendUserProfileCtrl
from controllers.UserAdmin.UserProfile.searchUserProfileController import SearchUserProfileController

class ListUserProfileUI:
    def __init__(self):
        self.c = ViewUserProfileCtrl()

    def displayPage(self):
        profiles = self.c.getAllProfiles()
        close_session()
        return render_template('user_profiles/list.html', profiles=profiles)
    
class CreateUserProfileUI:
    def __init__(self):
        self.c = CreateUserProfileCtrl()

    def handle_create_user_profile(self, request):
        if request.method == 'POST':
            profile_name = request.form.get('profile_name')
            description = request.form.get('description')

            result = self.c.createProfile(
                profile_name, description if description else None
            )
            close_session()
            if result == 1: # Already exists
                flash(f"Profile '{profile_name}' already exists", 'error')
            elif result == 2:  # Success
                flash(f"User profile '{profile_name}' created successfully", 'success')
                return redirect(url_for('list_user_profiles'))
            else:  # Error
                flash("Error creating user profile", 'error')
        
        return render_template('user_profiles/create.html')

class ViewUserProfileUI:
    def __init__(self):
        self.c = ViewUserProfileCtrl()

    def handle_view_user_profile(self, profile_id):
        profile = self.c.viewProfile(profile_id)
        close_session()
        if not profile:
            flash(f"User profile with ID {profile_id} not found", 'error')
            return redirect(url_for('list_user_profiles'))
        
        return render_template('user_profiles/view.html', profile = profile)

class UpdateUserProfileUI:
    def __init__(self):
        self.c = UpdateUserProfileCtrl()
        self.v = ViewUserProfileCtrl()

    def onClick(self, profile_id):
        if request.method == 'POST':
            profile_name = request.form.get('profile_name')
            description = request.form.get('description')

            result = self.c.updateProfile(
                profile_id= profile_id,
                profile_name=profile_name if profile_name else None,
                description=description if description else None
            )
            close_session()
            if result == 0:
                flash(f"User profile with ID {profile_id} not found", 'error')
            elif result == 1:
                flash("Profile name already in use", 'error')
            elif result == 2:
                flash("User profile updated successfully", 'success')
                return redirect(url_for('view_user_profile', profile_id=profile_id))
            
        # Get profile details
        profile = self.v.viewProfile(profile_id)
        close_session()
        if not profile:  # Not found
            flash(f"User profile with ID {profile_id} not found", 'error')
            return redirect(url_for('list_user_profiles'))
        
        return render_template('user_profiles/edit.html', profile=profile)

class SuspendUserProfileUI:
    def __init__(self):
        self.c = SuspendUserProfileCtrl()

    def onClick(self, profile_id):
        result = self.c.suspendProfile(profile_id)
        close_session()
        if result == False:
            flash(f"User profile with ID {profile_id} not found or is already suspended", 'error')

        flash("User profile suspended successfully", 'success')
        return redirect(url_for('view_user_profile', profile_id=profile_id))
    
    def activateProfile(self, profile_id):
        result = self.c.activateProfile(profile_id)
        close_session()
        if result == False:
            flash(f"User profile with ID {profile_id} not found or is already active", 'error')

        flash("User profile activated successfully", 'success')
        return redirect(url_for('view_user_profile', profile_id=profile_id))
        
class SearchUserProfileUI:
    def __init__(self):
        self.c = SearchUserProfileController()

    def onClick(self):
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        # Convert status
        is_active = None
        if status == 'active':
            is_active = True
        elif status == 'suspended':
            is_active = False

        # Search
        profiles = self.c.searchUserProfile(
            keyword if keyword else None,
            is_active
        )
        close_session()
        return render_template('user_profiles/search.html', 
                         profiles=profiles,
                         keyword=keyword,
                         selected_status=status)