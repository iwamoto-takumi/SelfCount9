from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ScoreForm(FlaskForm):
    fouls = IntegerField('ミス数', validators=[DataRequired(), NumberRange(min=0)], default=0)
    round = IntegerField('Round', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('送信')
