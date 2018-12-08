from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors

"""
 - DATETIME FORMATTER
"""
@app.template_filter('castdate')
def cast_date(dt):
    return(dt.strftime('%Y-%m-%d %H:%M'))
