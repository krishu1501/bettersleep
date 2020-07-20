# import os
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from datetime import datetime
import json
from flask import Flask, render_template, url_for, redirect , request, session
from flask_sqlalchemy import SQLAlchemy
# from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required ,UserMixin
from .config import config, Auth, Config, DevConfig, ProdConfig
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(config['prod'])
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

# def get_app():
#     return app

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    nodemcu = db.Column(db.Text, default='')

# @login_manager.request_loader
# def load_user_from_request(request):
#     return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    # print("WOOOOOOOOOOOOWOOOOOOOOOOOOOOWOOOOOOOOOO")
    return User.query.get(int(user_id))

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

def init_nodemcu(email):
    project_id = 'nodemcu-2da43'
    # extracting alphanumerals from email
    email = email[:email.rindex('.')]
    username = ''
    for ch in email:
        if 48<=ord(ch)<=57 or 65<=ord(ch)<=90 or 97<=ord(ch)<=122 :
            username+=ch
    d = {
        'project_id' : project_id,
        'vars' : {"LED_STATUS":0},
        'url' : 'https://'+ project_id +'.firebaseio.com/'+str(username)+ '.json'
    }
    return str(d)


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/widget')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        # Refresh token received included in the redirect URL

        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        # access_token received in 'token'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            # print("User checkinggggggggggggg")
            if user is None:
                # print("User not present previously")
                user = User()
                user.email = email
            # print("User checkinggggggggggggg")
            user.name = user_data['name']
            # print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            user.nodemcu = init_nodemcu(user.email)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/users')
# @login_required
def all_users():
    all_user = db.query.all()
    for i in all_user:
        print(i.id,i.name)
    


# token = google.fetch_token(
#     Auth.TOKEN_URI,
#     client_secret=Auth.CLIENT_SECRET,
#     authorization_response=request.url)

# google = get_google_auth(token=token)
# resp = google.get(Auth.USER_INFO)
# print(resp.json)



