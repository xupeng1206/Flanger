from sqlalchemy import Column, Integer
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    update_time = Column('update_time', Integer)


class AutoApiModel(BaseModel):
    __abstract__ = True
