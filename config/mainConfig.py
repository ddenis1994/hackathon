from os import urandom

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = urandom(16)


class DevelopmentConfig(Config):
    DEBUG = True

