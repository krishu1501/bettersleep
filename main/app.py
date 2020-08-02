# import os
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import os
from datetime import datetime
import json
import ast
from flask import Flask, render_template, url_for, redirect , request, session, send_from_directory, safe_join, current_app, flash
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
# app.app_context().push()
# db.create_all()
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
#     token_created_at = db.Column(db.DateTime, default=datetime.utcnow())

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
        'nodemcu_user' : username,
        'project_id' : project_id,
        'vars' : {"LED_STATUS":0},
        'url' : 'https://'+ project_id +'.firebaseio.com/'+str(username)+ '.json'
    }
    return str(d)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
@app.route('/login/<prompt>')
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
                        return redirect(url_for('login',prompt='consent'))
                    token['refresh_token'] = prev_tok['refresh_token']
            if user is None:
                # print("User not present previously")
                if 'refresh_token' not in token:
                    return redirect(url_for('login',prompt='consent') )
                user = User()
                user.email = email
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/learnmore')
def learnmore():
    return render_template('learnmore.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
# @login_required
def download_file(filename):
    try:
        if filename == 'node.txt':
            # @login_required
            def send_nodef(filename):
                nodemcu_user = ast.literal_eval(current_user.nodemcu)['nodemcu_user']
                filename = os.path.join(current_app.root_path, Auth.UPLOAD_FOLDER, filename)
                f_write = os.path.join(current_app.root_path, Auth.UPLOAD_FOLDER, 'nodemcu_code.txt')
                # filename = safe_join(Auth.UPLOAD_FOLDER,filename)
                # f_write = safe_join(Auth.UPLOAD_FOLDER,'nodemcu_code.txt')
                f = open(filename, 'rt')
                f2 = open(f_write, 'wt')
                for line in f:
                    if '<NODEMCU_USER>' in line:
                        line = line.replace('<NODEMCU_USER>',nodemcu_user)
                    f2.write(line)
                f.close()
                f2.close()
                return send_from_directory(Auth.UPLOAD_FOLDER,filename='nodemcu_code.txt',attachment_filename='nodemcu_code.txt',as_attachment=True)
            send_nodef = login_required(send_nodef)
            return send_nodef(filename)
        else:
            return send_from_directory(Auth.UPLOAD_FOLDER,filename=filename,as_attachment=True)
    except Exception as e:
        return str(e)

# @app.route('/mydata')
# @login_required
# def my_data():
#     # user = User.query.filter_by(id=current_user.get_id()).first()
#     # return User.__repr__(user)
#     # return User.__repr__(current_user)
#     return render_template('mydata.html',user=User.__repr__(current_user))
    
@app.route('/users')
# @login_required
def all_users():
    all_user = User.query.all()
    d = {'id': 'name'}
    for i in all_user:
        d[i.id] = i.name
    return str(d)
    # return render_template('all_users.html',data=d)

@app.route('/data/<int:a>')
def my_data(a=1):
    # all_user = User.query.all()
    # d = []
    # for i in all_user:
    #     d.append(i)
    # return d
    user = User.query.filter_by(id=a).first()
    return User.__repr__(user)
    # user = User.query.filter_by(id=current_user.get_id()).first()
    # return User.__repr__(user)
    # return User.__repr__(current_user)
    # return render_template('mydata.html',user=User.__repr__(current_user))
