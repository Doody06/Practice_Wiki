from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
import markdown2

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register') 

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25),])
    email = EmailField('Email', validators=[DataRequired(), Email(),])
    password = PasswordField('Password', validators=[Optional(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[Optional()])
    
    def validate_confirm_password(form, field):
        if form.password.data:
            if not field.data:
                raise ValueError('Please confirm your password.')
            if field.data != form.password.data:
                raise ValueError('Passwords must match.')
    submit = SubmitField('Update Profile')   

class NewPageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Markdown Content', validators=[DataRequired()])
    submit = SubmitField('Create Page')
    
class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
    