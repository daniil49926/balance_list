import os


class Config:
    DEBUG: bool = bool(os.environ.get('APP_DEBUG', False))
    HOST: str = os.environ.get('APPLICATION_HOST')
    PORT: int = int(os.environ.get('APPLICATION_PORT'))
    DATABASE_URI: str = os.environ.get('PG_DSN')
