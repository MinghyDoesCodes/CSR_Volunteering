from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
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
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
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
    
    def updateCategory(self,session, title, description, status):
        
        """Update request details"""
        self.title = title
        self.description = description
        self.status = status
        session.commit()
        return 1
    
    def suspendCategory(self, session):
        """Suspend the category"""
        if not self.is_active:
            return 1  # Already suspended
        self.is_active = False
        self.updated_at = datetime.now()
        self.status = 'Suspended'
        session.commit()
        return 2 # Successfully suspended
    
    def activateCategory(self, session):
        """Activate the category"""
        if self.is_active:
            return 1  # Already active
        self.is_active = True
        self.updated_at = datetime.now()
        self.status = 'Active'
        session.commit()
        return 2 # Successfully activated
    
    def searchCategory(session, keyword, status):
        """Search category by keyword and status"""
        query = session.query(Category)

        #Apply keyword filter
        if keyword:
            keyword_filter = f"%{keyword}%"
            query = query.filter(
                (Category.title.ilike(keyword_filter)) |
                (Category.description.ilike(keyword_filter))
            )

        #Apply status filter
        if status:
            # Normalize status to match database format (capitalize first letter)
            # Form sends "active" or "suspended", but DB stores "Active" or "Suspended"
            normalized_status = status.capitalize()
            query = query.filter_by(status=normalized_status)
        
        return query.all()
