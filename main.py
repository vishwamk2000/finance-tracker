

from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Transaction

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Tracker")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    transaction_type: str
    transaction_date: date


@app.get("/")
def home():
    return {
        "application": "Personal Finance Tracker",
        "version": "0.2.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    if transaction.transaction_type not in ("income", "expense"):
        raise HTTPException(
            status_code=400,
            detail="transaction_type must be income or expense",
        )

    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@app.get("/transactions")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.id.desc()).all()


@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    total_expenses = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(total_income - total_expenses, 2),
        "transaction_count": len(transactions),
    }
