from datetime import date, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Trade, DailyReview
from schemas import (
    TradeCreate,
    TradeUpdate,
    TradeResponse,
    ReviewCreate,
    ReviewResponse,
    SummaryResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MoreMoney", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════
# Trade Routes
# ═══════════════════════════════════════════


@app.post("/api/trades", response_model=TradeResponse)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = Trade(**trade.model_dump())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@app.get("/api/trades", response_model=list[TradeResponse])
def list_trades(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    stock_code: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Trade)
    if start_date:
        q = q.filter(Trade.trade_date >= start_date)
    if end_date:
        q = q.filter(Trade.trade_date <= end_date)
    if stock_code:
        q = q.filter(Trade.stock_code.contains(stock_code))
    return q.order_by(Trade.trade_date.desc(), Trade.created_at.desc()).all()


@app.get("/api/trades/{trade_id}", response_model=TradeResponse)
def get_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="交易记录不存在")
    return trade


@app.put("/api/trades/{trade_id}", response_model=TradeResponse)
def update_trade(trade_id: int, data: TradeUpdate, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="交易记录不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_trade, key, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@app.delete("/api/trades/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="交易记录不存在")
    db.delete(db_trade)
    db.commit()
    return {"message": "删除成功"}


# ═══════════════════════════════════════════
# Review Routes
# ═══════════════════════════════════════════


@app.post("/api/reviews", response_model=ReviewResponse)
def upsert_review(review: ReviewCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(DailyReview)
        .filter(DailyReview.review_date == review.review_date)
        .first()
    )
    if existing:
        for key, value in review.model_dump().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    db_review = DailyReview(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@app.get("/api/reviews", response_model=list[ReviewResponse])
def list_reviews(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    q = db.query(DailyReview)
    if start_date:
        q = q.filter(DailyReview.review_date >= start_date)
    if end_date:
        q = q.filter(DailyReview.review_date <= end_date)
    return q.order_by(DailyReview.review_date.desc()).all()


@app.get("/api/reviews/{review_date}", response_model=ReviewResponse)
def get_review(review_date: date, db: Session = Depends(get_db)):
    review = (
        db.query(DailyReview)
        .filter(DailyReview.review_date == review_date)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="复盘记录不存在")
    return review


# ═══════════════════════════════════════════
# Summary Route
# ═══════════════════════════════════════════


@app.get("/api/summary", response_model=SummaryResponse)
def get_summary(
    period: str = Query(..., pattern=r"^(daily|weekly|monthly|yearly)$"),
    date_param: Optional[date] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    week: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if period == "daily" and date_param:
        trades = db.query(Trade).filter(Trade.trade_date == date_param).all()
        return _build_summary(trades, f"{date_param} 日汇总")

    if period == "weekly" and year is not None and week is not None:
        jan4 = date(year, 1, 4)
        first_monday = jan4 - timedelta(days=jan4.weekday())
        start = first_monday + timedelta(weeks=week - 1)
        end = start + timedelta(days=6)
        trades = (
            db.query(Trade)
            .filter(Trade.trade_date >= start, Trade.trade_date <= end)
            .all()
        )
        return _build_summary(trades, f"{year}年 第{week}周 ({start} ~ {end})")

    if period == "monthly" and year is not None and month is not None:
        start = date(year, month, 1)
        end_month = month + 1
        end_year = year
        if end_month > 12:
            end_month = 1
            end_year += 1
        end = date(end_year, end_month, 1)
        trades = (
            db.query(Trade)
            .filter(Trade.trade_date >= start, Trade.trade_date < end)
            .all()
        )
        return _build_summary(trades, f"{year}年{month}月 月汇总")

    if period == "yearly" and year is not None:
        trades = (
            db.query(Trade)
            .filter(
                Trade.trade_date >= date(year, 1, 1),
                Trade.trade_date < date(year + 1, 1, 1),
            )
            .all()
        )
        return _build_summary(trades, f"{year}年 年汇总")

    raise HTTPException(status_code=400, detail="参数不完整")


def _build_summary(trades: list[Trade], title: str) -> dict:
    buy_trades = [t for t in trades if t.direction == "买入"]
    sell_trades = [t for t in trades if t.direction == "卖出"]

    total_buy_amount = sum(float(t.amount) for t in buy_trades)
    total_sell_amount = sum(float(t.amount) for t in sell_trades)
    total_pnl = sum(float(t.pnl or 0) for t in trades)

    evaluated = [t for t in trades if t.pnl is not None]
    win_trades = [t for t in evaluated if float(t.pnl) > 0]
    loss_trades = [t for t in evaluated if float(t.pnl) < 0]
    win_rate = (len(win_trades) / len(evaluated) * 100) if evaluated else 0.0

    biggest_win = max((float(t.pnl) for t in win_trades), default=0.0)
    biggest_loss = min((float(t.pnl) for t in loss_trades), default=0.0)

    stocks: dict[str, dict] = {}
    for t in trades:
        key = f"{t.stock_code} {t.stock_name}"
        entry = stocks.setdefault(key, {"count": 0, "total_pnl": 0.0})
        entry["count"] += 1
        entry["total_pnl"] += float(t.pnl or 0)

    return {
        "title": title,
        "total_trades": len(trades),
        "buy_count": len(buy_trades),
        "sell_count": len(sell_trades),
        "total_buy_amount": round(total_buy_amount, 2),
        "total_sell_amount": round(total_sell_amount, 2),
        "total_pnl": round(total_pnl, 2),
        "win_count": len(win_trades),
        "loss_count": len(loss_trades),
        "win_rate": round(win_rate, 2),
        "biggest_win": round(biggest_win, 2),
        "biggest_loss": round(biggest_loss, 2),
        "stocks": sorted(
            (
                {"name": k, "count": v["count"], "total_pnl": round(v["total_pnl"], 2)}
                for k, v in stocks.items()
            ),
            key=lambda x: x["total_pnl"],
            reverse=True,
        ),
        "trades": [
            {
                "id": t.id,
                "trade_date": str(t.trade_date),
                "stock_code": t.stock_code,
                "stock_name": t.stock_name,
                "direction": t.direction,
                "amount": float(t.amount),
                "pnl": float(t.pnl or 0),
                "pnl_pct": float(t.pnl_pct or 0),
                "reason": t.reason,
            }
            for t in trades
        ],
    }

