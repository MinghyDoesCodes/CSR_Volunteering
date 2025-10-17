"""
CONTROLLER: UserProfileController
Handles user profile (role) management operations
Business logic for CRUD operations on user profiles
"""

from entities.user_profile import UserProfile
from database.db_config import get_session
from sqlalchemy import or_


class UserProfileController:
    """
    Control class for user profile operations
    
    Handles:
    - Creating user profiles (role types)
    - Viewing user profiles
    - Updating user profiles
    - Suspending user profiles
    - Searching for user profiles
    """
    
    def __init__(self):
        self.session = get_session()
    
    def create_user_profile(self, profile_name, description=None):
        """
        User Story 8: As a User Admin, I want to create a user profile
        
        Creates a new user profile (role type)
        
        Args:
            profile_name (str): Name of the profile/role
            description (str, optional): Description of the profile
            
        Returns:
            tuple: (success: bool, message: str, profile: UserProfile or None)
        """
        try:
            # Check if profile name already exists
            existing = self.session.query(UserProfile).filter_by(
                profile_name=profile_name
            ).first()
            
            if existing:
                return (False, f"Profile '{profile_name}' already exists", None)
            
            # Create new profile using Entity method
            new_profile = UserProfile.create_user_profile(
                profile_name=profile_name,
                description=description
            )
            
            self.session.add(new_profile)
            self.session.commit()
            
            return (True, f"User profile '{profile_name}' created successfully", new_profile)
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error creating user profile: {str(e)}", None)
    
    def view_user_profile(self, profile_id):
        """
        User Story 9: As a User Admin, I want to view a user profile
        
        Retrieves details of a specific user profile
        
        Args:
            profile_id (int): The profile ID
            
        Returns:
            tuple: (success: bool, message: str, profile: UserProfile or None)
        """
        try:
            profile = UserProfile.findById(self.session, profile_id)
            
            if not profile:
                return (False, f"User profile with ID {profile_id} not found", None)
            
            return (True, "User profile retrieved successfully", profile)
            
        except Exception as e:
            return (False, f"Error retrieving user profile: {str(e)}", None)
    
    def update_user_profile(self, profile_id, profile_name=None, description=None):
        """
        User Story 10: As a User Admin, I want to update a user profile
        
        Updates user profile information
        
        Args:
            profile_id (int): The profile ID
            profile_name (str, optional): New profile name
            description (str, optional): New description
            
        Returns:
            tuple: (success: bool, message: str, profile: UserProfile or None)
        """
        try:
            profile = UserProfile.findById(self.session, profile_id)
            
            if not profile:
                return (False, f"User profile with ID {profile_id} not found", None)
            
            # Prepare data for update
            update_data = {
                'profile_name': profile_name,
                'description': description
            }
            
            # Remove None values for fields not being updated
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            success = profile.updateProfile(self.session, **update_data)
            
            if success:
                return (True, f"User profile '{profile.profile_name}' updated successfully", profile)
            else:
                return (False, "Failed to update user profile", None)
            
        except ValueError as ve:
            return (False, str(ve), None)
        except Exception as e:
            self.session.rollback()
            return (False, f"Error updating user profile: {str(e)}", None)
    
    def suspend_user_profile(self, profile_id):
        """
        User Story 11: As a User Admin, I want to suspend a user profile
        
        Suspends a user profile (cannot be assigned to new users)
        Note: Existing users with this profile can still login
        
        Args:
            profile_id (int): The profile ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            profile = UserProfile.findById(self.session, profile_id)
            
            if not profile:
                return (False, f"User profile with ID {profile_id} not found")
            
            success = profile.suspendProfile(self.session)
            
            if success:
                return (True, f"User profile '{profile.profile_name}' suspended successfully")
            else:
                return (False, f"User profile '{profile.profile_name}' is already suspended")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error suspending user profile: {str(e)}")
    
    def activate_user_profile(self, profile_id):
        """
        Reactivates a suspended user profile
        
        Args:
            profile_id (int): The profile ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            profile = UserProfile.findById(self.session, profile_id)
            
            if not profile:
                return (False, f"User profile with ID {profile_id} not found")
            
            success = profile.activateProfile(self.session)
            
            if success:
                return (True, f"User profile '{profile.profile_name}' activated successfully")
            else:
                return (False, f"User profile '{profile.profile_name}' is already active")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error activating user profile: {str(e)}")
    
    def search_user_profiles(self, keyword=None, is_active=None):
        """
        User Story 12: As a User Admin, I want to search for a user profile
        
        Searches for user profiles based on criteria
        
        Args:
            keyword (str, optional): Search in profile name and description
            is_active (bool, optional): Filter by profile status
            
        Returns:
            tuple: (success: bool, message: str, profiles: list of UserProfile)
        """
        try:
            query = self.session.query(UserProfile)
            
            # Apply keyword filter
            if keyword:
                search_pattern = f"%{keyword}%"
                query = query.filter(
                    or_(
                        UserProfile.profile_name.like(search_pattern),
                        UserProfile.description.like(search_pattern)
                    )
                )
            
            # Apply status filter
            if is_active is not None:
                query = query.filter_by(is_active=is_active)
            
            profiles = query.all()
            
            if not profiles:
                return (True, "No user profiles found matching the criteria", [])
            
            return (True, f"Found {len(profiles)} user profile(s)", profiles)
            
        except Exception as e:
            return (False, f"Error searching user profiles: {str(e)}", [])
    
    def get_all_user_profiles(self):
        """
        Get all user profiles
        
        Returns:
            list: List of all UserProfile objects
        """
        try:
            return self.session.query(UserProfile).all()
        except Exception as e:
            print(f"Error retrieving all profiles: {str(e)}")
            return []
    
    def get_active_user_profiles(self):
        """
        Get only active user profiles (for selection when creating users)
        
        Returns:
            list: List of active UserProfile objects
        """
        try:
            return self.session.query(UserProfile).filter_by(is_active=True).all()
        except Exception as e:
            print(f"Error retrieving active profiles: {str(e)}")
            return []

