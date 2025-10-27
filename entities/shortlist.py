"""
ENTITY: Shortlist
Represents when a CSR Rep shortlists a request
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base


class Shortlist(Base):
    """
    Entity class for Shortlist
    
    This represents when a CSR Rep shortlists (bookmarks) a request.
    Each shortlist records:
    - Which request was shortlisted
    - Which CSR Rep shortlisted it
    - When they shortlisted it
    """
    __tablename__ = 'shortlists'
    
    # Primary key
    shortlist_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys
    request_id = Column(Integer, ForeignKey('requests.request_id'), nullable=False)
    csr_rep_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    
    # Relationship to Request
    request = relationship("Request", back_populates="shortlists")
    
    # Relationship to UserAccount (CSR Rep who shortlisted)
    csr_rep = relationship("UserAccount", back_populates="shortlists")
    
    # Timestamp
    shortlisted_at = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<Shortlist(id={self.shortlist_id}, request={self.request_id}, csr_rep={self.csr_rep_id})>"
    
    @classmethod
    def findById(cls, session, shortlist_id):
        """Find a shortlist by its ID"""
        return session.query(cls).filter_by(shortlist_id=shortlist_id).first()
    
    @classmethod
    def getShortlistsByRequest(cls, session, request_id):
        """Get all shortlists for a specific request"""
        return session.query(cls).filter_by(request_id=request_id).all()
    
    @classmethod
    def countShortlistsForRequest(cls, session, request_id):
        """Count how many times a request has been shortlisted"""
        return session.query(cls).filter_by(request_id=request_id).count()
    
    @classmethod
    def createShortlist(cls, session, request_id, csr_rep_id):
        """
        Create a new shortlist entry
        
        Args:
            session: Database session
            request_id (int): The request being shortlisted
            csr_rep_id (int): The CSR Rep who is shortlisting
            
        Returns:
            Shortlist: New shortlist instance
        """
        shortlist = cls(
            request_id=request_id,
            csr_rep_id=csr_rep_id
        )
        session.add(shortlist)
        session.commit()
        return shortlist
