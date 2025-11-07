from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, or_
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import IntegrityError
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

    # Relationship to Requests
    requests = relationship("Request", back_populates="pin")
    
    # Relationship to Shortlists (for CSR Reps who shortlist requests)
    shortlists = relationship("Shortlist", back_populates="csr_rep")
    
    # Relationship to Matches (as PIN)
    matches_as_pin = relationship("Match", foreign_keys="Match.pin_id", back_populates="pin")
    
    # Relationship to Matches (as CSR Rep)
    matches_as_csr = relationship("Match", foreign_keys="Match.csr_rep_id", back_populates="csr_rep")

    # Relationship to categories (as Platform Manager)
    categories = relationship("Category", back_populates="creator")

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def login(session, username, password):
        """Authenticate user by username and password"""
        user = session.query(UserAccount).filter_by(
            username=username).options(joinedload(UserAccount.user_profile)).first()
        if not user:
            raise ValueError("No user found with this username.")
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise ValueError("Incorrect password.")
        
        if not user.is_active:
            raise ValueError("Account is suspended. Please contact administrator.")
        
        if not user.user_profile or not user.user_profile.is_active:
            raise ValueError("Your user profile is suspended. Please contact administrator.")
        
        return user

    def findById(session, userID):
        """Fetch a user account by ID"""
        return session.query(UserAccount).filter_by(id=userID).options(joinedload(UserAccount.user_profile)).first()
    
    def getAllAccounts(session):
        """Fetch all user accounts"""
        return session.query(UserAccount).options(joinedload(UserAccount.user_profile)).all()
    
    def checkEmailExists(session, email, excludeID=None):
        """Check if an email already exists in the database"""
        query = session.query(UserAccount).filter(UserAccount.email == email)
        if excludeID:
            query = query.filter(UserAccount.id != excludeID)
        return session.query(query.exists()).scalar()
    
    def checkUsernameExists(session, username, excludeID=None):
        """Check if a username already exists in the database"""
        query = session.query(UserAccount).filter(UserAccount.username == username)
        if excludeID:
            query = query.filter(UserAccount.id != excludeID)
        return session.query(query.exists()).scalar()
    
    def createAccount(session, email, userName, firstName, lastName,
                    phoneNumber, userProfileID, password):
        
        # Normalize
        email_norm = (email or "").strip().lower()
        username_norm = (userName or "").strip()

        # Duplicates
        if UserAccount.checkEmailExists(session, email_norm):
            return 1
        if UserAccount.checkUsernameExists(session, username_norm):
            return 2

        # Profile must be active
        profile = session.query(UserProfile).filter_by(
            id=userProfileID, is_active=True
        ).first()
        if not profile:
            return 3

        if not password:
            raise ValueError("Password is required to create an account.")

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user = UserAccount(
            username=username_norm,
            email=email_norm,
            password_hash=pw_hash,
            first_name=(firstName or "").strip(),
            last_name=(lastName or "").strip(),
            phone_number=(phoneNumber or "").strip() if phoneNumber else None,
            user_profile_id=profile.id,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Race-safe re-check
            if UserAccount.checkEmailExists(session, email_norm):
                return 1
            if UserAccount.checkUsernameExists(session, username_norm):
                return 2
            raise

        return 4  # Success
    
    def updateAccount(self, session, email, userName, firstName, lastName, phoneNumber, userProfileID):

        # Normalize
        email = (email or "").strip().lower()
        userName = (userName or "").strip()

        if UserAccount.checkEmailExists(session, email, excludeID = self.id):
            return 1  # Email already in use
        
        if UserAccount.checkUsernameExists(session, userName, excludeID = self.id):
            return 2  # Username already in use

        profile = session.query(UserProfile).filter_by(
            id = userProfileID,
            is_active = True
        ).first()
        if not profile:
            return 3  # Invalid or inactive user profile selected.
        
        self.email = email
        self.username = userName
        self.first_name = firstName
        self.last_name = lastName
        self.phone_number = phoneNumber
        self.user_profile_id = userProfileID
        self.updated_at = datetime.now()
        session.commit()
        return 4  # Success
    
    def suspendUser(self, session):
        """Suspend the user account"""
        if not self.is_active:
            return 1  # Already suspended
        self.is_active = False
        self.updated_at = datetime.now()
        session.commit()
        return 2 # Successfully suspended
    
    def activate(self, session):
        """Activate the user account"""
        if self.is_active:
            return 1  # Already active
        self.is_active = True
        self.updated_at = datetime.now()
        session.commit()
        return 2 # Successfully activated
    
    def searchUserAccount(session, keyword, profile_id, is_active):
        query = session.query(UserAccount)

        # Apply keyword filter (search in multiple fields)
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    UserAccount.username.like(search_pattern),
                    UserAccount.email.like(search_pattern),
                    UserAccount.first_name.like(search_pattern),
                    UserAccount.last_name.like(search_pattern)
                )
            )

        # Apply profile filter
        if profile_id:
            query = query.filter_by(user_profile_id=profile_id)

        # Apply status filter
        if is_active is not None:
            query = query.filter_by(is_active=is_active)

        return query.options(joinedload(UserAccount.user_profile)).all()
    
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

