from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class SearchForm(FlaskForm):
  search = StringField('search')
  submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})

class CfgNotifyForm(FlaskForm):
    check_order = StringField('Sort', validators=[DataRequired(message='Can not be empty'), Length(0, 64, message='Incorrect Length')])
    notify_type = SelectField('Notification Type', choices=[('MAIL', 'E-mail Notification'), ('SMS', 'SMS Notification')],
                              validators=[DataRequired(message='Can not be empty'), Length(0, 64, message='Incorrect Length')])
    notify_name = StringField('Notifier Name', validators=[DataRequired(message='Can not be empty'), Length(0, 64, message='Incorrect Length')])
    notify_number = StringField('Notification Number', validators=[DataRequired(message='Can not be empty'), Length(0, 64, message='Incorrect Length')])
    status = BooleanField('Effective Sign', default=True)
    submit = SubmitField('Submit')
