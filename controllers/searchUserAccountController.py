from entities.user_account import UserAccount
from database.db_config import get_session
from sqlalchemy import or_

class SearchUserAccountController:
    def __init__(self):
        self.session = get_session()

    def searchUserAccount(self, keyword=None, profile_id=None, is_active=None):
        """
        User Story 7: As a User Admin, I want to search for a user
        
        Searches for user accounts based on criteria
        
        Args:
            keyword (str, optional): Search in username, email, first_name, last_name
            profile_id (int, optional): Filter by user profile ID
            is_active (bool, optional): Filter by account status
            
        Returns:
            tuple: (success: bool, message: str, users: list of UserAccount)
        """
        try:
            query = self.session.query(UserAccount)
            
            # Apply keyword filter (search in multiple fields)
            if keyword:
                search_pattern = f"%{keyword}%"
                query = query.filter(
                    or_(
                        UserAccount.username.like(search_pattern),
                        UserAccount.email.like(search_pattern),
                        UserAccount.first_name.like(search_pattern),
                        UserAccount.last_name.like(search_pattern)
                    )
                )
            
            # Apply profile filter
            if profile_id is not None:
                query = query.filter_by(user_profile_id=profile_id)
            
            # Apply status filter
            if is_active is not None:
                query = query.filter_by(is_active=is_active)
            
            users = query.all()
            
            if not users:
                return (True, "No user accounts found matching the criteria", [])
            
            return (True, f"Found {len(users)} user account(s)", users)
            
        except Exception as e:
            return (False, f"Error searching user accounts: {str(e)}", []) 