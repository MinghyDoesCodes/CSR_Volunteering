import bcrypt
from entities.user_account import UserAccount
from database.db_config import get_session


class AuthenticationController:
    def __init__(self):
        self.session = get_session()
        self.current_user = None
    
    def login(self, username, password):
        try:
            user = UserAccount.login(self.session, username, password)
            if user:
                self.current_user = user
                return user
        except ValueError as e:
            raise e
    
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

