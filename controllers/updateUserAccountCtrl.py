from entities.user_account import UserAccount as UA
from database.db_config import get_session

class UpdateUserAccountCtrl:
    def __init__(self):
        self.session = get_session()

    def updateAccount(self, userID, email = None, firstName = None,
                lastName = None, phoneNumber = None, userProfileID = None):
    
        try:
            user = UA.findById(self.session, userID)
            if not user:
                return (False, f"User account with ID {userID} not found")
            
            #prepare data for update
            update_data = {
                'email': email,
                'first_name': firstName,
                'last_name': lastName,
                'phone_number': phoneNumber,
                'user_profile_id': userProfileID
            }

            # Remove None values for fields not being updated
            update_data = {k: v for k, v in update_data.items() if v is not None}

            success = user.updateAccount(self.session, **update_data)

            if success:
                return (True, f"User account '{user.username}' updated successfully")
            else:
                return (False, "Failed to update user account")
            
        except ValueError as ve:
            return (False, str(ve))
        except Exception as e:
            self.session.rollback()
            return (False, f"Error updating user account: {str(e)}")
