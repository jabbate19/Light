####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, FormField, DateTimeField, SelectField, Form
from wtforms.validators import DataRequired, Length
from wtforms.widgets.html5 import ColorInput

class ColorForm(FlaskForm):
    style = SelectField(u'RGB Style', 
        choices=[
            ("SOLID", "Solid"),
            ("PULSE", "Pulse"),
            ("LINE", "Moving Line"),
            ("RAINBOW", "Full Color Cycle")
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