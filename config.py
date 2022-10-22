class DevelopmentConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_EHCO = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wsr29yhi@localhost/blog'
    DATABASE_CONNECT_OPTIONS = {}
    JSON_AS_ASCII = False

