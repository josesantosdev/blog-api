from . import db, ma
from sqlalchemy import true
from marshmallow import fields

#SQLAlchemy Model
class User(db.Model):
        __tablename__ = 'Users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        username = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False, unique=True)
        password = db.Column(db.String(255))

#Marshmallow Serialize
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = true

        id = fields.Integer()
        name = fields.Str(required=True)
        username = fields.Str(required=True)
        email = fields.Str(required=True)
        password = fields.Str(required=True)

    #HATEOS
    _links = ma.Hyperlinks({
        "self": ma.URLFor("") #add controller route and method
        "colletion": ma.URLFor("") #add controller route and method
    })


        

    