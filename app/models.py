from app import db
from app import login
from hashlib import md5
from datetime import datetime
import flask_whooshalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""
Fetches user from table given id
"""
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
The [table] schema for [User]
Holds static user information and last_seen timestamp
"""
class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(64), index = True, unique = True)
    full_name     = db.Column(db.String(80), index = True)
    email         = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts         = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me      = db.Column(db.String(50))
    last_seen     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return('<User {}\nName {}\nID {}>'.format(self.username, self.full_name, self.id))

    """
    Generates password hash from password string
    """
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    """
    Checks if provided password matches self.password_hash
    """
    def check_password(self, password):
        return(check_password_hash(self.password_hash, password))

    """
    Fetches generated avatar from gravatar from hash, which is generated from email
    """
    def avatar(self, size = 64):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return('https://gravatar.com/avatar/{}?d=retro&s={}'.format(digest, size))

"""
The [table] schema for [Post]
Holds static information about posts, linked to user by user_id
"""
class Post(db.Model):
    __searchable__  = ['title', 'body']
    id              = db.Column(db.Integer, primary_key = True)
    title           = db.Column(db.String(40))
    body            = db.Column(db.String(100))
    timestamp       = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return('<Title {}>'.format(self.title))

"""
The [table] schema for [PostRegister]
This table serves as a register for activity on posts by users
"""
class PostRegister(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    post_id     = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    upvote      = db.Column(db.Integer)
    downvote    = db.Column(db.Integer)
