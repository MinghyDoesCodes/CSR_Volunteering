"""
CONTROLLER: ViewShortlistCountCtrl
Handles getting shortlist count for requests (for PIN users)
"""
from entities.shortlist import Shortlist
from database.db_config import get_session


class ViewShortlistCountCtrl:
    """
    Controller for viewing shortlist counts
    
    This controller provides functionality for PIN users to view
    how many times their requests have been shortlisted by CSR Reps.
    """
    
    def __init__(self):
        self.session = get_session()
    
    def getShortlistCount(self, request_id):
        """
        Get the shortlist count for a specific request
        
        Args:
            request_id (int): The ID of the request
            
        Returns:
            int: Number of times the request has been shortlisted
        """
        return Shortlist.countShortlistsForRequest(self.session, request_id)
    
    def getShortlistCountsForUser(self, user_id):
        """
        Get shortlist counts for all requests overnight by a specific user (PIN)
        
        Args:
            user_id (int): The ID of the PIN user
            
        Returns:
            dict: Dictionary mapping request_id to shortlist count
            Example: {1: 3, 2: 0, 3: 1}
        """
        from entities.request import Request
        
        # Get all requests for this user
        user_requests = self.session.query(Request).filter_by(user_account_id=user_id).all()
        
        # Build a dictionary of request_id -> shortlist_count
        counts = {}
        for request in user_requests:
            counts[request.request_id] = Shortlist.countShortlistsForRequest(self.session, request.request_id)
        
        return counts
