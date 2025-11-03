"""
CONTROLLER: CompletedHistoryCtrl
Handles searching & filtering completed match history for PIN users.

Sequence (from your diagram):
  UI.onSearchClick(serviceType?, fromDate?, toDate?) ->
    Ctrl.searchCompleted(pinID, serviceType?, fromDate?, toDate?, page?)
      -> Ctrl.validateDateRange(fromDate?, toDate?)
      -> Match.findCompletedByPinWithFilters(session, pinID, serviceType?, fromDate?, toDate?, page, page_size)
      <- items[], totalCount
    <- UI.showList(items[], totalCount, pageMeta)

Notes:
- Results are 'completed only' and should be sorted by most recent (enforced by the Entity).
- Pagination metadata is returned alongside items and totalCount.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from database.db_config import get_session
from entities.match import Match


class AuthError(Exception):
    """Raised when a user is not authorized to view the requested resource."""


class ValidationError(Exception):
    """Raised when request inputs (e.g., date range) are invalid."""


DateLike = Union[str, date, None]


class CompletedHistoryCtrl:
    """
    Controller for the 'Search & Filter Completed Match History' flow.

    Public API:
      - searchCompleted(pinID, serviceType?, fromDate?, toDate?, page?)
      - validateDateRange(fromDate?, toDate?)
    """

    def __init__(
        self,
        session=None,
        page_size: int = 10,
        auth_service: Optional[Any] = None,
    ):
        """
        :param session: DB session (defaults to database.db_config.get_session()).
        :param page_size: page size for pagination (defaults to 10).
        :param auth_service: optional service providing access checks. If supplied,
                             it should expose can_view_completed_history(pin_id) -> bool.
        """
        self.session = session or get_session()
        self.page_size = int(page_size) if page_size and page_size > 0 else 10
        self.auth_service = auth_service

    # -------------------------
    # Public API (called by UI)
    # -------------------------

    def searchCompleted(
        self,
        pinID: int,
        serviceType: Optional[str] = None,
        fromDate: DateLike = None,
        toDate: DateLike = None,
        page: int = 1,
    ) -> Tuple[List[Any], int, Dict[str, int]]:
        """
        Search/filter completed matches for a PIN.

        :returns: (items, totalCount, pageMeta)
        :raises AuthError: when access is not permitted.
        :raises ValidationError: when date range inputs are invalid.
        """
        if not self._validate_access(pinID):
            raise AuthError("Not authorised to view this PIN's completed history.")

        # Normalize and validate inputs
        page = self._sanitize_page(page)
        norm_from, norm_to = self.validateDateRange(fromDate, toDate)
        norm_type = self._sanitize_service_type(serviceType)

        # Entity call – expected to enforce:
        #   - completed-only filter
        #   - sorted by most recent
        #   - scoping by pinID
        items, total_count = Match.findCompletedByPinWithFilters(
            self.session,
            pinID,
            serviceType=norm_type,
            fromDate=norm_from,
            toDate=norm_to,
            page=page,
            page_size=self.page_size,
        )

        page_meta = self._make_page_meta(total_count, page)
        return items, total_count, page_meta

    def validateDateRange(
        self, fromDate: DateLike, toDate: DateLike
    ) -> Tuple[Optional[date], Optional[date]]:
        """
        Accepts either `date` objects or 'YYYY-MM-DD' strings (or None).
        Returns normalized (from_date, to_date).
        Raises ValidationError if start > end.
        """
        f = self._parse_date_maybe(fromDate)
        t = self._parse_date_maybe(toDate)

        if f and t and f > t:
            raise ValidationError("Start date cannot be after end date.")

        return f, t

    # -------------------------
    # Internal helpers
    # -------------------------

    def _validate_access(self, pinID: int) -> bool:
        if self.auth_service is None:
            return True
        return bool(self.auth_service.can_view_completed_history(pinID))

    def _sanitize_page(self, page: Optional[int]) -> int:
        try:
            p = int(page or 1)
        except (TypeError, ValueError):
            p = 1
        return max(1, p)

    def _sanitize_service_type(self, serviceType: Optional[str]) -> Optional[str]:
        if serviceType is None:
            return None
        s = str(serviceType).strip()
        return s or None

    def _parse_date_maybe(self, d: DateLike) -> Optional[date]:
        if d is None:
            return None
        if isinstance(d, date) and not isinstance(d, datetime):
            return d
        if isinstance(d, datetime):
            return d.date()
        # Expect plain string 'YYYY-MM-DD'
        s = str(d).strip()
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValidationError(f"Invalid date format '{s}'. Use YYYY-MM-DD.") from e

    def _make_page_meta(self, total_count: int, page: int) -> Dict[str, int]:
        size = self.page_size
        total_pages = max(1, (total_count + size - 1) // size)
        current_page = min(max(1, page), total_pages)
        return {
            "page": current_page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalCount": total_count,
            "hasPrev": 1 if current_page > 1 else 0,
            "hasNext": 1 if current_page < total_pages else 0,
            "offset": (current_page - 1) * size,
            "limit": size,
        }


# Optional: tiny demo guard (safe to remove in production)
if __name__ == "__main__":
    # Example usage; replace pinID/serviceType/dates as needed.
    ctrl = CompletedHistoryCtrl()
    try:
        items, total, meta = ctrl.searchCompleted(
            pinID=12345,
            serviceType="Food Delivery",
            fromDate="2025-01-01",
            toDate="2025-12-31",
            page=1,
        )
        print(f"items={len(items)} total={total} meta={meta}")
    except AuthError as e:
        print("AUTH ERROR:", e)
    except ValidationError as ve:
        print("VALIDATION ERROR:", ve)
