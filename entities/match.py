"""
ENTITY: Match
Represents a match between a PIN's request and a CSR Rep volunteer
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, time, date
from database.db_config import Base
from sqlalchemy import desc, nullslast, and_
from typing import Optional, List, Tuple



class Match(Base):
    """
    Entity class for Match
    
    Represents a completed volunteer service match between:
    - A PIN's request
    - A CSR Rep volunteer
    """
    __tablename__ = 'matches'
    
    # Primary key
    match_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys
    request_id = Column(Integer, ForeignKey('requests.request_id'), nullable=False)
    pin_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    csr_rep_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    
    # Match details
    status = Column(String(50), default='Pending', nullable=False)  # Pending, In Progress, Completed, Cancelled
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
        """String representation for debugging"""
        return f"<Match(id={self.match_id}, request={self.request_id}, status='{self.status}')>"
    
    @classmethod
    def findById(cls, session, match_id):
        """Find a match by its ID"""
        return session.query(cls).filter_by(match_id=match_id).first()
    
    @classmethod
    def findCompletedByPin(cls, session, pin_id: int, page: int = 1, page_size: int = 10):
        """
        Return (items, total_count) for completed matches belonging to pin_id,
        sorted by most recent first, paginated.
        """
        query = cls._base_completed_query(session, pin_id)

        total_count = query.count()

        query = query.order_by(
            nullslast(desc(cls.completed_at)),
            desc(cls.created_at)
    )

        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count

    
    @classmethod
    def getAllMatches(cls, session):
        """Get all matches"""
        return session.query(cls).all()
    
    @classmethod
    def _base_completed_query(cls, session, pin_id: int):
        return (
            session.query(cls)
            .filter(
                cls.pin_id == pin_id,
                cls.status == 'Completed'
        )
    )

    @classmethod
    def findCompletedByPinWithFilters(
        cls,
        session,
        pinID: int,
        serviceType: Optional[str] = None,
        fromDate: Optional[date] = None,
        toDate: Optional[date]= None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List["Match"], int]:
        query = session.query(cls).filter(cls.pin_id == pinID, cls.status == "Completed")

        if serviceType and str(serviceType).strip():
            query = query.filter(cls.service_type == str(serviceType).strip())

        if fromDate:
            start_dt = datetime.combine(fromDate, time.min)
            query = query.filter(cls.completed_at >= start_dt)
        if toDate:
            end_dt = datetime.combine(toDate, time.max)
            query = query.filter(cls.completed_at <= end_dt)

        total_count = query.count()
        from sqlalchemy import desc, nullslast
        query = query.order_by(nullslast(desc(cls.completed_at)), desc(cls.created_at))

        offset = max(0, (int(page) - 1) * int(page_size))
        items = query.offset(offset).limit(int(page_size)).all()
        return items, total_count
