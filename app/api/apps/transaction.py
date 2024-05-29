from datetime import datetime
from decimal import Decimal

from aiohttp import web
from asyncpg import UniqueViolationError

from core.custom_errors import InvalidTransaction, LowBalanced
from models import Transaction, User


async def add_transaction(request):
    data = await request.json()
    user_id = data.get("user_id")
    user = await User.get_user(user_id)

    if not user:
        raise web.HTTPNotFound(text="User not found")

    try:
        transaction = await Transaction.create_transaction(
            user_id,
            data.get("uid"),
            Decimal(data.get("amount")),
            data.get("type"),
            datetime.fromisoformat(data.get("timestamp"))
        )
    except UniqueViolationError:
        transaction = await Transaction.get_transaction(data.get("uid"))
    except LowBalanced as err:
        raise web.HTTPPaymentRequired(text="Low balance") from err
    except InvalidTransaction as err:
        raise web.HTTPBadRequest(text="Invalid transaction") from err

    return web.json_response({"transaction_id": transaction.id})


async def get_transaction(request):
    uid = request.match_info.get("id")
    transaction = await Transaction.get_transaction(uid)

    if not transaction:
        raise web.HTTPNotFound(text="Transaction not found")

    return web.json_response({
        "id": transaction.id,
        "uid": transaction.uid,
        "type": transaction.type,
        "amount": str(transaction.amount),
        "user_id": transaction.user_id,
        "timestamp": transaction.t_datetime.isoformat(),
    })
