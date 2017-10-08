from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, DateTimeField, SelectField
from wtforms.validators import Required
import datetime as dt


class ValveForm(FlaskForm):
    tag = StringField('Tag', validators=[Required()])
    size = DecimalField('Size [mm]', places=2,
                        rounding=None, validators=[Required()])
    submit = SubmitField('Submit')


class LogForm(FlaskForm):
    time = DateTimeField('Date and time', validators=[Required()],
                         default=dt.datetime.now)
    status = SelectField('Status',
                         choices=[('open', 'open'), ('closed', 'closed')],
                         validators=[Required()])
    submit = SubmitField('Submit')
