from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base
from entities.user_account import UserAccount as UA

class Request(Base):
    __tablename__ = 'requests'
    
    # Primary key
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to UserAccount
    user_account_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    
    # Relationship to UserAccount
    pin = relationship("UserAccount", back_populates="requests")
    
    # Relationship to Shortlists
    shortlists = relationship("Shortlist", back_populates="request")
    
    # Relationship to Matches
    matches = relationship("Match", back_populates="request")
    
    # Request details
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default='Pending', nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Request(id={self.request_id}, title='{self.title}', status='{self.status}')>"
    
    def findById(session, request_id):
        """Find a request by its ID"""
        return session.query(Request).filter_by(request_id=request_id).first()
    
    def getAllRequests(session):
        """Get all requests"""
        return session.query(Request).all()
    
    def createRequest(session, user_account_id, title, description):

        user = UA.findById(session, user_account_id)
        if not user:
            return 0 # User does not exist

        """Create a new request"""
        request = Request(
            user_account_id=user_account_id,
            title=title,
            description=description
        )
        session.add(request)
        session.commit()
        return 1
    
    def updateRequest(self , session, title, description, status):
        """Update request details"""
        self.title = title
        self.description = description
        self.status = status
        session.commit()
        return 1
    
    def deleteRequest(self, session):
        """Delete a request"""
        session.delete(self)
        session.commit()
        return 2
    
    def searchRequests(session, keyword, status):
        """Search requests by keyword and status"""
        query = session.query(Request)
        
        # Apply keyword filter
        if keyword:
            keyword_filter = f"%{keyword}%"
            query = query.filter(
                (Request.title.ilike(keyword_filter)) |
                (Request.description.ilike(keyword_filter))
            )
        
        # Apply status filter
        if status:
            query = query.filter_by(status=status)
        
        return query.all()
