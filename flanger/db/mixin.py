import datetime

from flanger.db.ext import db


class BaseModelMixin:
    __table__ = None

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def filter(cls, *args):
        return cls.query.filter(*args)

    @classmethod
    def delete_filtered(cls, *args):
        cls.query.filter(*args).delete()
        db.session.commit()

    @classmethod
    def delete_all(cls):
        cls.query.delete()
        db.session.commit()


class AutoApiModelMixin:

    __table__ = None

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def filter(cls, *args):
        return cls.query.filter(*args)

    @classmethod
    def delete_filtered(cls, *args):
        cls.query.filter(*args).delete()
        db.session.commit()

    @classmethod
    def delete_all(cls):
        cls.query.delete()
        db.session.commit()
