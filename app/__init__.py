from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.db = db
    
    Migrate(app, app.db)
   

    from .models import user_model, blog_post_model, revoked_token_model

    return app