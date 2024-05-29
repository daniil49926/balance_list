from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DECIMAL, VARCHAR, BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.sql import functions

from core import InvalidTransaction, LowBalanced, db


class Transaction(db.Model):
    __tablename__ = "Transaction"

    id = Column(BigInteger, primary_key=True)
    uid = Column(VARCHAR(50), nullable=False, unique=True)
    type = Column(VARCHAR(20), nullable=False)
    amount = Column(DECIMAL(5, 2), nullable=False)
    user_id = Column(BigInteger, ForeignKey('User.id'), nullable=False)
    t_datetime = Column(DateTime, nullable=False, server_default=functions.now())

    @staticmethod
    async def create_transaction(
        user_id, uid: int, amount: Decimal, transaction_type: str, t_datetime: datetime
    ) -> Any:
        from models import User  # noqa

        def deposit(user_balance: Decimal, transaction_amount: Decimal) -> Decimal:
            return user_balance + transaction_amount

        def withdraw(user_balance: Decimal, transaction_amount: Decimal) -> Decimal:
            if transaction_amount > user_balance:
                raise LowBalanced
            return user_balance - transaction_amount

        operations = {
            'DEPOSIT': deposit,
            'WITHDRAW': withdraw,
        }

        transaction_operation = operations.get(transaction_type)

        if not transaction_operation:
            raise InvalidTransaction('Invalid transaction type')

        async with db.transaction():
            user = await User.query.where(User.id == user_id).with_for_update().gino.first()
            await user.update(
                balance=transaction_operation(user.balance, amount)
            ).apply()

            return await Transaction.create(
                uid=uid,
                type=transaction_type,
                amount=amount,
                user_id=user_id,
                t_datetime=t_datetime,
            )

    @staticmethod
    async def get_transaction(uid: int) -> Any:
        return await Transaction.query.where(Transaction.uid == uid).with_for_update().gino.first()
