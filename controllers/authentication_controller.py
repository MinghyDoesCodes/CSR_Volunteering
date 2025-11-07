import bcrypt
from flask import session
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
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_profile'] = user.user_profile.profile_name
                return user
        except ValueError as e:
            raise e
    
    def get_current_user(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        
        db = get_session()
        user = UserAccount.findById(self.session, user_id)
        return user
    
    def is_logged_in(self):
        """Check if a user is currently logged in."""
        return 'user_id' in session
    
    def has_profile(self, profile_name):
        """Check if the logged-in user has the given profile name."""
        user_profile = session.get('user_profile')
        return user_profile == profile_name

