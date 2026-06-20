from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ═══════════════════════════════════════════
# Trade
# ═══════════════════════════════════════════

class TradeCreate(BaseModel):
    trade_date: date
    stock_code: str = Field(..., max_length=10)
    stock_name: str = Field(..., max_length=50)
    direction: str = Field(..., pattern=r"^(买入|卖出)$")
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    position_pct: Optional[float] = Field(None, ge=0, le=100)
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class TradeUpdate(BaseModel):
    trade_date: Optional[date] = None
    stock_code: Optional[str] = Field(None, max_length=10)
    stock_name: Optional[str] = Field(None, max_length=50)
    direction: Optional[str] = Field(None, pattern=r"^(买入|卖出)$")
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    amount: Optional[float] = Field(None, gt=0)
    position_pct: Optional[float] = Field(None, ge=0, le=100)
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class TradeResponse(BaseModel):
    id: int
    trade_date: date
    stock_code: str
    stock_name: str
    direction: str
    price: float
    quantity: int
    amount: float
    position_pct: Optional[float] = None
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("price", "amount", "position_pct", "pnl", "pnl_pct", mode="before")
    @classmethod
    def _coerce_numeric(cls, v):
        if v is None:
            return None
        return float(v)


# ═══════════════════════════════════════════
# Review
# ═══════════════════════════════════════════

class ReviewCreate(BaseModel):
    review_date: date
    market_review: Optional[str] = None
    self_review: Optional[str] = None
    tomorrow_outlook: Optional[str] = None
    tomorrow_plan: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    review_date: date
    market_review: Optional[str] = None
    self_review: Optional[str] = None
    tomorrow_outlook: Optional[str] = None
    tomorrow_plan: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════

class StockSummary(BaseModel):
    name: str
    count: int
    total_pnl: float


class TradeSummaryItem(BaseModel):
    id: int
    trade_date: str
    stock_code: str
    stock_name: str
    direction: str
    amount: float
    pnl: float
    pnl_pct: float
    reason: Optional[str] = None


class SummaryResponse(BaseModel):
    title: str
    total_trades: int
    buy_count: int
    sell_count: int
    total_buy_amount: float
    total_sell_amount: float
    total_pnl: float
    win_count: int
    loss_count: int
    win_rate: float
    biggest_win: float
    biggest_loss: float
    stocks: list[StockSummary]
    trades: list[TradeSummaryItem]
