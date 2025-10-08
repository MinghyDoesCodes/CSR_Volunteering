"""
ENTITY: UserAccount
Represents a user account in the system
Contains login credentials and personal information
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base


class UserAccount(Base):
    """
    Entity class for User Account
    
    Represents an individual user in the system.
    Each account is assigned a UserProfile (role).
    """
    __tablename__ = 'user_accounts'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Login credentials
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Foreign key to UserProfile
    user_profile_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)
    
    # Relationship to UserProfile (SQLAlchemy handles the JOIN automatically)
    user_profile = relationship("UserProfile", foreign_keys=[user_profile_id])
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<UserAccount(id={self.id}, username='{self.username}', profile='{self.user_profile.profile_name if self.user_profile else None}')>"
    
    def to_dict(self):
        """Convert to dictionary for easy display"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'user_profile_id': self.user_profile_id,
            'user_profile_name': self.user_profile.profile_name if self.user_profile else None,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

