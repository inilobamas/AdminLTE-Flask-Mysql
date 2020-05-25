from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberme = BooleanField('Remember me?')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('Password', validators=[DataRequired()])
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    # role = StringField('Fullname', validators=[DataRequired()])
    submit = SubmitField('Submit')
