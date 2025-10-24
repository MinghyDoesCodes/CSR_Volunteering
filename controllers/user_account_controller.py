"""
CONTROLLER: UserAccountController
Handles user account management operations
Business logic for CRUD operations on user accounts
"""

import bcrypt
from entities.user_account import UserAccount
from entities.user_profile import UserProfile
from database.db_config import get_session
from sqlalchemy import or_


class UserAccountController:
    """
    Control class for user account operations
    
    Handles:
    - Creating user accounts
    - Viewing user accounts
    - Updating user accounts
    - Suspending user accounts
    - Searching for user accounts
    """
    
    def __init__(self):
        self.session = get_session()
    
    def create_user_account(self, username, email, password, first_name, last_name, 
                           user_profile_id, phone_number=None):
        """
        User Story 3: As a User Admin, I want to create a user account
        
        Creates a new user account in the system
        
        Args:
            username (str): Unique username
            email (str): Unique email address
            password (str): Plain text password (will be hashed)
            first_name (str): User's first name
            last_name (str): User's last name
            user_profile_id (int): ID of the user profile/role
            phone_number (str, optional): User's phone number
            
        Returns:
            tuple: (success: bool, message: str, user_account: UserAccount or None)
        """
        try:
            # Validate user profile exists and is active
            profile = self.session.query(UserProfile).filter_by(
                id=user_profile_id, 
                is_active=True
            ).first()
            
            if not profile:
                return (False, "Invalid or inactive user profile selected", None)
            
            # Check if username already exists
            existing_user = self.session.query(UserAccount).filter_by(username=username).first()
            if existing_user:
                return (False, f"Username '{username}' already exists", None)
            
            # Check if email already exists
            existing_email = self.session.query(UserAccount).filter_by(email=email).first()
            if existing_email:
                return (False, f"Email '{email}' already exists", None)
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create new user account
            new_user = UserAccount(
                username=username,
                email=email,
                password_hash=hashed_password.decode('utf-8'),
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                user_profile_id=user_profile_id,
                is_active=True
            )
            
            # Add to database
            self.session.add(new_user)
            self.session.commit()
            
            return (True, f"User account '{username}' created successfully", new_user)
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error creating user account: {str(e)}", None)
    
    def view_user_account(self, user_id):
        """
        User Story 4: As a User Admin, I want to view a user account
        
        Retrieves details of a specific user account
        
        Args:
            user_id (int): The user account ID
            
        Returns:
            tuple: (success: bool, message: str, user_account: UserAccount or None)
        """
        try:
            user = self.session.query(UserAccount).filter_by(id=user_id).first()
            
            if not user:
                return (False, f"User account with ID {user_id} not found", None)
            
            return (True, "User account retrieved successfully", user)
            
        except Exception as e:
            return (False, f"Error retrieving user account: {str(e)}", None)
    
    def get_all_user_accounts(self):
        """
        Get all user accounts
        
        Returns:
            list: List of all UserAccount objects
        """
        try:
            return self.session.query(UserAccount).all()
        except Exception as e:
            print(f"Error retrieving all users: {str(e)}")
            return []

