from app import app
from app.models import User
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask import render_template, flash, redirect


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Adam'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }]
    return(render_template('index.html',  user = user, posts = posts))


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = from.username.data).first()
        if user in None or not user.check_pwd(form.password.data):
            flash('Invalid username or password')
            return(redirect(url_for('login')))
        login_user(user, remember = form.remember_me.data)
        return(redirect(url_for('index')))
    return(render_template('login.html', title = 'Sign In', form = form))
