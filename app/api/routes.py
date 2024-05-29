from api.apps import add_transaction, create_user, get_transaction, get_user_balance


def add_routes(app):
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{id}', get_user_balance, name='get_user')
    app.router.add_route('POST', r'/v1/transaction', add_transaction, name='add_transaction')
    app.router.add_route('GET', r'/v1/transaction/{id}', get_transaction, name='incoming_transaction')
