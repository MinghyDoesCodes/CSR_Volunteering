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
    
    @classmethod
    def create_user_profile(cls, profile_name, description=None):
        """
        Creates a new UserProfile instance
        
        Args:
            profile_name (str): Name of the profile/role
            description (str, optional): Description of the profile
            
        Returns:
            UserProfile: New UserProfile instance
        """
        return cls(
            profile_name=profile_name,
            description=description,
            is_active=True
        )
    
    @classmethod
    def findById(cls, session, profile_id):
        """Fetch a user profile by ID"""
        return session.query(cls).filter_by(id=profile_id).first()
    
    def getAllProfiles(session):
        "Fetch all profiles"
        return session.query(UserProfile).all()
    
    def getActiveProfiles(session):
        "Fetch active profiles"
        return session.query(UserProfile).filter_by(is_active = True).all()
    
    @classmethod
    def checkProfileNameExists(cls, session, profile_name, exclude_id=None):
        """Check if a profile name already exists in the database"""
        query = session.query(cls).filter(cls.profile_name == profile_name)
        if exclude_id:
            query = query.filter(cls.id != exclude_id)
        return session.query(query.exists()).scalar()
    
    def updateProfile(self, session, **kwargs):
        """
        Update profile fields safely while maintaining unique constraints.
        Accepts only whitelisted fields.
        """
        allowed_fields = {'profile_name', 'description'}
        
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        # Check if profile_name is being updated and if it's unique
        if 'profile_name' in update_data and UserProfile.checkProfileNameExists(session, update_data['profile_name'], exclude_id=self.id):
            return 1 # Profile name already in use
        
        for key, value in update_data.items():
            setattr(self, key, value)
        
        session.commit()
        return 2 # Success
    
    def suspendProfile(self, session):
        """Suspend the user profile"""
        if not self.is_active:
            return False  # Already suspended
        self.is_active = False
        session.commit()
        return True
    
    def activateProfile(self, session):
        """Activate the user profile"""
        if self.is_active:
            return False  # Already active
        self.is_active = True
        session.commit()
        return True

