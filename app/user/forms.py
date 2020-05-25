from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class SearchForm(FlaskForm):
  search = StringField('search')
  submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})