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
    # VCAP = (os.environ.get('VCAP_SERVICES'))["dashDB For Transactions"][0]["credentials"]
    # username = VCAP["username"]
    # password = VCAP["password"]
    # host = VCAP["host"]
    # port = VCAP["port"]
    # dbname = VCAP["db"]
    SQLALCHEMY_DATABASE_URI = os.environ.get('VCAP_SERVICES')


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
{
  "dashDB For Transactions": [
    {
      "label": "dashDB For Transactions",
      "provider": null,
      "plan": "Lite",
      "name": "sqldatabase",
      "tags": [
        "big_data",
        "ibm_created",
        "db2",
        "sqldb",
        "purescale",
        "sql",
        "db2 on cloud",
        "db2oncloud",
        "dash",
        "dashdb",
        "oracle",
        "database",
        "transactions",
        "flex",
        "dbaas",
        "ibm_dedicated_public",
        "lite",
        "apidocs_enabled",
        "ibmcloud-alias"
      ],
      "instance_name": "sqldatabase",
      "binding_name": null,
      "credentials": {
        "db": "BLUDB",
        "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=mfj14756;PWD=c6bgzmcwmjr99q+k;",
        "host": "dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net",
        "hostname": "dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net",
        "https_url": "https://dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net:8443",
        "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net:50000/BLUDB",
        "parameters": {
          "role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager"
        },
        "password": "c6bgzmcwmjr99q+k",
        "port": 50000,
        "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=mfj14756;PWD=c6bgzmcwmjr99q+k;Security=SSL;",
        "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net:50001/BLUDB:sslConnection=true;",
        "uri": "db2://mfj14756:c6bgzmcwmjr99q%2Bk@dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net:50000/BLUDB",
        "username": "mfj14756"
      },
      "syslog_drain_url": null,
      "volume_mounts": []
    }
  ]
}