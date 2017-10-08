from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import Required


class ValveForm(FlaskForm):
    tag = StringField('What is the valve tag?', validators=[Required()])
    size = DecimalField('What is the valve size?', places=2,
                        rounding=None, validators=[Required()])
    submit = SubmitField('Submit')
