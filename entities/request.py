from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from datetime import datetime
from database.db_config import Base
from entities.user_account import UserAccount

class Request(Base):
    __tablename__ = 'requests'
    
    # Primary key
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to UserAccount
    user_account_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    
    # Relationship to UserAccount
    pin = relationship("UserAccount", back_populates="requests")

    # Foreign key to category
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=True)

    # Relationship to Category
    category = relationship("Category", back_populates="requests")
    
    # Relationship to Shortlists
    shortlists = relationship("Shortlist", back_populates="request")
    
    # Relationship to Matches
    matches = relationship("Match", back_populates="request")
    
    # Request details
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default='Pending', nullable=False)

    # View Counter
    view_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Request(id={self.request_id}, title='{self.title}', status='{self.status}', views={self.view_count})>"
    
    def findById(session, request_id):
        """Find a request by its ID"""
        return session.query(Request).filter_by(request_id=request_id).first()
    
    def getAllRequests(session):
        """Get all requests"""
        return session.query(Request).all()
    
    def increment_view(self, session):
        """Increment and persist view count"""
        self.view_count +=  1
        session.commit()
    
    def createRequest(session, userID, title, categoryID, description):
        from entities.user_account import UserAccount as UA
        user = UA.findById(session, userID)
        if not user:
            return 0 # User does not exist

        """Create a new request"""
        request = Request(
            user_account_id=userID,
            title=title,
            category_id=categoryID,
            description=description
        )
        session.add(request)
        session.commit()
        return 1
    
    def updateRequest(self , session, title, categoryID, description, status):
        """Update request details"""
        self.title = title
        self.category_id = categoryID
        self.description = description
        self.status = status
        session.commit()
        return 1
    
    def deleteRequest(self, session):
        """Delete a request"""
        # Delete all related shortlists first (to avoid foreign key constraint violation)
        from entities.shortlist import Shortlist
        shortlists_to_delete = session.query(Shortlist).filter_by(request_id=self.request_id).all()
        for shortlist in shortlists_to_delete:
            session.delete(shortlist)
        
        # Delete all related matches
        from entities.match import Match
        matches_to_delete = session.query(Match).filter_by(request_id=self.request_id).all()
        for match in matches_to_delete:
            session.delete(match)
        
        # Now delete the request
        session.delete(self)
        session.commit()
        return 2
    
    def searchRequests(session, keyword, status):
        """Search requests by keyword and status"""
        # query = session.query(Request)
        query = (
            session.query(Request)
            .join(UserAccount, Request.user_account_id == UserAccount.id)
            .options(joinedload(Request.pin))
        )
        
        
        # Apply keyword filter
        if keyword:
            keyword_filter = f"%{keyword}%"
            query = query.filter(
                (Request.title.ilike(keyword_filter)) |
                (Request.description.ilike(keyword_filter)) |
                (UserAccount.username.ilike(keyword_filter)) |
                (UserAccount.first_name.ilike(keyword_filter))
            )
        
        # Apply status filter
        if status:
            # Normalize status to match database format (capitalize first letter)
            # Form sends "pending" or "completed", but DB stores "Pending" or "Completed"
            normalized_status = status.capitalize()
            query = query.filter(Request.status == normalized_status)
        
        return query.all()