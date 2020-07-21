import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = ('552833547680-pf5eserplcmvsnmt18jp4197ru21u0u5.apps.googleusercontent.com')
    CLIENT_SECRET = '8x44hBSsgxOwBezTqXqMbNQD'
    # REDIRECT_URI = 'https://localhost:5000/widget'
    REDIRECT_URI = 'https://bettersleep.herokuapp.com/widget'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://oauth2.googleapis.com/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/fitness.activity.read']
    # SCOPE = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email']
    # SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'


class Config:
    APP_NAME = "local host app"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")


class ProdConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
