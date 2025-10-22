# createUserAccountCtrl.py
from entities.user_account import UserAccount as UA
from database.db_config import get_session

class CreateUserAccountCtrl:
    """
    Control layer for the 'Create User Account' use case.

    Return codes from UA.createAccount(...):
        1 -> Email already in use
        2 -> Username already in use
        3 -> Invalid or inactive user profile
        4 -> Success
    """

    def __init__(self, session=None):
        # Allow DI of a session for unit tests; default to app session.
        self.session = session or get_session()

    def createAccount(self, email, userName, firstName, lastName,
                      phoneNumber, userProfileID, password):
        """
        Orchestrates the create flow (Boundary -> Controller -> Entity).
        Delegates all validation, hashing, persistence, and auditing to the Entity.

        Args:
            email (str)
            userName (str)
            firstName (str)
            lastName (str)
            phoneNumber (str|None)
            userProfileID (int)
            password (str)

        Returns:
            int: One of {1, 2, 3, 4} as defined above.
        """
        # Delegate to Entity; mirrors your UpdateUserAccountCtrl pattern.
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
        return result
