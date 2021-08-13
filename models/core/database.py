import os

from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_FILE
from models.core.auth_session import AuthSession


def safe_environ_get(name, *default):
    var = os.environ.get(name)
    if var is None:
        if default:
            return default
        else:
            raise ValueError(f"environment variable {name} must be set")
    else:
        return var


class FastMTGDB(object):
    def __init__(self):
        db_conn = "sqlite:///" + DB_FILE
        self.session_maker = sessionmaker(
            class_=AuthSession, autocommit=False, autoflush=False, bind=engine
        )
        self.engine = create_engine(db_conn)
        self._mtg_db = None

    def get_mtg_db(self, user: str = None, update_override=False) -> AuthSession:
        return self.session_maker(
            bind=self.engine, user_uid=user, update_override=update_override
        )
