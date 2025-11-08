from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base
from sqlalchemy.orm import joinedload
from entities.request import Request
from entities.user_account import UserAccount

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

    @classmethod
    def removeShortlist(cls, session, request_id, csr_rep_id):
        shortlist = session.query(cls).filter_by(
            request_id=request_id,
            csr_rep_id=csr_rep_id
        ).first()

        if not shortlist:
            return 1 # Not part of shortlist
        
        session.delete(shortlist)
        session.commit()
        return 2 # Successfully removed from shortlist
    
    @classmethod
    def searchShortlist(cls, session, userID, keyword):
        query = (
            session.query(cls)
            .join(Request, cls.request_id == Request.request_id)
            .join(UserAccount, Request.user_account_id == UserAccount.id)
            .filter(cls.csr_rep_id == userID)
            .options(
                joinedload(cls.request).joinedload(Request.category),
                joinedload(cls.request).joinedload(Request.pin)
            )
        )

        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                (Request.title.ilike(search_pattern)) |
                (Request.description.ilike(search_pattern)) |
                (UserAccount.username.ilike(search_pattern)) |
                (UserAccount.first_name.ilike(search_pattern))
            )

        return query.all()