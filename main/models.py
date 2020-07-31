from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    nodemcu = db.Column(db.Text, default='')
    token_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
       return {'id':self.id,'email':self.email,'name':self.name,'avatar':self.avatar,'active':self.active,'token':self.tokens,'created at':self.created_at,'nodemcu':self.nodemcu,'token created at':self.token_created_at}