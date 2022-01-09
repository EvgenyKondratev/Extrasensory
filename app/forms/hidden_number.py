from main_app import app
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, NumberRange


class HiddenNumberForm(FlaskForm):
    hidden_number = IntegerField(label='Введите загаданное двухзначное число',
                                 validators=[DataRequired(),
                                             NumberRange(min=app.config.get('MIN_RANGE_HIDDEN_NUMBER'),
                                                         max=app.config.get('MAX_RANGE_HIDDEN_NUMBER'))])
    submit = SubmitField(label='Отправить')
