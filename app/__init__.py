from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Blog-API'
    }
)




def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    CORS(app)


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
    from app.controllers.blog_post_controller import BlogPostController

    app.register_blueprint(AuthController.auth_controller, url_prefix='/api/v1')
    app.register_blueprint(UserController.user_controller, url_prefix='/api/v1')
    app.register_blueprint(BlogPostController.blog_post_controller, url_prefix='/api/v1' )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    return app