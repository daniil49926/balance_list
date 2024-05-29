def load_environ(base_dir: str) -> None:
    """
    The environment variables file must be on the same level as the base directory of the application
    :param base_dir: string value of the base directory of the application
    :type base_dir: str
    """
    import os

    from dotenv import load_dotenv

    if not base_dir.endswith('\\'):
        base_dir += '\\'

    if os.path.exists(os.path.join(os.path.dirname(base_dir), ".env")):
        load_dotenv(os.path.join(os.path.dirname(base_dir), ".env"))
