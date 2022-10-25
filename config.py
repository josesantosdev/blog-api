from instance import config


class DevelopmentConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_EHCO = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config.user}:{config.password}@{config.host}/{config.db}'
    DATABASE_CONNECT_OPTIONS = {}
    JSON_AS_ASCII = False
    JWT_SECRET_KEY = 'super-secret-jwt'

