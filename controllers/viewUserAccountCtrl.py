# viewUserAccountCtrl.py
from entities.user_account import UserAccount as UA
from database.db_config import get_session

class ViewUserAccountCtrl:
    """
    Control layer for the 'View User Account' use case.

    Return values:
        0                 -> User not found
        (2, user_dto:dict)-> Success; safe, non-sensitive details for UI
    """

    def __init__(self, session=None):
        self.session = session or get_session()

    def viewAccount(self, userID):
        """
        Fetch a user's details for display.

        Args:
            userID (int)

        Returns:
            int | tuple[int, dict]:
                0 if not found,
                (2, dto) on success. 'dto' is derived from entity.to_dict()
                and must not include sensitive fields (e.g., password_hash).
        """
        dto = UA.viewDetails(self.session, userID)
        if not dto:
            return 0  # Not found

        return 2, dto  # Success
