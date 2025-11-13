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
        
        # Create shortlist
        result = Shortlist.createShortlist(
            self.session,
            request_id=request_id,
            csr_rep_id=csr_rep_id
        )
        return result  # 1: Already shortlisted, 2: Success
    
    def isShortlisted(self, request_id, csr_rep_id):
        
        result = Shortlist.checkIfShortlisted(
            self.session,
            request_id,
            csr_rep_id
        )
        return result # True/False
    
    def removeShortlist(self, request_id, csr_rep_id):
        result = Shortlist.removeShortlist(self.session, request_id, csr_rep_id)
        return result # 1: Not shortlisted, 2: Successful