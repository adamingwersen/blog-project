from app import db
from app import login
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
The [table] schema for [User].
TODO:
 * Hashing function implementation for password_hash
 * Describe Post rel.
"""
class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(64), index = True, unique = True)
    email         = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts         = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me      = db.Column(db.String(50))
    last_seen     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return('<User {}>'.format(self.username))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return(check_password_hash(self.password_hash, password))

    def avatar(self, size = 64):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return('https://gravatar.com/avatar/{}?d=retro&s={}'.format(digest, size))

"""
The [table] schema for [Post]
"""
class Post(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    title        = db.Column(db.String(40))
    body         = db.Column(db.String(512))
    timestamp    = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return('<Body {}>'.format(self.body))
