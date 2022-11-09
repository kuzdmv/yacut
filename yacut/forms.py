from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URL_mapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional(), Regexp('^[A-Za-z0-9_]+$', message='Недопустимое имя')]
    )
    submit = SubmitField('Создать')
