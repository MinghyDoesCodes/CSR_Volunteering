"""
CONTROLLER: CreateWeeklyReportCtrl
Generates weekly reports for Platform Managers
"""

from datetime import date, datetime, timedelta

from controllers.PM.createDailyReportCtrl import CreateDailyReportCtrl


class CreateWeeklyReportCtrl(CreateDailyReportCtrl):
    """Controller for creating weekly reports"""

    def createWeeklyReport(self, anchor_date: date | str | None = None):
        """Generate a weekly report ending on the specified week.

        Args:
            anchor_date: Any date within the target week. Defaults to today.

        Returns:
            dict: Weekly report payload containing current week stats, previous
            week stats, deltas, and category breakdown.
        """

        if anchor_date is None:
            anchor_date = date.today()

        if isinstance(anchor_date, str):
            anchor_date = datetime.strptime(anchor_date, "%Y-%m-%d").date()
        elif isinstance(anchor_date, datetime):
            anchor_date = anchor_date.date()

        # ISO weekday: Monday = 0, Sunday = 6
        start_of_week = anchor_date - timedelta(days=anchor_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        start_datetime = datetime.combine(start_of_week, datetime.min.time())
        end_datetime = datetime.combine(end_of_week, datetime.max.time())

        previous_start = start_of_week - timedelta(days=7)
        previous_end = start_of_week - timedelta(days=1)

        prev_start_dt = datetime.combine(previous_start, datetime.min.time())
        prev_end_dt = datetime.combine(previous_end, datetime.max.time())

        current_stats = self._getDailyStats(start_datetime, end_datetime)
        previous_stats = self._getDailyStats(prev_start_dt, prev_end_dt)
        changes = self._calculateChanges(current_stats, previous_stats)
        category_breakdown = self._getCategoryBreakdown(start_datetime, end_datetime)

        return {
            "report_date": anchor_date,
            "week_start": start_of_week,
            "week_end": end_of_week,
            "current_stats": current_stats,
            "previous_stats": previous_stats,
            "changes": changes,
            "category_breakdown": category_breakdown,
        }

