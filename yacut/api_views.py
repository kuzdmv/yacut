import re

from flask import jsonify, request

from . import app, db
from .models import URL_map
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    short = ''
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data and data['custom_id']:
        pattern = re.compile(r'^[A-Za-z0-9_]+$')
        short = data['custom_id']
        if len(short) < 1 or len(short) > 16 or not bool(pattern.match(short)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URL_map.query.filter_by(short=short).first():
            raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
    if 'custom_id' not in data or data['custom_id'] is None:
        short = get_unique_short_id()
        while URL_map.query.filter_by(short=short).first():
            short = get_unique_short_id()
    url = URL_map(
        original=data['url'],
        short=short
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:custom_id>/', methods=['GET'])
def get_url(custom_id):
    url = URL_map.query.filter_by(short=custom_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
