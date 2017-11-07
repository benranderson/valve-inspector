from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, \
    SelectField, DecimalField
from wtforms.validators import Required


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

    # def __init__(self, status):
    #     super(LogForm, self).__init__()
    #     self.status.default = status
    #     self.process()
