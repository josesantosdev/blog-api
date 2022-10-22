from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


def condigure(app):
    db = SQLAlchemy
    ma = Marshmallow
    db.init_app(app)
    ma.init_app(app)
    app.db = db
    

class User(db.Model):
    def __init__(self, id, name, email, password) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password

class UserSchema:
    class Meta:
        pass

    