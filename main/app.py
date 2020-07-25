# import os
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from datetime import datetime
import json
import ast
from flask import Flask, render_template, url_for, redirect , request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required ,UserMixin
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from .config import config, Auth, Config, DevConfig, ProdConfig
from .commands import create_tables
from .models import db,User


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['prod'])
    db.init_app(app)
    # login_manager.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.cli.add_command(create_tables)

    return app


# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object(config['prod'])
app = create_app()
app.app_context().push()
db.create_all()
# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.session_protection = "strong"

# def get_app():
#     return app

# class User(db.Model, UserMixin):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     name = db.Column(db.String(100), nullable=True)
#     avatar = db.Column(db.String(200))
#     active = db.Column(db.Boolean, default=True)
#     tokens = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     nodemcu = db.Column(db.Text, default='')

# @login_manager.request_loader
# def load_user_from_request(request):
#     return redirect(url_for('login'))



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
def login(prompt=None):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline',prompt=prompt)
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/oauth2callback')
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
        # authorization code if received, included in the redirect URL

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
            if user is not None:
                prev_tok = ast.literal_eval(user.tokens)
                if 'refresh_token' not in token:
                    if 'refresh_token' not in prev_tok:
                        return ('Please Login again' + login('consent') )
                    token['refresh_token'] = prev_tok['refresh_token']
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

@app.route('/mydata')
@login_required
def my_data():
    user = User.query.filter_by(id=current_user.get_id()).first()
    return User.__repr__(user)
    
@app.route('/users')
# @login_required
def all_users():
    all_user = User.query.all()
    d = {'id': 'name'}
    for i in all_user:
        d[i.id] = i.name
    return str(d)



# token = google.fetch_token(
#     Auth.TOKEN_URI,
#     client_secret=Auth.CLIENT_SECRET,
#     authorization_response=request.url)

# google = get_google_auth(token=token)
# resp = google.get(Auth.USER_INFO)
# print(resp.json)



