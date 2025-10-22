# createUserAccountCtrl.py
from entities.user_account import UserAccount as UA
from database.db_config import get_session

class CreateUserAccountCtrl:
    def __init__(self, session=None):
        self.session = get_session()

    def createAccount(self, email, userName, firstName, lastName,
                phoneNumber, userProfileID, password):
        
        result = UA.createAccount(
            self.session,
            email=email,
            userName=userName,
            firstName=firstName,
            lastName=lastName,
            phoneNumber=phoneNumber,
            userProfileID=userProfileID,
            password=password,
        )
        return result # 1: Email in use, 2: Username in use, 3: Invalid profile, 4: Success
