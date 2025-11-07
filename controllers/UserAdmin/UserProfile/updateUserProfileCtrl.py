from entities.user_profile import UserProfile as UP
from database.db_config import get_session

class UpdateUserProfileCtrl:
    def __init__(self):
        self.session = get_session()

    def updateProfile(self, profile_id, profile_name, description):
        
        user = UP.findById(self.session, profile_id)
        if not user:
            return 0 # User not found
            
        result = user.updateProfile(self.session,profile_name=profile_name,description=description)
        
        return result # 1: Profile Name in use, 2: Success