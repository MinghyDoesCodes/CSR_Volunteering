from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base

class Category(Base):
    __tablename__ = 'categories'
    
    # Primary key
    category_id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key to UserAccount (creator)
    created_by = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)

    # Relationship to UserAccount
    creator = relationship("UserAccount", back_populates="categories")

    # Relationship to Requests
    requests = relationship("Request", back_populates="category")
    
    # Category details
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default='Active', nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Category(id={self.category_id}, name='{self.title}')>"
    
    def findById(session, category_id):
        """Find a category by its ID"""
        return session.query(Category).filter_by(category_id=category_id).first()
    
    def getAllCategories(session):
        """Get all categories"""
        return session.query(Category).all()
    
    def getActiveCategories(session):
        """Get all active categories"""
        return session.query(Category).filter_by(status='Active').all()
    
    def createCategory(session, userID, title, description=None):
        from entities.user_account import UserAccount as UA
        user = UA.findById(session, userID)
        if not user:
            return 0 # User does not exist
        
        """Create a new category"""
        category = Category(
            created_by=userID,
            title=title,
            description=description,
        )
        session.add(category)
        session.commit()
        return 1 # Success