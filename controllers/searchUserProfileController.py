from entities.user_profile import UserProfile
from database.db_config import get_session
from sqlalchemy import or_

class SearchUserProfileController :
    def __init__(self):
        self.session = get_session()

    def searchUserProfile(self, keyword=None, is_active=None):
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
    