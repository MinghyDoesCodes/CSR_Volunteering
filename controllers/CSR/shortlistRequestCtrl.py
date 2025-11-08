"""
CONTROLLER: ShortlistRequestCtrl
Handles shortlisting requests by CSR Reps
"""
from entities.shortlist import Shortlist
from database.db_config import get_session


class ShortlistRequestCtrl:
    """
    Controller for shortlisting requests
    """
    
    def __init__(self):
        self.session = get_session()
    
    def shortlistRequest(self, request_id, csr_rep_id):
        """
        Shortlist a request for a CSR Rep
        
        Args:
            request_id (int): The request to shortlist
            csr_rep_id (int): The CSR Rep doing the shortlisting
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check if already shortlisted
        existing = self.session.query(Shortlist).filter_by(
            request_id=request_id,
            csr_rep_id=csr_rep_id
        ).first()
        
        if existing:
            return (False, "Request already in your shortlist")
        
        # Create shortlist
        shortlist = Shortlist.createShortlist(
            self.session,
            request_id=request_id,
            csr_rep_id=csr_rep_id
        )
        
        return (True, "Request added to shortlist successfully")
    
    def isShortlisted(self, request_id, csr_rep_id):
        """
        Check if a CSR Rep has shortlisted a request
        
        Args:
            request_id (int): The request to check
            csr_rep_id (int): The CSR Rep to check
            
        Returns:
            bool: True if shortlisted, False otherwise
        """
        existing = self.session.query(Shortlist).filter_by(
            request_id=request_id,
            csr_rep_id=csr_rep_id
        ).first()
        
        return existing is not None
    
    def removeShortlist(self, request_id, csr_rep_id):
        result = Shortlist.removeShortlist(self.session, request_id, csr_rep_id)
        return result