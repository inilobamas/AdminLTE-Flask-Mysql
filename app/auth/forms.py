from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberme = BooleanField('Remember me?')
    submit = SubmitField('Submit')