import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '73218d6a-6586-420c-870e-46ee72b67634'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <liukq>'
    BOLOG_POSTS_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:123123@192.168.75.1/flask_test'

    BOLGO_MAIL_SUBJECT_PREFIX = '[BOLGO]'
    FLASKY_ADMIN = 'liukaiqiang@pdmi.cn'
    BOLGO_MAIL_SENDER = 'BOLGO Admin <liukaiqiang@pdmi.cn>'
    MAIL_SERVER = 'smtp.pdmi.cn'
    MAIL_PORT = 25
    MAIL_USER_TLS = False
    MAIL_USERNAME = 'liukaiqiang@pdmi.cn'
    MAIL_PASSWORD = 'Tianlkq0608'

config = {
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}
