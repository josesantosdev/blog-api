from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import true
from marshmallow import fields


db = SQLAlchemy
ma = Marshmallow

def condigure(app):
    db.init_app(app)
    ma.init_app(app)
    app.db = db
    

class User(db.Model):
        __tablename__ = 'Users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        username = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False, unique=True)
        password = db.Column(db.String(255))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = true

        id = fields.Integer()
        name = fields.Str(required=True)
        username = fields.Str(required=True)
        email = fields.Str(required=True)
        password = fields.Str(required=True)

        
        

    