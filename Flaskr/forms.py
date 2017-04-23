from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])