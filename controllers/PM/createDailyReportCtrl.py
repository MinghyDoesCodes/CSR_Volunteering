"""
CONTROLLER: CreateDailyReportCtrl
Handles generation of daily reports for Platform Managers
"""
from database.db_config import get_session
from entities.request import Request
from entities.match import Match
from entities.user_account import UserAccount
from entities.shortlist import Shortlist
from entities.category import Category
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_


class CreateDailyReportCtrl:
    """
    Controller for creating daily reports
    """
    
    def __init__(self):
        self.session = get_session()
    
    def createDailyReport(self, report_date=None):
        """
        Generate a daily report for the specified date (defaults to today)
        
        Args:
            report_date (date, optional): Date for the report. Defaults to today.
            
        Returns:
            dict: Report data containing:
                - report_date: The date of the report
                - today_stats: Statistics for the report date
                - yesterday_stats: Statistics for the previous day (for comparison)
                - changes: Calculated differences
                - category_breakdown: Statistics grouped by category
        """
        if report_date is None:
            report_date = date.today()
        
        # Ensure report_date is a date object
        if isinstance(report_date, str):
            report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
        elif isinstance(report_date, datetime):
            report_date = report_date.date()
        
        # Calculate date range for the report day (start and end of day)
        start_of_day = datetime.combine(report_date, datetime.min.time())
        end_of_day = datetime.combine(report_date, datetime.max.time())
        
        # Calculate previous day for comparison
        previous_date = report_date - timedelta(days=1)
        start_of_previous = datetime.combine(previous_date, datetime.min.time())
        end_of_previous = datetime.combine(previous_date, datetime.max.time())
        
        # Get today's statistics
        today_stats = self._getDailyStats(start_of_day, end_of_day)
        
        # Get yesterday's statistics for comparison
        yesterday_stats = self._getDailyStats(start_of_previous, end_of_previous)
        
        # Calculate changes (differences)
        changes = self._calculateChanges(today_stats, yesterday_stats)
        
        # Get category breakdown
        category_breakdown = self._getCategoryBreakdown(start_of_day, end_of_day)
        
        return {
            'report_date': report_date,
            'today_stats': today_stats,
            'yesterday_stats': yesterday_stats,
            'changes': changes,
            'category_breakdown': category_breakdown
        }
    
    def _getDailyStats(self, start_datetime, end_datetime):
        """
        Get statistics for a specific date range
        
        Args:
            start_datetime: Start of the date range
            end_datetime: End of the date range
            
        Returns:
            dict: Statistics for the period
        """
        # New requests created
        new_requests = self.session.query(Request).filter(
            and_(
                Request.created_at >= start_datetime,
                Request.created_at <= end_datetime
            )
        ).count()
        
        # Requests completed (status changed to Completed)
        completed_requests = self.session.query(Request).filter(
            and_(
                Request.updated_at >= start_datetime,
                Request.updated_at <= end_datetime,
                Request.status == 'Completed'
            )
        ).count()
        
        # New matches created
        new_matches = self.session.query(Match).filter(
            and_(
                Match.created_at >= start_datetime,
                Match.created_at <= end_datetime
            )
        ).count()
        
        # Matches completed
        completed_matches = self.session.query(Match).filter(
            and_(
                Match.completed_at >= start_datetime,
                Match.completed_at <= end_datetime,
                Match.status == 'Completed'
            )
        ).count()
        
        # New shortlists created
        new_shortlists = self.session.query(Shortlist).filter(
            and_(
                Shortlist.shortlisted_at >= start_datetime,
                Shortlist.shortlisted_at <= end_datetime
            )
        ).count()
        
        # New user accounts created
        new_users = self.session.query(UserAccount).filter(
            and_(
                UserAccount.created_at >= start_datetime,
                UserAccount.created_at <= end_datetime
            )
        ).count()
        
        # Total requests (all time, for context)
        total_requests = self.session.query(Request).count()
        
        # Pending requests (current)
        pending_requests = self.session.query(Request).filter_by(status='Pending').count()
        
        return {
            'new_requests': new_requests,
            'completed_requests': completed_requests,
            'new_matches': new_matches,
            'completed_matches': completed_matches,
            'new_shortlists': new_shortlists,
            'new_users': new_users,
            'total_requests': total_requests,
            'pending_requests': pending_requests
        }
    
    def _calculateChanges(self, today_stats, yesterday_stats):
        """
        Calculate the difference between today and yesterday
        
        Args:
            today_stats: Statistics for today
            yesterday_stats: Statistics for yesterday
            
        Returns:
            dict: Changes (differences) with indicators
        """
        changes = {}
        
        for key in today_stats:
            if key in ['total_requests', 'pending_requests']:
                # These are cumulative, show absolute values
                changes[key] = {
                    'value': today_stats[key],
                    'change': None,
                    'change_percent': None,
                    'trend': None
                }
            else:
                change = today_stats[key] - yesterday_stats[key]
                change_percent = 0
                if yesterday_stats[key] > 0:
                    change_percent = (change / yesterday_stats[key]) * 100
                elif change > 0:
                    change_percent = 100  # Infinite increase from 0
                
                # Determine trend
                if change > 0:
                    trend = 'increase'
                elif change < 0:
                    trend = 'decrease'
                else:
                    trend = 'stable'
                
                changes[key] = {
                    'value': today_stats[key],
                    'change': change,
                    'change_percent': round(change_percent, 1),
                    'trend': trend
                }
        
        return changes
    
    def _getCategoryBreakdown(self, start_datetime, end_datetime):
        """
        Get statistics broken down by category
        
        Args:
            start_datetime: Start of the date range
            end_datetime: End of the date range
            
        Returns:
            list: List of dicts with category statistics
        """
        # Get all categories
        categories = self.session.query(Category).all()
        
        breakdown = []
        
        for category in categories:
            # Count new requests in this category for the day
            category_requests = self.session.query(Request).filter(
                and_(
                    Request.category_id == category.category_id,
                    Request.created_at >= start_datetime,
                    Request.created_at <= end_datetime
                )
            ).count()
            
            # Count completed requests in this category for the day
            category_completed = self.session.query(Request).filter(
                and_(
                    Request.category_id == category.category_id,
                    Request.updated_at >= start_datetime,
                    Request.updated_at <= end_datetime,
                    Request.status == 'Completed'
                )
            ).count()
            
            breakdown.append({
                'category_id': category.category_id,
                'category_title': category.title,
                'new_requests': category_requests,
                'completed_requests': category_completed,
                'is_active': category.is_active
            })
        
        # Sort by new_requests descending
        breakdown.sort(key=lambda x: x['new_requests'], reverse=True)
        
        return breakdown

