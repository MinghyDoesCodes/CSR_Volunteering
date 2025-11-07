from flask import render_template, request, redirect, url_for, flash
from database.db_config import close_session
from controllers.authentication_controller import AuthenticationController
from controllers.PIN.Request.createRequestCtrl import CreateRequestCtrl
from controllers.PIN.Request.viewRequestCtrl import ViewRequestCtrl
from controllers.PIN.Request.updateRequestCtrl import UpdateRequestCtrl
from controllers.PIN.Request.deleteRequestCtrl import DeleteRequestCtrl
from controllers.PIN.Request.searchRequestCtrl import SearchRequestCtrl
from controllers.PIN.viewShortlistCountCtrl import ViewShortlistCountCtrl
from controllers.shortlistRequestCtrl import ShortlistRequestCtrl
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
    
        current_user = self.a.get_current_user()
        user_profile = current_user.user_profile.profile_name if current_user else None
        
        requests = self.c.searchRequests(keyword or None, None)
        render = render_template('requests/search.html', 
                            requests=requests,
                            keyword=keyword,
                            user_profile=user_profile)
        
        close_session()
        return render