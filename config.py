import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'psswrd'
    MYSQL_URI = """mysql+mysqldb://flask_mgmt:flask@localhost[:3306]/flask_app"""
    SQLITE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'
    SQLALCHEMY_DATABASE_URI = MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
