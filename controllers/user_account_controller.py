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
    
    def update_user_account(self, user_id, email=None, first_name=None, last_name=None,
                           phone_number=None, user_profile_id=None):
        """
        User Story 5: As a User Admin, I want to update a user account
        
        Updates user account information
        Note: Username and password are not updated here (separate methods)
        
        Args:
            user_id (int): The user account ID
            email (str, optional): New email
            first_name (str, optional): New first name
            last_name (str, optional): New last name
            phone_number (str, optional): New phone number
            user_profile_id (int, optional): New user profile ID
            
        Returns:
            tuple: (success: bool, message: str, user_account: UserAccount or None)
        """
        try:
            user = self.session.query(UserAccount).filter_by(id=user_id).first()
            
            if not user:
                return (False, f"User account with ID {user_id} not found", None)
            
            # Update fields if provided
            if email is not None:
                # Check if email already exists for another user
                existing = self.session.query(UserAccount).filter(
                    UserAccount.email == email,
                    UserAccount.id != user_id
                ).first()
                if existing:
                    return (False, f"Email '{email}' already exists", None)
                user.email = email
            
            if first_name is not None:
                user.first_name = first_name
            
            if last_name is not None:
                user.last_name = last_name
            
            if phone_number is not None:
                user.phone_number = phone_number
            
            if user_profile_id is not None:
                # Validate profile exists and is active
                profile = self.session.query(UserProfile).filter_by(
                    id=user_profile_id,
                    is_active=True
                ).first()
                if not profile:
                    return (False, "Invalid or inactive user profile selected", None)
                user.user_profile_id = user_profile_id
            
            self.session.commit()
            
            return (True, f"User account '{user.username}' updated successfully", user)
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error updating user account: {str(e)}", None)
    
    def suspend_user_account(self, user_id):
        """
        User Story 6: As a User Admin, I want to suspend a user account
        
        Suspends a user account (user cannot login)
        
        Args:
            user_id (int): The user account ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            user = self.session.query(UserAccount).filter_by(id=user_id).first()
            
            if not user:
                return (False, f"User account with ID {user_id} not found")
            
            if not user.is_active:
                return (False, f"User account '{user.username}' is already suspended")
            
            user.is_active = False
            self.session.commit()
            
            return (True, f"User account '{user.username}' suspended successfully")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error suspending user account: {str(e)}")
    
    def activate_user_account(self, user_id):
        """
        Reactivates a suspended user account
        
        Args:
            user_id (int): The user account ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            user = self.session.query(UserAccount).filter_by(id=user_id).first()
            
            if not user:
                return (False, f"User account with ID {user_id} not found")
            
            if user.is_active:
                return (False, f"User account '{user.username}' is already active")
            
            user.is_active = True
            self.session.commit()
            
            return (True, f"User account '{user.username}' activated successfully")
            
        except Exception as e:
            self.session.rollback()
            return (False, f"Error activating user account: {str(e)}")
    
    def search_user_accounts(self, keyword=None, profile_id=None, is_active=None):
        """
        User Story 7: As a User Admin, I want to search for a user
        
        Searches for user accounts based on criteria
        
        Args:
            keyword (str, optional): Search in username, email, first_name, last_name
            profile_id (int, optional): Filter by user profile ID
            is_active (bool, optional): Filter by account status
            
        Returns:
            tuple: (success: bool, message: str, users: list of UserAccount)
        """
        try:
            query = self.session.query(UserAccount)
            
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
            if profile_id is not None:
                query = query.filter_by(user_profile_id=profile_id)
            
            # Apply status filter
            if is_active is not None:
                query = query.filter_by(is_active=is_active)
            
            users = query.all()
            
            if not users:
                return (True, "No user accounts found matching the criteria", [])
            
            return (True, f"Found {len(users)} user account(s)", users)
            
        except Exception as e:
            return (False, f"Error searching user accounts: {str(e)}", [])
    
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

