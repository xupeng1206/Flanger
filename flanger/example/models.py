from flanger.db.mixin import AutoApiModelMixin, db


class Book(db.Model, AutoApiModelMixin):

    name = db.Column(db.String(127))
    author = db.Column(db.String(127))

    class Meta:
        allowed_methods = ["get", "post", "put", "delete"]

class Music(db.Model, AutoApiModelMixin):

    name = db.Column(db.String(127))
    composer = db.Column(db.String(127))

    class Meta:
        allowed_methods = ["get", "post", "put", "delete"]


class Video(db.Model, AutoApiModelMixin):

    name = db.Column(db.String(127))
    director = db.Column(db.String(127))

    class Meta:
        allowed_methods = ["get", "post", "put", "delete"]
