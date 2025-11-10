"""
ENTITY: Match
Represents a match between a PIN's request and a CSR Rep volunteer
"""

from datetime import datetime, time, date
from typing import Optional, List, Tuple

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, desc
from sqlalchemy.orm import relationship, joinedload
from database.db_config import Base
from entities.request import Request


class Match(Base):
    """
    Entity class for Match

    Represents a completed volunteer service match between:
    - A PIN's request
    - A CSR Rep volunteer
    """
    __tablename__ = "matches"

    # Primary key
    match_id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    request_id = Column(Integer, ForeignKey("requests.request_id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)
    csr_rep_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)

    # Match details
    status = Column(String(50), default="Pending", nullable=False)  # Pending, In Progress, Completed, Cancelled
    service_type = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    request = relationship("Request", back_populates="matches")
    pin = relationship("UserAccount", foreign_keys=[pin_id], back_populates="matches_as_pin")
    csr_rep = relationship("UserAccount", foreign_keys=[csr_rep_id], back_populates="matches_as_csr")

    def __repr__(self):
        return f"<Match(id={self.match_id}, request={self.request_id}, status='{self.status}')>"

    # ---------------- PIN QUERIES ----------------

    @classmethod
    def _base_completed_query(cls, session, pin_id: int):
        return (
            session.query(cls)
            .filter(cls.pin_id == int(pin_id), cls.status == "Completed")
        )

    @classmethod
    def findCompletedByPin(
        cls, session, pin_id: int, page: int = 1, page_size: int = 10
    ) -> Tuple[List["Match"], int]:
        """
        Return (items, total_count) for completed matches belonging to pin_id,
        sorted by most recent first, paginated.
        """
        query = cls._base_completed_query(session, pin_id)
        total_count = query.count()

        query = query.order_by(
            desc(cls.completed_at).nullslast(),
            desc(cls.created_at),
        )

        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count

    @classmethod
    def findCompletedByPinWithFilters(
        cls,
        session,
        pinID: int,
        serviceType: Optional[str] = None,
        categoryID: Optional[int] = None,
        fromDate: Optional[date] = None,
        toDate: Optional[date] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List["Match"], int]:
        """
        Completed matches for a PIN with optional filters and pagination.
        """
        query = (
            session.query(cls)
            .join(cls.request)
            .options(joinedload(cls.request))
            .filter(cls.pin_id == int(pinID), cls.status == "Completed")
        )

        if serviceType and str(serviceType).strip():
            query = query.filter(cls.service_type == str(serviceType).strip())

        if categoryID is not None:
            query = query.filter(Request.category_id == int(categoryID))

        if fromDate:
            query = query.filter(cls.completed_at >= datetime.combine(fromDate, time.min))
        if toDate:
            query = query.filter(cls.completed_at <= datetime.combine(toDate, time.max))

        total_count = query.count()
        query = query.order_by(desc(cls.completed_at).nullslast(), desc(cls.created_at))

        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count

    # ---------------- CSR QUERIES ----------------

    @classmethod
    def _base_completed_query_for_csr(cls, session, csr_rep_id: int):
        return (
            session.query(cls)
            .options(
                joinedload(cls.request),
                joinedload(cls.pin),
                joinedload(cls.csr_rep),
            )
            .filter(cls.csr_rep_id == int(csr_rep_id), cls.status == "Completed")
        )

    @classmethod
    def findCompletedByCSR(
        cls,
        session,
        csr_rep_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List["Match"], int]:
        query = cls._base_completed_query_for_csr(session, csr_rep_id)
        total_count = query.count()
        query = query.order_by(desc(cls.completed_at).nullslast(), desc(cls.created_at))
        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count

    @classmethod
    def findCompletedByCSRWithFilters(
        cls,
        session,
        csrRepID: int,
        serviceType: Optional[str] = None,
        fromDate: Optional[date] = None,
        toDate: Optional[date] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List["Match"], int]:
        query = cls._base_completed_query_for_csr(session, csrRepID)

        if serviceType and str(serviceType).strip():
            query = query.filter(cls.service_type == str(serviceType).strip())

        if fromDate:
            query = query.filter(cls.completed_at >= datetime.combine(fromDate, time.min))
        if toDate:
            query = query.filter(cls.completed_at <= datetime.combine(toDate, time.max))

        total_count = query.count()
        query = query.order_by(desc(cls.completed_at).nullslast(), desc(cls.created_at))
        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count

    @classmethod
    def findById(cls, session, match_id: int):
        """
        Fetch a single match by ID with relationships eagerly loaded,
        so your template doesn't trigger a thousand lazy-loads.
        """
        return (
            session.query(cls)
            .options(
                joinedload(cls.request),
                joinedload(cls.pin),
                joinedload(cls.csr_rep),
            )
            .filter(cls.match_id == int(match_id))
            .first()
        )