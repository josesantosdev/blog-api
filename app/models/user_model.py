
from app import db, ma
from sqlalchemy import BigInteger, String, DateTime
from marshmallow import fields, Schema
from werkzeug.security import generate_password_hash, check_password_hash
from .blog_post_model import BlogPostSchema
import datetime



#SQLAlchemy Model
class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(BigInteger, primary_key=True)
        name = db.Column(String(255), nullable=False)
        email = db.Column(String(255), nullable=False, unique=True)
        password = db.Column(String(255))
        created_at = db.Column(DateTime)
        modifield_at = db.Column(DateTime)
        blogposts = db.relationship('BlogPost', backref='User', lazy=True)

        def __init__(self, data):
            self.name = data.get("name")
            self.email = data.get("email")
            self.password = generate_password_hash(data.get("password"))
            self.created_at = datetime.datetime.utcnow()
            self.modified_at = datetime.datetime.utcnow()

        def save(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self, data):
            for key, item in data.items():
                if key == "password":
                    self.password = generate_password_hash(data.get("password"))
                
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
            return User.query.filter_by(email=email).first()
        
        def id_user(self):
            return self.id
    
        def verify_password(self, data_password):
            return check_password_hash(self.password, data_password)

        def __repr__(self) -> str:
            return f'<id {self.id}>'
        
#Marshmallow Serealize
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    blogposts = fields.Nested(BlogPostSchema, many=True)

    #HATEOS
    _links = ma.Hyperlinks({
        "self": ma.URLFor("user_controller.get_one_user", values=dict(id='<id>'))
    })


        

    