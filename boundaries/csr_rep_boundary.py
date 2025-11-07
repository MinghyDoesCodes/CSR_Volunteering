"""
BOUNDARY: CSRRepBoundary
User interface for CSR Rep operations
Handles all user interactions and displays (CLI-based)
"""

from controllers.authentication_controller import AuthenticationController
from controllers.PIN.Request.viewRequestCtrl import ViewRequestCtrl
from controllers.shortlistRequestCtrl import ShortlistRequestCtrl


class CSRRepBoundary:
    """
    Boundary class for CSR Rep interface
    
    This is the user interface layer for CSR Rep users
    to interact with volunteer operations.
    """
    
    def __init__(self):
        self.auth_controller = AuthenticationController()
        self.view_request_ctrl = ViewRequestCtrl()
        self.shortlist_request_ctrl = ShortlistRequestCtrl()
    
    def display_menu(self):
        """Display the main menu for CSR Rep users"""
        print("\n" + "="*60)
        print("CSR VOLUNTEERING SYSTEM - CSR REP DASHBOARD")
        print("="*60)
        
        if self.auth_controller.is_logged_in():
            user = self.auth_controller.get_current_user()
            print(f"Logged in as: {user.first_name} {user.last_name} ({user.username})")
            print(f"Role: {user.user_profile.profile_name}")
        
        print("\n--- VOLUNTEER OPPORTUNZY MANAGEMENT ---")
        print("1.  Login")
        print("2.  Logout")
        print("3.  Browse All Requests")
        print("4.  View Request Details")
        print("5.  Shortlist a Request")
        print("6.  View My Shortlisted Requests")
        
        print("\n--- OTHER ---")
        print("0.  Exit")
        print("="*60)
    
    def run(self):
        """Main loop for the CSR Rep interface"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_logout()
            elif choice == "3":
                self.handle_browse_requests()
            elif choice == "4":
                self.handle_view_request_details()
            elif choice == "5":
                self.handle_shortlist_request()
            elif choice == "6":
                self.handle_view_my_shortlist()
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
    
    # ==================== REQUEST OPERATIONS ====================
    
    def handle_browse_requests(self):
        """Handle browsing all requests"""
        print("\n--- BROWSE REQUESTS ---")
        
        all_requests = self.view_request_ctrl.listRequests()
        
        if all_requests:
            print(f"\nTotal: {len(all_requests)} request(s)")
            self.display_requests_table(all_requests)
        else:
            print("\nNo requests available")
    
    def handle_view_request_details(self):
        """Handle viewing a specific request"""
        print("\n--- VIEW REQUEST DETAILS ---")
        
        try:
            request_id = int(input("Enter Request ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        request = self.view_request_ctrl.viewRequest(request_id)
        
        if request:
            print("\n✓ Request retrieved successfully")
            self.display_request_details(request)
            
            # Show shortlist status
            if self.auth_controller.is_logged_in():
                user = self.auth_controller.get_current_user()
                is_shortlisted = self.shortlist_request_ctrl.isShortlisted(request_id, user.id)
                status = "Yes" if is_shortlisted else "No"
                print(f"\nShortlisted by you: {status}")
        else:
            print("\n✗ Request not found")
    
    def handle_shortlist_request(self):
        """Handle shortlisting a request"""
        print("\n--- SHORTLIST REQUEST ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        try:
            request_id = int(input("Enter Request ID to shortlist: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        # Check if request exists
        request = self.view_request_ctrl.viewRequest(request_id)
        if not request:
            print("\n✗ Request not found")
            return
        
        user = self.auth_controller.get_current_user()
        
        # Check if already shortlisted
        is_shortlisted = self.shortlist_request_ctrl.isShortlisted(request_id, user.id)
        if is_shortlisted:
            print("\n✗ Request already in your shortlist")
            return
        
        success, message = self.shortlist_request_ctrl.shortlistRequest(request_id, user.id)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def handle_view_my_shortlist(self):
        """Handle viewing CSR Rep's shortlisted requests"""
        print("\n--- MY SHORTLISTED REQUESTS ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        user = self.auth_controller.get_current_user()
        
        # Get all shortlists for this CSR Rep
        from entities.shortlist import Shortlist
        from database.db_config import get_session
        
        session = get_session()
        shortlists = session.query(Shortlist).filter_by(csr_rep_id=user.id).all()
        
        if shortlists:
            print(f"\nTotal: {len(shortlists)} shortlisted request(s)")
            for shortlist in shortlists:
                request = self.view_request_ctrl.viewRequest(shortlist.request_id)
                if request:
                    print(f"\nRequest ID {request.request_id}: {request.title}")
                    print(f"  Status: {request.status}")
                    print(f"  Shortlisted at: {shortlist.shortlisted_at}")
        else:
            print("\nNo shortlisted requests")
    
    # ==================== DISPLAY HELPERS ====================
    
    def display_request_details(self, request):
        """Display details of a single request"""
        print("\n" + "-"*60)
        print(f"Request ID:      {request.request_id}")
        print(f"Title:           {request.title}")
        print(f"Description:     {request.description}")
        print(f"Status:          {request.status}")
        if request.pin:
            print(f"Requested By:    {request.pin.first_name} {request.pin.last_name}")
        print(f"Created At:      {request.created_at}")
        print("-"*60)
    
    def display_requests_table(self, requests):
        """Display multiple requests in table format"""
        print("\n" + "-"*120)
        print(f"{'ID':<5} {'Title':<30} {'Status':<15} {'Requested By':<20} {'Created At':<20}")
        print("-"*120)
        for req in requests:
            created = req.created_at.strftime('%Y-%m-%d %H:%M')
            title = req.title[:27] + "..." if len(req.title) > 30 else req.title
            requested_by = ""
            if req.pin:
                requested_by = f"{req.pin.first_name} {req.pin.last_name}"
            print(f"{req.request_id:<5} {title:<30} {req.status:<15} {requested_by:<20} {created:<20}")
        print("-"*120)

