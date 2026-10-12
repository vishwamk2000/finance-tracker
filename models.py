
from sqlalchemy import Column, Date, Float, Integer, String
from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)
