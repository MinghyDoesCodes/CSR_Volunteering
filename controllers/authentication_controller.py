"""
CONTROLLER: AuthenticationController
Handles user authentication (login/logout)
Business logic for user sessions
"""

import bcrypt
from entities.user_account import UserAccount
from database.db_config import get_session


class AuthenticationController:
    """
    Control class for authentication operations
    
    Handles:
    - User login validation
    - Password verification
    - Session management
    """
    
    def __init__(self):
        self.session = get_session()
        self.current_user = None
    
    def login(self, username, password):
        """
        User Story 1: As a User Admin, I want to log in
        
        Validates credentials and creates a session
        
        Args:
            username (str): The username
            password (str): The plain text password
            
        Returns:
            tuple: (success: bool, message: str, user: UserAccount or None)
        """
        try:
            # Query database for user
            user = self.session.query(UserAccount).filter_by(username=username).first()
            
            # Check if user exists
            if not user:
                return (False, "Invalid username or password", None)
            
            # Check if account is suspended
            if not user.is_active:
                return (False, "Account is suspended. Please contact administrator.", None)
            
            # Verify password
            password_match = bcrypt.checkpw(
                password.encode('utf-8'),
                user.password_hash.encode('utf-8')
            )
            
            if not password_match:
                return (False, "Invalid username or password", None)
            
            # Check if user profile is active
            if not user.user_profile.is_active:
                return (False, "Your user profile is suspended. Please contact administrator.", None)
            
            # Successful login
            self.current_user = user
            return (True, f"Welcome, {user.first_name}!", user)
            
        except Exception as e:
            return (False, f"Login error: {str(e)}", None)
    
    def logout(self):
        """
        User Story 2: As a User Admin, I want to log out
        
        Terminates the current user session
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            return (True, f"User '{username}' logged out successfully")
        else:
            return (False, "No user is currently logged in")
    
    def get_current_user(self):
        """
        Get the currently logged-in user
        
        Returns:
            UserAccount or None: The current user object
        """
        return self.current_user
    
    def is_logged_in(self):
        """
        Check if a user is currently logged in
        
        Returns:
            bool: True if user is logged in
        """
        return self.current_user is not None
    
    def has_profile(self, profile_name):
        """
        Check if current user has a specific profile/role
        
        Args:
            profile_name (str): The profile name to check
            
        Returns:
            bool: True if user has the specified profile
        """
        if not self.current_user:
            return False
        return self.current_user.user_profile.profile_name == profile_name

