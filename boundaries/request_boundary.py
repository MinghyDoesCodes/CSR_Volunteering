from flask import render_template, request, redirect, url_for, flash
from database.db_config import close_session
from controllers.authentication_controller import AuthenticationController
from controllers.PIN.Request.createRequestCtrl import CreateRequestCtrl
from controllers.PIN.Request.viewRequestCtrl import ViewRequestCtrl
from controllers.PIN.Request.updateRequestCtrl import UpdateRequestCtrl
from controllers.PIN.Request.deleteRequestCtrl import DeleteRequestCtrl
from controllers.PIN.Request.searchRequestCtrl import SearchRequestCtrl
from controllers.PIN.viewShortlistCountCtrl import ViewShortlistCountCtrl
from controllers.PIN.viewHistoryCtrl import ViewHistoryCtrl
from controllers.PIN.completedHistoryCtrl import CompletedHistoryCtrl
from controllers.CSR.shortlistRequestCtrl import ShortlistRequestCtrl
from controllers.CSR.searchShortlistCtrl import searchShortlistCtrl
from controllers.CSR.CSR_viewHistoryCtrl import CSRViewHistoryCtrl
from controllers.CSR.CSR_completedHistoryCtrl import CSRCompletedHistoryCtrl, ValidationError
from controllers.Category.viewCategoryCtrl import ViewCategoryCtrl

class ListRequestUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = ViewRequestCtrl()
        self.v = ViewShortlistCountCtrl()
        self.s = ShortlistRequestCtrl()

    def DisplayPage(self):
        current_user = self.a.get_current_user()
        print("User:", current_user)
        user_profile_name = current_user.user_profile.profile_name if current_user else None

        # Get requests based on user role
        if user_profile_name == 'PIN':
            # PIN users only see requests they created
            all_requests = self.c.listRequests()
            requests = [req for req in all_requests if req.user_account_id == current_user.id]
        else:
            # CSR Reps see all requests
            requests = self.c.listRequests()

        # Get shortlist counts for PIN users
        shortlist_counts = {}
        csr_shortlisted = {}

        if user_profile_name == 'PIN':
            shortlist_counts = self.v.getShortlistCountsForUser(current_user.id)
        elif user_profile_name == 'CSR Rep':
            # Get CSR Rep's shortlist status for each request
            for req in requests:
                csr_shortlisted[req.request_id] = self.s.isShortlisted(req.request_id, current_user.id)
        
        # Pass user profile for template logic
        user_profile = user_profile_name

        render = render_template('requests/list.html', 
                               requests=requests,
                               shortlist_counts=shortlist_counts,
                               csr_shortlisted=csr_shortlisted,
                               user_profile=user_profile)
        close_session()
        return render
    
class CreateRequestUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = CreateRequestCtrl()
        self.v = ViewCategoryCtrl()

    def createRequest(self, request):
        if request.method == 'POST':
            user_account_id = self.a.get_current_user().id
            title = request.form.get('request_title')
            description = request.form.get('request_description')
            category_id = request.form.get('category_id')
            
            result = self.c.createRequest(
                userAccountID=user_account_id,
                title=title,
                description=description,
                categoryID=category_id
            )
            close_session()
            if result == 0:
                flash("User does not exist", 'error')
            elif result == 1:
                flash("Request created successfully", 'success')
                return redirect(url_for('listRequests'))
        
        # Get categories for dropdown
        categories = self.v.listActiveCategories()
        close_session()
        return render_template('requests/create.html', categories=categories)
    
class ViewRequestUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = ViewRequestCtrl()
        self.s = ShortlistRequestCtrl()
        self.v = ViewShortlistCountCtrl()

    def viewRequest(self, request_id):
        request_obj = self.c.viewRequest(request_id)
        if not request_obj:
            flash(f"Request with ID {request_id} not found", 'error')
            return redirect(url_for('listRequests'))
        
        # Check if current user is CSR Rep and has shortlisted this request
        current_user = self.a.get_current_user()
        is_shortlisted = False
        shortlist_count = 0

        if current_user and current_user.user_profile.profile_name == 'CSR Rep':
            is_shortlisted = self.s.isShortlisted(request_id, current_user.id)
        elif current_user and current_user.user_profile.profile_name == 'PIN':
            # Get shortlist count for PIN users
            shortlist_count = self.v.getShortlistCount(request_id)

        render = render_template('requests/view.html',
                        request=request_obj,
                        current_user=current_user,
                        is_shortlisted=is_shortlisted,
                        shortlist_count=shortlist_count)
        
        close_session()
        return render
    
class UpdateRequestUI:
    def __init__(self):
        self.c = UpdateRequestCtrl()
        self.v = ViewRequestCtrl()
        self.vc = ViewCategoryCtrl()

    def onClick(self, request_id):
        if request.method == 'POST':
            title = request.form.get('request_title')
            description = request.form.get('request_description')
            category_id = request.form.get('category_id')
            status = request.form.get('request_status')

            result = self.c.updateRequest(
                requestID=request_id,
                title=title if title else None,
                categoryID=int(category_id) if category_id else None,
                description=description if description else None,
                status=status if status else None
            )
            if result == 0:
                flash(f"Request with ID {request_id} not found", 'error')
            elif result == 1:
                flash("Request updated successfully", 'success')
                return redirect(url_for('viewRequest', request_id=request_id))
        
        # Get request details
        request_obj = self.v.viewRequest(request_id)
        if not request_obj:  # Not found
            flash(f"Request with ID {request_id} not found", 'error')
            return redirect(url_for('listRequests'))
        
        # Get categories for dropdown
        categories = self.vc.listActiveCategories()
        
        render = render_template('requests/edit.html',
                    request=request_obj, categories=categories)
        close_session()
        return render
    
class DeleteRequestUI:
    def __init__(self):
        self.c = DeleteRequestCtrl()

    def onClick(self, request_id):
        result = self.c.deleteRequest(request_id)
        close_session()
        if result == 0:
            flash(f"Request with ID {request_id} not found", 'error')
        elif result == 1:
            flash("Cannot delete a completed request", 'error')
            return redirect(url_for('listRequests'))
        elif result == 2:
            flash("Request deleted successfully", 'success')
            return redirect(url_for('listRequests'))
        
class SearchRequestUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = SearchRequestCtrl()

    def onClick(self):
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')
    
        current_user = self.a.get_current_user()
        user_profile = current_user.user_profile.profile_name if current_user else None

        if user_profile == 'PIN':
            # PIN users only search their own requests
            all_requests = self.c.searchRequests(keyword or None, status)
            requests = [req for req in all_requests if req.user_account_id == current_user.id]
        else:
            # CSR Reps search all requests
            requests = self.c.searchRequests(keyword or None, status)
        
        render = render_template('requests/search.html', 
                            requests=requests,
                            keyword=keyword,
                            status=status,
                            user_profile=user_profile)
        
        close_session()
        return render
    
# PIN User View Completed History
class ViewCompletedHistoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = ViewHistoryCtrl()
        self.cat = ViewCategoryCtrl()

    def onClickHistory(self):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'PIN':
            flash("Only PIN Users can view completed match history.", 'error')
            return redirect(url_for('dashboard'))
        
        page = request.args.get('page', 1, type=int)

        items, total_count, page_meta = self.c.viewHistory(current_user.id, page)
        print ("Items: ", items)

        categories = self.cat.listCategories()
        service_types = [cat.title for cat in categories] if categories else []

        render = render_template(
                    'completed_history/list.html',
                    items=items,
                    total_count=total_count,
                    page_meta=page_meta,
                    user = current_user,
                    service_types = service_types
        )
        close_session()
        return render
    
# PIN User Search and filter Completed History
class CompletedHistoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = CompletedHistoryCtrl()
        self.cat = ViewCategoryCtrl()

    def onSearchClick(self):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'PIN':
            flash("Only PIN users can view completed match history.", 'error')
            return redirect(url_for('dashboard'))
        
        # Get filter parameters from query string
        service_type = request.args.get('serviceType', '').strip() or None
        from_date = request.args.get('from', '').strip() or None
        to_date = request.args.get('to', '').strip() or None
        page = request.args.get('page', 1, type=int)

        items, total_count, page_meta = self.c.searchCompleted(
            current_user.id,
            service_type,
            from_date,
            to_date,
            page
        )
        filters = {
            'serviceType': service_type,
            'from': from_date,
            'to': to_date
        }
        categories = self.cat.listCategories()
        service_types = [cat.title for cat in categories] if categories else []
        render = render_template(
                    'completed_history/list.html',
                    items=items,
                    total_count=total_count,
                    page_meta=page_meta,
                    user = current_user,
                    service_types = service_types,
                    filters = filters,
        )
        close_session()
        return render

# CSR Rep Shortlist Request
class CSRRepBoundary:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = ViewRequestCtrl()
        self.s = ShortlistRequestCtrl()

    def handle_shortlist_request_web(self, request_id):
        """Handle shortlisting from web interface"""
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can shortlist requests.", 'error')

        request = self.c.viewRequest(request_id)
        if not request:
            flash(f"Request with ID {request_id} not found.", 'error')
            return redirect(url_for('listRequests'))
        
        result = self.s.shortlistRequest(request_id, current_user.id)
        close_session()

        if result == 1:
            flash("Request is already shortlisted.", 'info')
        elif result == 2:
            flash("Request added to shortlist successfully.", 'success')
            return redirect(url_for('viewRequest', request_id=request_id))
        
    def removeShortlist(self, request_id):
        """Handle removing shortlist from web interface"""
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can remove shortlists.", 'error')

        request = self.c.viewRequest(request_id)
        if not request:
            flash(f"Request with ID {request_id} not found.", 'error')
            return redirect(url_for('listRequests'))
        
        result = self.s.removeShortlist(request_id, current_user.id)
        close_session()

        if result == 1:
            flash("Request is not in your shortlist.", 'info')
        elif result == 2:
            flash("Request removed from shortlist successfully.", 'success')
            return redirect(url_for('viewRequest', request_id=request_id))
        
# CSR Rep Search and filter Shortlist
class SearchShortlistUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = searchShortlistCtrl()
        self.cat = ViewCategoryCtrl()

    def searchShortlists(self):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can search their shortlist.", 'error')
            return redirect(url_for('dashboard'))
        
        keyword = request.args.get('keyword', '').strip()
        categoryID = request.args.get('category_id', '').strip()
        shortlist = self.c.searchShortlist(current_user.id, keyword, categoryID)
        print("Requests: ", shortlist)

        categories = self.cat.listCategories()        
        render = render_template(
                    'shortlist.html', 
                    requests=shortlist,
                    keyword=keyword,
                    categories=categories
                )
        close_session()
        return render
    
#CSR Rep View Complete History
class ListCompletedHistoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = CSRViewHistoryCtrl()

    def displayPage(self):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can view completed match history.", 'error')
            return redirect(url_for('dashboard'))
        
        page = request.args.get('page', 1, type=int)
        items, total_count, page_meta = self.c.viewHistory(current_user.id, page)
        service_types = self.c.getServiceTypes(current_user.id)

        render = render_template(
                    'completed_history/csr_list.html',
                    items=items,
                    total_count=total_count,
                    page_meta=page_meta,
                    service_types = service_types,
                    filters = None
        )
        close_session()
        return render
        

#CSR Rep Search and filter Completed History
class CSRCompletedHistoryUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.cs = CSRViewHistoryCtrl()
        self.c = CSRCompletedHistoryCtrl()

    def onClickHistory(self):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can view completed match history.", 'error')
            return redirect(url_for('dashboard'))
        
        # Get filter parameters from query string
        service_type = request.args.get('serviceType', '').strip() or None
        from_date = request.args.get('from', '').strip() or None
        to_date = request.args.get('to', '').strip() or None
        page = request.args.get('page', 1, type=int)

        try:
            items, total_count, page_meta = self.c.searchCompleted(
                current_user.id,
                service_type,
                from_date,
                to_date,
                page
            )
        except (ValidationError) as e:
            flash(str(e), 'error')
            return redirect(url_for('csrViewCompletedHistory'))
        
        # To populate service type filter dropdown
        service_types = self.cs.getServiceTypes(current_user.id)
        render = render_template(
                    'completed_history/csr_list.html',
                    items=items,
                    total_count=total_count,
                    page_meta=page_meta,
                    service_types = service_types,
                    filters = {'serviceType': service_type, 'from': from_date, 'to': to_date}
        )
        close_session()
        return render

#CSR Rep View Details of Completed Services
class ViewCompletedDetailsUI:
    def __init__(self):
        self.a = AuthenticationController()
        self.c = CSRViewHistoryCtrl()

    def viewDetails(self, match_id):
        current_user = self.a.get_current_user()
        if not current_user or current_user.user_profile.profile_name != 'CSR Rep':
            flash("Only CSR Reps can view completed match history.", 'error')
            return redirect(url_for('dashboard'))
        
        m = self.c.viewDetails(current_user.id, match_id)
        if m == 0:
            flash("Not authorised to view this CSR's completed services.", 'error')
            return redirect(url_for('dashboard'))
        elif m == 1:
            flash(f"Completed match with ID {match_id} not found.", 'error')
            return redirect(url_for('csrViewCompletedHistory'))
        elif m == 2:
            flash("You are not authorised to view this completed service.", 'error')
            return redirect(url_for('csrViewCompletedHistory'))
        elif m == 3:
            flash("This service is not completed yet.", 'error')
            return redirect(url_for('csrViewCompletedHistory'))

        render = render_template(
                    'completed_history/details.html',
                    m=m
        )
        close_session()
        return render