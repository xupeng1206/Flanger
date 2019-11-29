from sqlalchemy import Column, Integer
from flask_sqlalchemy import SQLAlchemy

__all__ = ['db', 'BaseModel']


db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    update_time = Column('update_time', Integer)
