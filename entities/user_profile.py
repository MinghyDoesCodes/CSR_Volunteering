"""
ENTITY: UserProfile
Represents a user profile type/role in the system
Examples: User Admin, Platform Manager, CSR Rep, PIN
"""

from sqlalchemy import Column, Integer, String, Boolean, Text
from database.db_config import Base


class UserProfile(Base):
    """
    Entity class for User Profile (Role/Profile Type)
    
    This represents different types of user roles in the system.
    Each UserAccount will be assigned one UserProfile.
    """
    __tablename__ = 'user_profiles'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Profile details
    profile_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<UserProfile(id={self.id}, name='{self.profile_name}', active={self.is_active})>"
    
    def to_dict(self):
        """Convert to dictionary for easy display"""
        return {
            'id': self.id,
            'profile_name': self.profile_name,
            'description': self.description,
            'is_active': self.is_active
        }

