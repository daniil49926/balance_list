import os

from aiohttp import web

from core.load_env import load_environ

load_environ(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = web.Application()


def main() -> None:
    from api.routes import add_routes
    from cleanups import close_db
    from config import Config
    from core.database import db
    from startups import init_db

    app['config'] = Config
    app['db'] = db

    # Startups
    app.on_startup.append(init_db)

    # Cleanups
    app.on_cleanup.append(close_db)
    add_routes(app)
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)


if __name__ == '__main__':
    main()
