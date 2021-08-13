import os

from app.utils.env_utils import load_environment

ENVIRONMENT = load_environment()


def get(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise Exception(f"{key} environment variable is undefined")

    return value


# Root of the repo
ROOT = os.path.dirname(os.path.dirname(__file__))

DB_FILE = os.path.join(ROOT, get("DB_FILE"))
