import string
import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_mapForm
from .models import URL_map


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_link = ''.join(random.choices(letters_and_digits, k=6))
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short:
            if URL_map.query.filter_by(short=short).first():
                flash(f'Имя {short} уже занято!')
                return render_template('index.html', form=form)
        else:
            short = get_unique_short_id()
            while URL_map.query.filter_by(short=short).first():
                short = get_unique_short_id()

        link = URL_map(
            original=form.original_link.data,
            short=short
        )
        db.session.add(link)
        db.session.commit()
        context = {'form': form, 'link': link}
        return render_template('index.html', **context)
    return render_template('index.html', form=form)


@app.route('/<string:url>')
def redirect_view(url):
    url = URL_map.query.filter_by(short=url).first()
    if url is not None:
        return redirect(url.original)
    abort(404)
