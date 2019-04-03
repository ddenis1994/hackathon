from .mainConfig import Config


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///localDB/mainDB.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'neddproject@gmail.com'
    MAIL_PASSWORD = 'nedd123456'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    DEBUG = True


