from app import app, db
from app.models import User, Post, PostRegister
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, PostVoteForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
import flask_whooshalchemy

"""
 - SET ACTIVITY -
 Sets latest activity and commit to db
"""


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


"""
 - LOGOUT -
"""


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return(redirect(url_for('index')))


"""
 - INDEX -
Routes all transaction from / and /index
"""


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.has_prev else None
    if current_user.is_authenticated:
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data,
                        body=form.body.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Posted!', category='message')
            return(redirect(url_for('index')))
        return(render_template('index.html',  title="Home", form=form, posts=posts.items, next_url=next_url, prev_url=prev_url))
    else:
        return(render_template('welcome.html',  title="Welcome", posts=posts.items, next_url=next_url, prev_url=prev_url))


"""
 - BOARD -
"""


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
    form = PostVoteForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc())
    n_posts = posts.count()
    posts = posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'browse', page=posts.next_num) if posts.has_next else None
    prev_url = url_for(
        'browse', page=posts.prev_num) if posts.has_prev else None
    return(render_template('browse.html',  title="Browse", posts=posts.items, n_posts=n_posts, next_url=next_url, prev_url=prev_url))


@app.route('/search', methods=['POST'])
@login_required
def search():
  form = SearchForm()
  if not form.validate_on_submit():
    return redirect(url_for('index'))
  return redirect((url_for('search_results', query=form.search.data)))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)


"""
 - LOGIN -
"""


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return(redirect(url_for('login')))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return(redirect(next_page))

    return(render_template('login.html', title='Sign In', form=form))


"""
 - USER PAGE -
"""


@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    n_posts = posts.count()
    posts = posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=username,
                       page=posts.prev_num) if posts.has_prev else None
    return(render_template('user.html', user=user, posts=posts.items, n_posts=n_posts, next_url=next_url, prev_url=prev_url))


"""
 - EDIT PROFILE
"""


@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile description has been updated!')
        return(redirect(url_for('edit_profile')))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return(render_template('edit_profile.html', title='Edit Profile', form=form))


"""
 - REGISTER -
"""


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, full_name=form.full_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering with us.', category='message')
        return(redirect(url_for('login')))
    return(render_template('register.html', title='Register', form=form))
