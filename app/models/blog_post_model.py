from app import db, ma
from sqlalchemy import true, BigInteger, String, DateTime, Text, ForeignKey
from marshmallow import fields
import datetime


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(BigInteger, primary_key=True)
    title = db.Column(String(128), nullable=False)
    contents = db.Column(Text, nullable=False)
    owner_id = db.Column(BigInteger, ForeignKey('Users.id'), nullable=False)
    created_at = db.Column(DateTime)
    modified_at = db.Column(DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.contents = data.get('contents')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    @staticmethod
    def get_all_blogposts():
        return BlogPost.query.all()
  
    @staticmethod
    def get_one_blogpost(id):
        return BlogPost.query.get(id)

    def __repr__(self):
        return f'<id {self.id}>'

class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost
        load_instance = true
        include_fk = True

        id = fields.Int(dump_only=True)
        title = fields.Str(required=True)
        contents = fields.Str(required=True)
        owner_id = fields.Int(required=True)
        created_at = fields.DateTime(dump_only=True)
        modified_at = fields.DateTime(dump_only=True)
        

'''
    # HATEOS
    _links = ma.Hyperlinks({
        "self": ma.URLFor(""), #add controller route and method
        "colletion": ma.URLFor("") #add controller route and method
    })

'''