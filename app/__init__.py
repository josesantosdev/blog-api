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
   

    from app.models.user_model import User
    from app.models.blog_post_model import BlogPost
    from app.models.revoked_token_model import RevokedToken

    from app.controllers.auth_controller import AuthController
    from app.controllers.user_controller import UserController

    app.register_blueprint(AuthController.auth_controller, url_prefix='/api/v1')
    app.register_blueprint(UserController.user_controller, url_prefix='/api/v1')

    return app