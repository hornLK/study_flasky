from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField
)
from wtforms.validators import Required,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[
    Required(),Length(1,64),Email()]
    )
    password = PasswordField(
    'Password',validators=[
        Required()]
    )
    remember_me = BooleanField('Keep login')
    submit = SubmitField('LogIn')

class RegisterationForm(FlaskForm):
    email = StringField('Email',validators=[
        Required(),Length(1,64),Email()]
    )
    username = StringField(
        'Username',validators = [
            Required(),
            Length(1,64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$',
                0,
                'Usernames must have only letters,'
                'numbers,dots or underscores'
            )
    ]
    )
    password = PasswordField(
        'Password',validators=[
            Required(),
            EqualTo('password2',message='Passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm password',validators=[Required()]
    )
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('You old password',
                                 validators=[Required()])
    new_password = PasswordField('You new password',
                                 validators=[
                                 Required(),
                                 EqualTo('new_password2',message='Passwords  must match')])
    new_password2 = PasswordField('confirm new password',
                                 validators=[Required()])
    submit = SubmitField("reset password")
    def validate_oldpassword(self,field):
        if User.query.filter_by(password!=field.data).first():
            raise ValidationError('old password error')
