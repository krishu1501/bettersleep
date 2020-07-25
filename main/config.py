import os
import ast
import json
import requests

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    # REDIRECT_URI = 'https://localhost:5000/widget'
    # REDIRECT_URI = 'https://bettersleep.eu-gb.mybluemix.net/oauth2callback'
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
    # null = 'null'
    # st = str(os.environ.get('DB_PATH'))

    # headers = {
    # 'Content-Type': 'application/json'
    # }
    # payload = "{\"123\":\"%s\"}" % (st)
    # url = "https://nodemcu-2da43.firebaseio.com/.json"
    # resp = requests.patch(url=url, headers=headers, data=payload)

    # print( "from env : %s" % (st) )
    # # st = st1.replace('null','None')
    # # VCAP_SERVICES = ast.literal_eval(st1)
    # VCAP = ast.literal_eval(st)
    username = os.environ.get("username")
    password = os.environ.get("password")
    host = os.environ.get("host")
    port = int(str(os.environ.get("portn")))
    print("type : ",type(os.environ.get("portn")))
    database = os.environ.get("database")
    schema = os.environ.get("schema")
    SQLALCHEMY_DATABASE_URI = f'ibm_db_sa+pyodbc400://{username}:{password}@{host}:{port}/{database};currentSchema={schema}'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('VCAP_SERVICES')


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
