from datetime import datetime
from typing import Any

from sqlalchemy import DECIMAL, VARCHAR, BigInteger, CheckConstraint, Column, DateTime
from sqlalchemy.sql import and_, case, functions

from core import db


class User(db.Model):
    __tablename__ = "User"

    id = Column(BigInteger, primary_key=True)
    username = Column(VARCHAR(50), nullable=False, unique=True)
    balance = Column(DECIMAL(5, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=functions.now())

    __table_args__ = (
        CheckConstraint(balance >= 0, name='only_positive_balance'),
    )

    @staticmethod
    async def create_user(username: str) -> Any:
        return await User.create(username=username)

    @staticmethod
    async def get_user(user_id: int) -> Any:
        return await User.query.where(User.id == user_id).gino.first()

    @staticmethod
    async def get_user_with_balance_on_date(user_id: int, on_date: datetime) -> Any:
        from models import Transaction
        case_stmt = case(
            [
                (Transaction.type == 'DEPOSIT', Transaction.amount),
                (Transaction.type == 'WITHDRAW', -1 * Transaction.amount)
            ],
        )
        result = await db.select(
            [
                User.id,
                User.username,
                User.created_at,
                functions.sum(case_stmt),
            ]
        ).select_from(
            User.join(Transaction,  User.id == Transaction.user_id)
        ).where(and_(User.id == user_id, Transaction.t_datetime <= on_date)).group_by(User.id).gino.first()
        return None if not result else User(id=int(result[0]), username=result[1], balance=str(result[3]), created_at=result[2])
