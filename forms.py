from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, FloatField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image_url = URLField('Image URL (Optional)')
    submit = SubmitField('Add Book')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [
        DataRequired(),
        Length(min=6),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')