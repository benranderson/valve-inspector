from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, \
    SelectField
from wtforms.validators import Required


class ValveForm(FlaskForm):
    tag = StringField('Tag', validators=[Required()])
    size = IntegerField('Size [in]', validators=[Required()])
    submit = SubmitField('Submit')


class LogForm(FlaskForm):
    date = DateTimeField('Date and time', validators=[Required()],
                         default=datetime.now)
    status = SelectField('Status',
                         choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')],
                         validators=[Required()])
    submit = SubmitField('Submit')
