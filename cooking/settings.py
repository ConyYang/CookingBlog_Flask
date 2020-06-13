import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SCRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('COOK Admin', MAIL_USERNAME)

    COOKLOG_EMAIL = os.getenv('COOKLOG_EMAIL')
    COOKLOG_POST_PER_PAGE = 10
    COOKLOG_MANAGE_POST_PER_PAGE = 15
    COOKLOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}