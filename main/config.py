import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    # REDIRECT_URI = 'https://localhost:5000/widget'
    # REDIRECT_URI = 'https://bettersleep.eu-gb.mybluemix.net/widget'
    REDIRECT_URI = os.environ.get('REDIRECT_URI')
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://oauth2.googleapis.com/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/fitness.activity.read']
    # SCOPE = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email']
    # SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'


class Config:
    APP_NAME = "sleep-app"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")


class ProdConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get('VCAP_SERVICES')


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
