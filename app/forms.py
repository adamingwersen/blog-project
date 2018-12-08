from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp, NoneOf
from app.models import User

class LoginForm(FlaskForm):
    username    = StringField('Username', validators = [DataRequired()])
    password    = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username    = StringField('Username', validators = [DataRequired(), Regexp('^[a-zA-Z0-9_.]*$', message = 'Username must not contain spaces')])
    full_name   = StringField('Full Name', validators = [DataRequired(), Regexp('^[a-zA-Z ]*$', message = 'Your full name must not contain special characters')])
    email       = StringField('Email', validators = [DataRequired(), Email(message = 'Please provide a valid email adress')])
    password    = PasswordField('Password', validators = [DataRequired()])
    password2   = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password', message = 'Passwords do not match')])
    submit      = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise(ValidationError('Username already taken. Choose another'))

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise(ValidationError('Email already taken. Choose another'))

class EditProfileForm(FlaskForm):
    username    = StringField('Username', validators = [DataRequired(), Regexp('^[a-zA-Z0-9_.]*$', message = 'Username must not contain spaces')])
    full_name   = StringField('Full Name', validators = [DataRequired(), Regexp('^[a-zA-Z ]*$', message = 'Your full name must not contain special characters')])
    email       = StringField('Email', validators = [DataRequired(), Email(message = 'Please provide a valid email adress')])
    about_me    = TextAreaField('About me', validators = [Length(min = 0, max = 50)], widget = TextArea())
    submit      = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise(ValidationError('Username already taken. Choose another'))

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise(ValidationError('Email already taken. Choose another'))

class PostForm(FlaskForm):
    title   = TextAreaField('Title', validators = [DataRequired(), Length(min = 0, max = 40)], widget = TextArea())
    body    = TextAreaField('Body', validators = [DataRequired(), Length(min = 0, max = 8000, message = "Blog post too long")], widget = TextArea())
    submit  = SubmitField('Post')

class PostVoteForm(FlaskForm):
    upvote      = BooleanField('Upvote')
    downvote    = BooleanField('Downvote')

class SearchForm(FlaskForm):
    a = BooleanField('a')
