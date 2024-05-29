from datetime import datetime

from aiohttp import web
from asyncpg import UniqueViolationError

from models import User


async def get_user_balance(request):
    user_id = int(request.match_info.get('id'))
    input_date = request.query.get('date')
    on_date = datetime.fromisoformat(input_date.split('.')[0]) if input_date else None

    user = await User.get_user(user_id) if not on_date else await User.get_user_with_balance_on_date(user_id, on_date)
    if not user:
        raise web.HTTPNotFound(text="User not found")
    return web.json_response({
        "id": user.id,
        "name": user.username,
        "balance": str(user.balance),
    })


async def create_user(request):
    data = await request.json()
    name = data.get("name")

    if not name:
        return web.json_response({"error": "Name is required"}, status=400)

    try:
        user = await User.create_user(name)

        return web.json_response({
            "id": user.id,
            "name": user.username,
        }, status=201)
    except UniqueViolationError as err:
        raise web.HTTPBadRequest(text="User with this name already exists") from err
