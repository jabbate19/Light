####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, FormField, DateTimeField, SelectField, Form
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ColorInput
import re

class RoomForm(FlaskForm):
    name = TextAreaField("Room Name",
        validators=[DataRequired()])
    pswd = TextAreaField("Serial #",
        validators=[DataRequired()])
    whitelist = TextAreaField("Whitelist",
        validators=[])
    submit = SubmitField(('Submit'), validators=[DataRequired()])

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class ColorForm(FlaskForm):
    style = SelectField(u'RGB Style',
        choices=[
            ("SOLID", "Solid"),
            ("BLINK", "Blink"),
            ("CHASE", "Chase"),
            ("COMET", "Comet"),
            ("PULSE", "Pulse"),
            ("SPARKLE", "Sparkle"),
            ("SPARKLE PULSE", "Sparkle Pulse"),
            ("RAINBOW", "Rainbow"),
            ("RAINBOW CHASE", "Rainbow Chase"),
            ("RAINBOW COMET", "Rainbow Comet"),
            ("RAINBOW SPARKLE", "Rainbow Sparkle"),
#            ("INTRUDER", "Intruder Alert (EPILEPSY WARNING!)"),
            ("OFF", "Off")
        ],
        validators=[DataRequired()]
    )
    numcolors = SelectField(u'Number of Colors',
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3")
        ],
        validators=[DataRequired()]
    )
    color1 = StringField(widget=ColorInput(), validators=[DataRequired()])
    color2 = StringField(widget=ColorInput(), validators=[DataRequired()])
    color3 = StringField(widget=ColorInput(), validators=[DataRequired()])
    submit = SubmitField(('Submit'), validators=[DataRequired()])
    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

