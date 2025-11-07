"""
CONTROLLER: CreateMonthlyReportCtrl
Generates monthly reports for Platform Managers
"""

from datetime import date, datetime, timedelta

from controllers.createDailyReportCtrl import CreateDailyReportCtrl


class CreateMonthlyReportCtrl(CreateDailyReportCtrl):
    """Controller for creating monthly reports"""

    def createMonthlyReport(self, anchor_date: date | str | None = None):
        """Generate a monthly report for the month containing anchor_date."""

        if anchor_date is None:
            anchor_date = date.today()

        if isinstance(anchor_date, str):
            try:
                anchor_date = datetime.strptime(anchor_date, "%Y-%m-%d").date()
            except ValueError:
                anchor_date = datetime.strptime(f"{anchor_date}-01", "%Y-%m-%d").date()
        elif isinstance(anchor_date, datetime):
            anchor_date = anchor_date.date()

        first_of_month = anchor_date.replace(day=1)
        # compute last day by moving to next month and subtracting a day
        if first_of_month.month == 12:
            next_month = first_of_month.replace(year=first_of_month.year + 1, month=1, day=1)
        else:
            next_month = first_of_month.replace(month=first_of_month.month + 1, day=1)

        last_of_month = next_month - timedelta(days=1)

        start_datetime = datetime.combine(first_of_month, datetime.min.time())
        end_datetime = datetime.combine(last_of_month, datetime.max.time())

        # previous month range
        prev_last = first_of_month - timedelta(days=1)
        prev_first = prev_last.replace(day=1)
        prev_start_dt = datetime.combine(prev_first, datetime.min.time())
        prev_end_dt = datetime.combine(prev_last, datetime.max.time())

        current_stats = self._getDailyStats(start_datetime, end_datetime)
        previous_stats = self._getDailyStats(prev_start_dt, prev_end_dt)
        changes = self._calculateChanges(current_stats, previous_stats)
        category_breakdown = self._getCategoryBreakdown(start_datetime, end_datetime)

        return {
            "report_date": anchor_date,
            "month_start": first_of_month,
            "month_end": last_of_month,
            "current_stats": current_stats,
            "previous_stats": previous_stats,
            "changes": changes,
            "category_breakdown": category_breakdown,
        }

