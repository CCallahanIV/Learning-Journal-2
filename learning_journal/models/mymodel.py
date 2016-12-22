from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class Entries(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(Date)
    body = Column(Unicode)
