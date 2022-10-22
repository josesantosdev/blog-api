from . import db, ma
from sqlalchemy import true, BigInteger, String, DateTime
from marshmallow import fields
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
#SQLAlchemy Model
class User(db.Model):
        __tablename__ = 'Users'
        id = db.Column(BigInteger, primary_key=True)
        name = db.Column(String(255), nullable=False)
        username = db.Column(String(255), nullable=False)
        email = db.Column(String(255), nullable=False, unique=True)
        password = db.Column(String(255))
        created_at = db.Column(DateTime)
        modifield_at = db.Column(DateTime)

        def __init__(self, name, email, password, username) -> None:
            self.name = name
            self.email= email
            self.password = generate_password_hash(password)
            self.username = username
            self.created_at = datetime.datetime.utcnow()
            self.modified_at = datetime.datetime.utcnow()

        def save(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self, data):
            for key, item in data.items():
                if key == 'password':
                    self.password = generate_password_hash(data.get('password'))
                
                setattr(self, key, item)
            
            self.modified_at = datetime.datetime.utcnow()

            db.session.commit()
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()

        @staticmethod
        def get_one_user(id):
            return User.query.get(id)

        @staticmethod
        def get_all_users():
            return User.query.all()

        @staticmethod
        def get_user_by_email(email):
            return User.query.filter_by(email=email).firt()

        def verify_password(self, data):
            return check_password_hash(self.password, data.get('password'))


        
#Marshmallow Serealize
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


        

    