from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base
import bcrypt
from entities.user_profile import UserProfile


class UserAccount(Base):
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
    user_profile = relationship("UserProfile")
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def findByUsername(session, username):
        """Fetch a user account by username"""
        return session.query(UserAccount).filter_by(username=username).first()
    
    def verifyPassword(self, password):
        """Verify a plaintext password against the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def checkActive(self):
        """Check if the user account and user profile is active"""
        if not self.is_active:
            raise ValueError("Account is suspended. Please contact administrator.")
        if self.user_profile and not self.user_profile.is_active:
            raise ValueError("Your user profile is suspended. Please contact administrator.")
        return True

    def findById(session, userID):
        """Fetch a user account by ID"""
        return session.query(UserAccount).filter_by(id=userID).first()
    
    def checkEmailExists(session, email, excludeID=None):
        """Check if an email already exists in the database"""
        query = session.query(UserAccount).filter(UserAccount.email == email)
        if excludeID:
            query = query.filter(UserAccount.id != excludeID)
        return session.query(query.exists()).scalar()
    
    # def checkUsernameExists(cls, session, username, excludeID=None):
    #     """Check if a username already exists in the database"""
    #     query = session.query(cls).filter(cls.username == username)
    #     if excludeID:
    #         query = query.filter(cls.id != excludeID)
    #     return session.query(query.exists()).scalar()
    
    def updateAccount(self, session, **kwargs):
        """
        Update user fields safely while maintaining unique constraints.
        Accepts only whitelisted fields.
        """
        allowed_fields = {'email', 'first_name', 'last_name', 'phone_number', 'user_profile_id'}
        
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        # Check if email is being updated and if it's unique
        if 'email' in update_data and UserAccount.checkEmailExists(session, update_data['email'], excludeID=self.id):
            raise ValueError("Email already in use by another account.")      
            
        # Check if user_profile_id is valid and active
        if 'user_profile_id' in update_data:
            profile = session.query(UserProfile).filter_by(
                id = update_data['user_profile_id'],
                is_active = True
            ).first()
            if not profile:
                raise ValueError("Invalid or inactive user profile selected.")

        for key, value in update_data.items():
            setattr(self, key, value)

        self.updated_at = datetime.now()
        session.commit()
        return True
    
    def suspendUser(self, session):
        """Suspend the user account"""
        if not self.is_active:
            return False  # Already suspended
        self.is_active = False
        self.updated_at = datetime.now()
        session.commit()
        return True
    
    def activate(self, session):
        """Activate the user account"""
        if self.is_active:
            return False  # Already active
        self.is_active = True
        self.updated_at = datetime.now()
        session.commit()
        return True
    
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

