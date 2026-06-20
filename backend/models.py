from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Text
from sqlalchemy.sql import func
from database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    trade_date = Column(Date, nullable=False, index=True)
    stock_code = Column(String(10), nullable=False)
    stock_name = Column(String(50), nullable=False)
    direction = Column(String(4), nullable=False)
    price = Column(Numeric(10, 3), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    position_pct = Column(Numeric(5, 2))
    pnl = Column(Numeric(15, 2))
    pnl_pct = Column(Numeric(7, 2))
    reason = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class DailyReview(Base):
    __tablename__ = "daily_reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_date = Column(Date, nullable=False, unique=True, index=True)
    market_review = Column(Text)
    self_review = Column(Text)
    tomorrow_outlook = Column(Text)
    tomorrow_plan = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
