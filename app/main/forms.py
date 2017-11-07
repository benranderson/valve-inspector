from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, \
    DateTimeField, SelectField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required


class ProjectForm(FlaskForm):
    number = StringField('Number', validators=[Required()])
    title = StringField('Title', validators=[Required()])
    client = StringField('Client', validators=[Required()])
    vessel = StringField('Vessel')
    campaign = StringField('Campaign')
    date = DateField('Date', default=datetime.now)
    submit = SubmitField('Submit')


class ValveForm(FlaskForm):
    tag = StringField('Tag', validators=[Required()])
    size = IntegerField('Size [in]', validators=[Required()])
    location = StringField('Location', validators=[Required()])
    submit = SubmitField('Submit')


class LogForm(FlaskForm):
    date = DateTimeField('Date and Time', validators=[Required()],
                         default=datetime.now)
    status = SelectField('Status',
                         choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')],
                         validators=[Required()])
    turns = DecimalField('Number of turns', validators=[Required()])
    submit = SubmitField('Submit')
