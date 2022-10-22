from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy
ma = Marshmallow

def condigure(app):
    db.init_app(app)
    ma.init_app(app)
    app.db = db
    