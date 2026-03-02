import uuid
from sqlalchemy.orm import DeclarativeBase


def new_id() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass
