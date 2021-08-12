from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import attributes
from sqlalchemy.orm.session import Session


class AuthSession(Session):
    def __init__(
        self, user_uid=None, update_override=False, **kwargs
    ):
        super(AuthSession, self).__init__(**kwargs)
        self._verifying_delete = False
        self.update_override = update_override
        if user_uid:
            self.user = user_uid

    def create_attached_instance(self, meta: DeclarativeMeta):
        instance = meta()
        state = attributes.instance_state(instance)
        state.session_id = self.hash_key
        return instance
