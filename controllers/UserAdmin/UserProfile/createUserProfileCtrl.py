from entities.user_profile import UserProfile as UP
from database.db_config import get_session

class CreateUserProfileCtrl:
    def __init__(self):
        self.session = get_session()

    def createProfile(self, profileName, description=None):
        
        try:
            # Check if profile name already exists
            existing = self.session.query(UP).filter_by(
                profile_name=profileName
            ).first()
            
            if existing:
                return 1  # Profile already exists
            
            # Create new profile using Entity method
            new_profile = UP.create_user_profile(
                profile_name=profileName,
                description=description
            )
            
            self.session.add(new_profile)
            self.session.commit()
            
            return 2  # Success
            
        except Exception as e:
            self.session.rollback()
            return 0  # Error

