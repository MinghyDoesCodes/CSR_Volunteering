"""
BOUNDARY: PINBoundary
User interface for PIN (Person-in-Need) operations
Handles all user interactions and displays (CLI-based)
"""

from controllers.authentication_controller import AuthenticationController
from controllers.createRequestCtrl import CreateRequestCtrl
from controllers.viewRequestCtrl import ViewRequestCtrl
from controllers.updateRequestCtrl import UpdateRequestCtrl
from controllers.deleteRequestCtrl import DeleteRequestCtrl
from controllers.searchRequestCtrl import SearchRequestCtrl
from controllers.viewShortlistCountCtrl import ViewShortlistCountCtrl
from controllers.viewHistoryCtrl import ViewHistoryCtrl, AuthError


class PINBoundary:
    """
    Boundary class for PIN interface
    
    This is the user interface layer for Person-in-Need users
    to interact with request management operations.
    """
    
    def __init__(self):
        self.auth_controller = AuthenticationController()
        self.create_request_ctrl = CreateRequestCtrl()
        self.view_request_ctrl = ViewRequestCtrl()
        self.update_request_ctrl = UpdateRequestCtrl()
        self.delete_request_ctrl = DeleteRequestCtrl()
        self.search_request_ctrl = SearchRequestCtrl()
        self.view_shortlist_count_ctrl = ViewShortlistCountCtrl()
        self.view_history_ctrl = ViewHistoryCtrl()
    
    def display_menu(self):
        """Display the main menu for PIN users"""
        print("\n" + "="*60)
        print("CSR VOLUNTEERING SYSTEM - PIN DASHBOARD")
        print("="*60)
        
        if self.auth_controller.is_logged_in():
            user = self.auth_controller.get_current_user()
            print(f"Logged in as: {user.first_name} {user.last_name} ({user.username})")
            print(f"Role: {user.user_profile.profile_name}")
        
        print("\n--- REQUEST MANAGEMENT ---")
        print("1.  Login")
        print("2.  Logout")
        print("3.  Create Request")
        print("4.  View My Requests")
        print("5.  View Request Details")
        print("6.  Update Request")
        print("7.  Delete Request")
        print("8.  Search Requests")
        print("9.  View Shortlist Count")
        print("10. View Completed Match History")
        
        print("\n--- OTHER ---")
        print("0.  Exit")
        print("="*60)
    
    def run(self):
        """Main loop for the PIN interface"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_logout()
            elif choice == "3":
                self.handle_create_request()
            elif choice == "4":
                self.handle_view_my_requests()
            elif choice == "5":
                self.handle_view_request_details()
            elif choice == "6":
                self.handle_update_request()
            elif choice == "7":
                self.handle_delete_request()
            elif choice == "8":
                self.handle_search_requests()
            elif choice == "9":
                self.handle_view_shortlist_count()
            elif choice == "10":
                self.handle_view_completed_history()
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
    
    def handle_create_request(self):
        """Handle creating a new request"""
        print("\n--- CREATE REQUEST ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        title = input("Request Title: ").strip()
        description = input("Description: ").strip()
        
        user = self.auth_controller.get_current_user()
        
        result = self.create_request_ctrl.createRequest(
            userAccountID=user.id,
            title=title,
            description=description
        )
        
        if result == 0:
            print("\n✗ User does not exist")
        elif result == 1:
            print("\n✓ Request created successfully")
    
    def handle_view_my_requests(self):
        """Handle viewing all requests for the current PIN user"""
        print("\n--- MY REQUESTS ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        user = self.auth_controller.get_current_user()
        
        # Get all requests and filter by current user
        all_requests = self.view_request_ctrl.listRequests()
        my_requests = [r for r in all_requests if r.user_account_id == user.id]
        
        if my_requests:
            print(f"\nTotal: {len(my_requests)} request(s)")
            self.display_requests_table(my_requests, user.id)
        else:
            print("\nNo requests found")
    
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
        else:
            print("\n✗ Request not found")
    
    def handle_update_request(self):
        """Handle updating a request"""
        print("\n--- UPDATE REQUEST ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        try:
            request_id = int(input("Enter Request ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        request = self.view_request_ctrl.viewRequest(request_id)
        if not request:
            print("\n✗ Request not found")
            return
        
        user = self.auth_controller.get_current_user()
        if request.user_account_id != user.id:
            print("\n✗ You can only update your own requests")
            return
        
        print("\nCurrent Details:")
        self.display_request_details(request)
        
        print("\nEnter new values (press Enter to keep current value):")
        title = input(f"Title [{request.title}]: ").strip() or None
        description = input(f"Description [{request.description}]: ").strip() or None
        
        result = self.update_request_ctrl.updateRequest(
            requestID=request_id,
            title=title,
            description=description,
            status=request.status
        )
        
        if result == 0:
            print("\n✗ Request not found")
        elif result == 1:
            print("\n✓ Request updated successfully")
    
    def handle_delete_request(self):
        """Handle deleting a request"""
        print("\n--- DELETE REQUEST ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        try:
            request_id = int(input("Enter Request ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        request = self.view_request_ctrl.viewRequest(request_id)
        if not request:
            print("\n✗ Request not found")
            return
        
        user = self.auth_controller.get_current_user()
        if request.user_account_id != user.id:
            print("\n✗ You can only delete your own requests")
            return
        
        result = self.delete_request_ctrl.deleteRequest(requestID=request_id)
        
        if result == 0:
            print("\n✗ Request not found")
        elif result == 1:
            print("\n✗ Cannot delete a completed request")
        elif result == 2:
            print("\n✓ Request deleted successfully")
    
    def handle_search_requests(self):
        """Handle searching requests"""
        print("\n--- SEARCH REQUESTS ---")
        
        keyword = input("Search keyword (optional): ").strip() or None
        status = input("Status filter (optional): ").strip() or None
        
        requests = self.search_request_ctrl.searchRequests(keyword, status)
        
        print(f"\nFound: {len(requests)} request(s)")
        if requests:
            # Filter to show only current user's requests if logged in
            user = self.auth_controller.get_current_user()
            if user:
                user_requests = [r for r in requests if r.user_account_id == user.id]
                if user_requests:
                    self.display_requests_table(user_requests, user.id)
                else:
                    print("No matching requests found for your account")
            else:
                self.display_requests_table(requests, None)
        else:
            print("No requests found")
    
    def handle_view_shortlist_count(self):
        """Handle viewing shortlist count"""
        print("\n--- VIEW SHORTLIST COUNT ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        try:
            request_id = int(input("Enter Request ID: ").strip())
        except ValueError:
            print("\n✗ Invalid ID")
            return
        
        count = self.view_shortlist_count_ctrl.getShortlistCount(request_id)
        print(f"\nShortlist count: {count} time{'s' if count != 1 else ''}")
    
    def onClickHistory(self, page: int = 1, current_user=None):
        """
        Entry point for viewing completed history
        Matches BCE diagram: onClickHistory()
        Can be called from web interface or CLI
        
        Args:
            page (int): Page number to display
            current_user: Optional user object (for web interface)
            
        Returns:
            tuple: (items, total_count, page_meta) on success
            None: On error (will trigger appropriate error handling)
        """
        # For web interface, user is passed in; for CLI, get from auth_controller
        if current_user:
            user = current_user
        elif not self.auth_controller.is_logged_in():
            return None
        else:
            user = self.auth_controller.get_current_user()
        
        # Validate user is PIN
        if not user or user.user_profile.profile_name != 'PIN':
            return None
        
        try:
            # Call controller - matches BCE/Sequence diagram
            items, total_count, page_meta = self.view_history_ctrl.viewHistory(
                pinID=user.id,
                page=page
            )
            return items, total_count, page_meta, user
        except AuthError as e:
            # Error handling: return None for web, print for CLI
            if current_user is None:  # CLI mode
                print("\n" + "="*60)
                print("✗ AUTHORIZATION ERROR")
                print(f"  {str(e)}")
                print("="*60)
            return None
        except Exception as e:
            # Error handling: return None for web, print for CLI
            if current_user is None:  # CLI mode
                print(f"\n✗ Error: {str(e)}")
            return None
    
    def renderList(self, items, total_count, page_meta, current_user=None):
        """
        Prepare data for rendering the list
        Matches BCE diagram: renderList(items, totalCount, pageMeta)
        
        For web interface: Returns dict for template rendering
        For CLI: Use render_list() method instead
        """
        # This returns data structure for template rendering
        # Handles empty state implicitly (template checks total_count == 0)
        return {
            'items': items,
            'total_count': total_count,
            'page_meta': page_meta,
            'current_user': current_user
        }
    
    def handle_view_completed_history(self):
        """Handle viewing completed match history (CLI entry point)"""
        print("\n--- VIEW COMPLETED MATCH HISTORY ---")
        
        if not self.auth_controller.is_logged_in():
            print("\n✗ Please login first")
            return
        
        # Get page number
        try:
            page_input = input("Page number (Enter for page 1): ").strip()
            page = int(page_input) if page_input else 1
        except ValueError:
            print("\n✗ Invalid page number, using page 1")
            page = 1
        
        # Call onClickHistory which matches BCE diagram
        result = self.onClickHistory(page)
        
        if result:
            items, total_count, page_meta, user = result
            
            # Empty state is handled in render_list() method
            if total_count > 0:
                print(f"\n✓ Found {total_count} completed match(es)")
            self.render_list(items, total_count, page_meta)
    
    def render_list(self, items, total_count, page_meta):
        """
        Render list of completed matches (CLI display)
        This is the CLI version of renderList()
        """
        print("\n" + "="*100)
        print(f"Page {page_meta['page']} of {page_meta['totalPages']} | Total: {total_count} completed match(es)")
        print("="*100)
        
        if total_count == 0:
            # Empty state handled here for CLI
            print("No completed matches found.")
            print("You haven't received any completed assistance yet.")
            print("="*100)
            return
        
        print(f"{'Match ID':<10} {'Request Title':<30} {'Service Type':<20} {'Volunteer':<20} {'Completed At':<20}")
        print("-"*100)
        
        for item in items:
            match_id = item.match_id
            title = ""
            if item.request:
                title = item.request.title[:27] + "..." if len(item.request.title) > 30 else item.request.title
            else:
                title = "Request not found"
            
            service_type = item.service_type or "N/A"
            volunteer = ""
            if item.csr_rep:
                volunteer = f"{item.csr_rep.first_name} {item.csr_rep.last_name}"
            else:
                volunteer = "Unknown"
            
            completed = ""
            if item.completed_at:
                completed = item.completed_at.strftime('%Y-%m-%d %H:%M')
            else:
                completed = item.created_at.strftime('%Y-%m-%d %H:%M')
            
            print(f"{match_id:<10} {title:<30} {service_type:<20} {volunteer:<20} {completed:<20}")
        
        print("-"*100)
        
        # Pagination info
        if page_meta['hasPrev'] or page_meta['hasNext']:
            print("\nPagination:")
            if page_meta['hasPrev']:
                print(f"  Previous page: {page_meta['page'] - 1}")
            if page_meta['hasNext']:
                print(f"  Next page: {page_meta['page'] + 1}")
    
    # ==================== DISPLAY HELPERS ====================
    
    def display_request_details(self, request):
        """Display details of a single request"""
        print("\n" + "-"*60)
        print(f"Request ID:      {request.request_id}")
        print(f"Title:           {request.title}")
        print(f"Description:     {request.description}")
        print(f"Status:          {request.status}")
        print(f"View Count: {request.view_count} times")
        print(f"Created At:      {request.created_at}")
        print(f"Updated At:      {request.updated_at}")
        print("-"*60)
    
    def display_requests_table(self, requests, user_id):
        """Display multiple requests in table format"""
        print("\n" + "-"*120)
        print(f"{'ID':<5} {'Title':<30} {'Status':<15} {'Created At':<20}")
        print("-"*120)
        for req in requests:
            created = req.created_at.strftime('%Y-%m-%d %H:%M')
            title = req.title[:27] + "..." if len(req.title) > 30 else req.title
            print(f"{req.request_id:<5} {title:<30} {req.status:<15} {created:<20}")
        print("-"*120)

