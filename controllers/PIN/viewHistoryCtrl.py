"""
CONTROLLER: ViewHistoryCtrl
Handles viewing completed match history for PIN users
"""

from typing import Any, Dict, List, Optional, Tuple
from database.db_config import get_session
from entities.match import Match


class AuthError(Exception):
    """Raised when a user is not authorized to view the requested resource."""

class ViewHistoryCtrl:
    """
    Controller for the 'Completed Match History' flow.

    Sequence (from your diagram):
      UI.onClickHistory() -> Ctrl.viewHistory(pinID, page)
        -> Ctrl.validateAccess(pinID)
        -> Match.findCompletedByPin(pinID, page)
        <- items[], totalCount
      <- UI.renderList(items[], totalCount, pageMeta)

    Notes:
    - Results are 'completed only' and should be sorted by most recent.
    - Pagination metadata is returned alongside items and totalCount.
    """

    def __init__(
        self,
        session=None,
        page_size: int = 10,
        auth_service: Optional[Any] = None,
    ):
        """
        :param session: DB session (defaults to database.db_config.get_session()).
        :param page_size: page size for pagination.
        :param auth_service: optional service providing access checks. If supplied,
                             it should expose can_view_completed_history(pin_id) -> bool.
        """
        self.session = session or get_session()
        self.page_size = int(page_size) if page_size and page_size > 0 else 10
        self.auth_service = auth_service

    # -------------------------
    # Public API (called by UI)
    # -------------------------

    def viewHistory(self, pinID: int, page: int = 1) -> Tuple[List[Any], int, Dict[str, int]]:
        """
        Main entry point used by the boundary/UI.

        :returns: (items, totalCount, pageMeta)
        :raises AuthError: when access is not permitted.
        """
        if not self.validateAccess(pinID):
            # UI may catch this and call showAuthError()
            raise AuthError("Not authorised to view this PIN's completed history.")

        page = self._sanitize_page(page)

        # Entity call – expected to enforce:
        #   - completed-only filter
        #   - sorted by most recent
        # Implement findCompletedByPin(session, pin_id, page, page_size) in entities.match.Match
        items, total_count = Match.findCompletedByPin(
            self.session, pinID, page=page, page_size=self.page_size
        )

        page_meta = self._make_page_meta(total_count, page)

        # (Optional) UI may showEmptyState() if total_count == 0
        return items, total_count, page_meta

    def validateAccess(self, pinID: int) -> bool:
        """
        Access control hook (shown in your sequence diagram).

        Default behaviour allows access; inject an auth_service to enforce rules.
        """
        if self.auth_service is None:
            return True
        return bool(self.auth_service.can_view_completed_history(pinID))

    # -------------------------
    # Helpers
    # -------------------------

    def _sanitize_page(self, page: Optional[int]) -> int:
        try:
            p = int(page or 1)
        except (TypeError, ValueError):
            p = 1
        return max(1, p)

    def _make_page_meta(self, total_count: int, page: int) -> Dict[str, int]:
        size = self.page_size
        total_pages = max(1, (total_count + size - 1) // size)
        # If requested page > total_pages, clamp to the last page in metadata
        current_page = min(page, total_pages)
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
    ctrl = ViewHistoryCtrl()
    try:
        items, total, meta = ctrl.viewHistory(pinID=12345, page=1)
        print(f"items={len(items)} total={total} meta={meta}")
    except AuthError as e:
        print("AUTH ERROR:", e)