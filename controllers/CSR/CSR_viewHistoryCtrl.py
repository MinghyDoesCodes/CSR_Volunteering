"""
CONTROLLER: ViewHistoryCtrl
CSR Rep - view completed services list and a specific completed service
"""

from typing import Any, Dict, List, Optional, Tuple
from database.db_config import get_session
from entities.match import Match

class CSRViewHistoryCtrl:
    """
    Public API:
      - viewHistory(csrRepID, page=1)  -> (items, total_count, page_meta)
      - viewDetails(csrRepID, matchID) -> Match
    """

    def __init__(self, session=None, page_size: int = 10, auth_service: Optional[Any] = None):
        self.session = session or get_session()
        self.page_size = int(page_size) if page_size and page_size > 0 else 10
        self.auth_service = auth_service

    # -------------------------
    # Public API
    # -------------------------

    def viewHistory(self, csrRepID: int, page: int = 1) -> Tuple[List[Any], int, Dict[str, int]]:
        page = self._sanitize_page(page)
        items, total_count = Match.findCompletedByCSR(
            self.session,
            csr_rep_id=int(csrRepID),
            page=page,
            page_size=self.page_size,
        )
        page_meta = self._make_page_meta(total_count, page)
        return items, total_count, page_meta
    
    def getServiceTypes(self, csrRepID: int) -> List[str]:
        return Match.getServiceTypes(self.session, csrRepID)

    def viewDetails(self, csrRepID: int, matchID: int):
        if not self._validate_access(csrRepID):
            return 0 # Unauthorized
        m = Match.findById(self.session, int(matchID))
        if not m:
            return 1 # Not found
        elif m.csr_rep_id != int(csrRepID):
            return 2 # Unauthorized
        elif m.status != "Completed":
            return 3 # Not completed
        return m

    # -------------------------
    # Helpers
    # -------------------------

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
