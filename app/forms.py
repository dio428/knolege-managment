from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    """Login form for users."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserCreationForm(FlaskForm):
    """Form for admin to create a new user."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    is_admin = BooleanField('Is Admin?')
    submit = SubmitField('Create User')

class ProductForm(FlaskForm):
    """Form for admin to create a new product."""
    name = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Create Product')

class TipSubmissionForm(FlaskForm):
    """Form for users to submit a new tip."""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    product = SelectField('Product', coerce=int, validators=[DataRequired()])
    attachments = FileField('Attachments (you can select multiple files)')
    submit = SubmitField('Submit Tip')
