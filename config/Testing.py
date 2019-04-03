from .mainConfig import Config


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_utilises/DBTest/mainDB.db'



