"""
CONTROLLER: CompletedHistoryCtrl
CSR Rep - search & filter completed services by service type and/or date range
"""

from __future__ import annotations
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from database.db_config import get_session
from entities.match import Match


class AuthError(Exception):
    pass


class ValidationError(Exception):
    pass


DateLike = Union[str, date, datetime, None]


class CSRCompletedHistoryCtrl:
    """
    Public API:
      - searchCompleted(csrRepID, serviceType?, fromDate?, toDate?, page?)
        -> (items, total_count, page_meta)
    """

    def __init__(self, session=None, page_size: int = 10, auth_service: Optional[Any] = None):
        self.session = session or get_session()
        self.page_size = int(page_size) if page_size and page_size > 0 else 10
        self.auth_service = auth_service

    def searchCompleted(
        self,
        csrRepID: int,
        serviceType: Optional[str] = None,
        fromDate: DateLike = None,
        toDate: DateLike = None,
        page: int = 1,
    ) -> Tuple[List[Any], int, Dict[str, int]]:
        if not self._validate_access(csrRepID):
            raise AuthError("Not authorised to view this CSR's completed services.")

        page = self._sanitize_page(page)
        norm_from, norm_to = self._validate_date_range(fromDate, toDate)
        norm_type = self._sanitize_service_type(serviceType)

        items, total_count = Match.findCompletedByCSRWithFilters(
            self.session,
            csrRepID=csrRepID,
            serviceType=norm_type,
            fromDate=norm_from,
            toDate=norm_to,
            page=page,
            page_size=self.page_size,
        )
        page_meta = self._make_page_meta(total_count, page)
        return items, total_count, page_meta

    # ----------------- helpers -----------------

    def _validate_access(self, csrRepID: int) -> bool:
        if self.auth_service is None:
            return True
        return bool(self.auth_service.can_view_completed_history_for_csr(csrRepID))

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

    def _parse_date(self, d: DateLike) -> Optional[date]:
        if d is None:
            return None
        if isinstance(d, datetime):
            return d.date()
        if isinstance(d, date):
            return d
        s = str(d).strip()
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValidationError(f"Invalid date format '{s}'. Use YYYY-MM-DD.") from e

    def _validate_date_range(self, fromDate: DateLike, toDate: DateLike) -> Tuple[Optional[date], Optional[date]]:
        f = self._parse_date(fromDate)
        t = self._parse_date(toDate)
        if f and t and f > t:
            raise ValidationError("Start date cannot be after end date.")
        return f, t

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
