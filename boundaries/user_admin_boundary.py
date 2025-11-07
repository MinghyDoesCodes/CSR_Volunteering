"""
BOUNDARY: UserAdminBoundary
User interface for User Admin operations
Handles all user interactions and displays (CLI-based for now)
"""

from controllers.authentication_controller import AuthenticationController
from controllers.user_account_controller import UserAccountController
from controllers.user_profile_controller import UserProfileController
from controllers.UserAdmin.UserProfile.createUserProfileCtrl import CreateUserProfileCtrl
from controllers.UserAdmin.UserProfile.viewUserProfileCtrl import ViewUserProfileCtrl
from controllers.UserAdmin.UserAccount.searchUserAccountController import SearchUserAccountController
from controllers.UserAdmin.UserProfile.searchUserProfileController import SearchUserProfileController


class UserAdminBoundary:
    """
    Boundary class for User Admin interface
    
    This is the user interface layer that interacts with the user
    and calls appropriate controllers to perform operations.
    """
    
    def __init__(self):
        self.auth_controller = AuthenticationController()
        self.account_controller = UserAccountController()
        self.profile_controller = UserProfileController()
        self.create_profile_ctrl = CreateUserProfileCtrl()
        self.view_profile_ctrl = ViewUserProfileCtrl()
        self.search_user_account_controller = SearchUserAccountController()
        self.search_user_profile_controller = SearchUserProfileController()
    
    def display_menu(self):
        """Display the main menu for User Admin"""
        print("\n" + "="*60)
        print("CSR VOLUNTEERING SYSTEM - USER ADMIN DASHBOARD")
        print("="*60)
        
        if self.auth_controller.is_logged_in():
            user = self.auth_controller.get_current_user()
            print(f"Logged in as: {user.first_name} {user.last_name} ({user.username})")
            print(f"Role: {user.user_profile.profile_name}")
        
        print("\n--- USER ACCOUNT MANAGEMENT ---")
        print("1.  Login")
        print("2.  Logout")
        print("3.  Create User Account")
        print("4.  View User Account")
        print("5.  Update User Account")
        print("6.  Suspend/Activate User Account")
        print("7.  Search User Accounts")
        print("8.  List All User Accounts")
        
        print("\n--- USER PROFILE MANAGEMENT ---")
        print("9.  Create User Profile")
        print("10. View User Profile")
        print("11. Update User Profile")
        print("12. Suspend/Activate User Profile")
        print("13. Search User Profiles")
        print("14. List All User Profiles")
        
        print("\n--- OTHER ---")
        print("0.  Exit")
        print("="*60)
    
    def run(self):
        """Main loop for the User Admin interface"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_logout()
            elif choice == "3":
                self.handle_create_user_account()
            elif choice == "4":
                self.handle_view_user_account()
            elif choice == "5":
                self.handle_update_user_account()
            elif choice == "6":
                self.handle_suspend_activate_user_account()
            elif choice == "7":
                self.handle_search_user_accounts()
            elif choice == "8":
                self.handle_list_all_user_accounts()
            elif choice == "9":
                self.handle_create_user_profile()
            elif choice == "10":
                self.handle_view_user_profile()
            elif choice == "11":
                self.handle_update_user_profile()
            elif choice == "12":
                self.handle_suspend_activate_user_profile()
            elif choice == "13":
                self.handle_search_user_profiles()
            elif choice == "14":
                self.handle_list_all_user_profiles()
            elif choice == "0":
                print("\nThank you for using CSR Volunteering System!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    # ==================== AUTHENTICATION ====================
    
    def handle_login(self):
        """Handle user login"""
        print("\n--- LOGIN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message, user = self.auth_controller.login(username, password)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def handle_logout(self):
        """Handle user logout"""
        print("\n--- LOGOUT ---")
        success, message = self.auth_controller.logout()
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    # ==================== USER ACCOUNT OPERATIONS ====================
    
    def handle_create_user_account(self):
        """Handle creating a new user account"""
        print("\n--- CREATE USER ACCOUNT ---")
        
        # Display available profiles
        profiles = self.profile_controller.get_active_user_profiles()
        if not profiles:
            print("✗ No active user profiles available. Please create a profile first.")
            return
        
        print("\nAvailable User Profiles:")
        for profile in profiles:
            print(f"  {profile.id}. {profile.profile_name} - {profile.description}")
        
        # Get user input
        username = input("\nUsername: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        phone_number = input("Phone Number (optional): ").strip() or None
        
        try:
            profile_id = int(input("User Profile ID: ").strip())
        except ValueError:
            print("\n✗ Invalid profile ID")
            return
        
        # Call controller
        success, message, user = self.account_controller.create_user_account(
            username, email, password, first_name, last_name, profile_id, phone_number
        )
        
        if success:
            print(f"\n✓ {message}")
            self.display_user_account(user)
        else:
            print(f"\n✗ {message}")
    
    def handle_view_user_account(self):
        """Handle viewing a user account"""
        print("\n--- VIEW USER ACCOUNT ---")
        
        try:
            user_id = int(input("Enter User Account ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        success, message, user = self.account_controller.view_user_account(user_id)
        
        if success:
            print(f"\n✓ {message}")
            self.display_user_account(user)
        else:
            print(f"\n✗ {message}")
    
    def handle_update_user_account(self):
        """Handle updating a user account"""
        print("\n--- UPDATE USER ACCOUNT ---")
        
        try:
            user_id = int(input("Enter User Account ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        # First, view current details
        success, message, user = self.account_controller.view_user_account(user_id)
        if not success:
            print(f"\n✗ {message}")
            return
        
        print("\nCurrent Details:")
        self.display_user_account(user)
        
        print("\nEnter new values (press Enter to keep current value):")
        email = input(f"Email [{user.email}]: ").strip() or None
        first_name = input(f"First Name [{user.first_name}]: ").strip() or None
        last_name = input(f"Last Name [{user.last_name}]: ").strip() or None
        phone_number = input(f"Phone [{user.phone_number}]: ").strip() or None
        
        # Show available profiles
        profiles = self.profile_controller.get_active_user_profiles()
        print("\nAvailable Profiles:")
        for profile in profiles:
            current = " (current)" if profile.id == user.user_profile_id else ""
            print(f"  {profile.id}. {profile.profile_name}{current}")
        
        profile_input = input(f"Profile ID [{user.user_profile_id}]: ").strip()
        profile_id = int(profile_input) if profile_input else None
        
        # Call controller
        success, message, updated_user = self.account_controller.update_user_account(
            user_id, email, first_name, last_name, phone_number, profile_id
        )
        
        if success:
            print(f"\n✓ {message}")
            self.display_user_account(updated_user)
        else:
            print(f"\n✗ {message}")
    
    def handle_suspend_activate_user_account(self):
        """Handle suspending or activating a user account"""
        print("\n--- SUSPEND/ACTIVATE USER ACCOUNT ---")
        
        try:
            user_id = int(input("Enter User Account ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        # View current status
        success, message, user = self.account_controller.view_user_account(user_id)
        if not success:
            print(f"\n✗ {message}")
            return
        
        status = "Active" if user.is_active else "Suspended"
        print(f"\nCurrent Status: {status}")
        
        action = input("Enter 'suspend' or 'activate': ").strip().lower()
        
        if action == "suspend":
            success, message = self.account_controller.suspend_user_account(user_id)
        elif action == "activate":
            success, message = self.account_controller.activate_user_account(user_id)
        else:
            print("\n✗ Invalid action")
            return
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def handle_search_user_accounts(self):
        """Handle searching for user accounts"""
        print("\n--- SEARCH USER ACCOUNTS ---")
        
        keyword = input("Search keyword (username/email/name) (optional): ").strip() or None
        
        # Profile filter
        profiles = self.profile_controller.get_all_user_profiles()
        print("\nFilter by Profile (optional):")
        print("  0. All profiles")
        for profile in profiles:
            print(f"  {profile.id}. {profile.profile_name}")
        
        profile_input = input("Profile ID (or Enter for all): ").strip()
        profile_id = int(profile_input) if profile_input else None
        
        # Status filter
        status_input = input("Status (active/suspended/all): ").strip().lower()
        if status_input == "active":
            is_active = True
        elif status_input == "suspended":
            is_active = False
        else:
            is_active = None
        
        # Search
        success, message, users = self.search_user_account_controller.searchUserAccount(
            keyword, profile_id, is_active
        )
        
        print(f"\n{message}")
        if users:
            self.display_user_accounts_table(users)
    
    def handle_list_all_user_accounts(self):
        """Handle listing all user accounts"""
        print("\n--- ALL USER ACCOUNTS ---")
        
        users = self.account_controller.get_all_user_accounts()
        if users:
            print(f"\nTotal: {len(users)} user account(s)")
            self.display_user_accounts_table(users)
        else:
            print("\nNo user accounts found")
    
    # ==================== USER PROFILE OPERATIONS ====================
    
    def handle_create_user_profile(self):
        """Handle creating a new user profile"""
        print("\n--- CREATE USER PROFILE ---")
        
        profile_name = input("Profile Name: ").strip()
        description = input("Description (optional): ").strip() or None
        
        result = self.create_profile_ctrl.createProfile(profile_name, description)
        
        if result == 2:  # Success
            print(f"\n✓ User profile '{profile_name}' created successfully")
        elif result == 1:  # Already exists
            print(f"\n✗ Profile '{profile_name}' already exists")
        else:  # Error
            print(f"\n✗ Error creating user profile")
    
    def handle_view_user_profile(self):
        """Handle viewing a user profile"""
        print("\n--- VIEW USER PROFILE ---")
        
        try:
            profile_id = int(input("Enter User Profile ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        result, profile = self.view_profile_ctrl.viewProfile(profile_id)
        
        if result == 1:  # Success
            print(f"\n✓ User profile retrieved successfully")
            self.display_user_profile(profile)
        else:  # Not found or error
            print(f"\n✗ User profile with ID {profile_id} not found")
    
    def handle_update_user_profile(self):
        """Handle updating a user profile"""
        print("\n--- UPDATE USER PROFILE ---")
        
        try:
            profile_id = int(input("Enter User Profile ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        # View current details
        result, profile = self.view_profile_ctrl.viewProfile(profile_id)
        if result == 0:  # Not found or error
            print(f"\n✗ User profile with ID {profile_id} not found")
            return
        
        print("\nCurrent Details:")
        self.display_user_profile(profile)
        
        print("\nEnter new values (press Enter to keep current value):")
        profile_name = input(f"Profile Name [{profile.profile_name}]: ").strip() or None
        description = input(f"Description [{profile.description}]: ").strip() or None
        
        success, message, updated_profile = self.profile_controller.update_user_profile(
            profile_id, profile_name, description
        )
        
        if success:
            print(f"\n✓ {message}")
            self.display_user_profile(updated_profile)
        else:
            print(f"\n✗ {message}")
    
    def handle_suspend_activate_user_profile(self):
        """Handle suspending or activating a user profile"""
        print("\n--- SUSPEND/ACTIVATE USER PROFILE ---")
        
        try:
            profile_id = int(input("Enter User Profile ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        # View current status
        result, profile = self.view_profile_ctrl.viewProfile(profile_id)
        if result == 0:  # Not found or error
            print(f"\n✗ User profile with ID {profile_id} not found")
            return
        
        status = "Active" if profile.is_active else "Suspended"
        print(f"\nCurrent Status: {status}")
        
        action = input("Enter 'suspend' or 'activate': ").strip().lower()
        
        if action == "suspend":
            success, message = self.profile_controller.suspend_user_profile(profile_id)
        elif action == "activate":
            success, message = self.profile_controller.activate_user_profile(profile_id)
        else:
            print("\n✗ Invalid action")
            return
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def handle_search_user_profiles(self):
        """Handle searching for user profiles"""
        print("\n--- SEARCH USER PROFILES ---")
        
        keyword = input("Search keyword (name/description) (optional): ").strip() or None
        
        status_input = input("Status (active/suspended/all): ").strip().lower()
        if status_input == "active":
            is_active = True
        elif status_input == "suspended":
            is_active = False
        else:
            is_active = None
        
        success, message, profiles = self.search_user_profile_controller.searchUserProfile(
            keyword, is_active
        )
        
        print(f"\n{message}")
        if profiles:
            self.display_user_profiles_table(profiles)
    
    def handle_list_all_user_profiles(self):
        """Handle listing all user profiles"""
        print("\n--- ALL USER PROFILES ---")
        
        profiles = self.profile_controller.get_all_user_profiles()
        if profiles:
            print(f"\nTotal: {len(profiles)} user profile(s)")
            self.display_user_profiles_table(profiles)
        else:
            print("\nNo user profiles found")
    
    # ==================== DISPLAY HELPERS ====================
    
    def display_user_account(self, user):
        """Display details of a single user account"""
        print("\n" + "-"*60)
        print(f"ID:           {user.id}")
        print(f"Username:     {user.username}")
        print(f"Email:        {user.email}")
        print(f"Name:         {user.first_name} {user.last_name}")
        print(f"Phone:        {user.phone_number or 'N/A'}")
        print(f"Profile:      {user.user_profile.profile_name}")
        print(f"Status:       {'Active' if user.is_active else 'Suspended'}")
        print(f"Created:      {user.created_at}")
        print(f"Updated:      {user.updated_at}")
        print("-"*60)
    
    def display_user_accounts_table(self, users):
        """Display multiple user accounts in table format"""
        print("\n" + "-"*120)
        print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Name':<20} {'Profile':<15} {'Status':<10}")
        print("-"*120)
        for user in users:
            status = "Active" if user.is_active else "Suspended"
            name = f"{user.first_name} {user.last_name}"
            print(f"{user.id:<5} {user.username:<15} {user.email:<25} {name:<20} {user.user_profile.profile_name:<15} {status:<10}")
        print("-"*120)
    
    def display_user_profile(self, profile):
        """Display details of a single user profile"""
        print("\n" + "-"*60)
        print(f"ID:           {profile.id}")
        print(f"Profile Name: {profile.profile_name}")
        print(f"Description:  {profile.description or 'N/A'}")
        print(f"Status:       {'Active' if profile.is_active else 'Suspended'}")
        print("-"*60)
    
    def display_user_profiles_table(self, profiles):
        """Display multiple user profiles in table format"""
        print("\n" + "-"*100)
        print(f"{'ID':<5} {'Profile Name':<20} {'Description':<50} {'Status':<10}")
        print("-"*100)
        for profile in profiles:
            status = "Active" if profile.is_active else "Suspended"
            desc = (profile.description[:47] + "...") if profile.description and len(profile.description) > 50 else (profile.description or "N/A")
            print(f"{profile.id:<5} {profile.profile_name:<20} {desc:<50} {status:<10}")
        print("-"*100)

