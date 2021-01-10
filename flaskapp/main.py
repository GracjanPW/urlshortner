import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskapp.db import get_db
from random import choice

bp = Blueprint('main',__name__, url_prefix='/')

@bp.route('/', methods=('GET','POST'))
def create_url():
    short_url = None
    if request.method == 'POST':
        url = request.form['url']

        db = get_db()
        error = None
        
        if not url:
            error = 'Please enter a url to shorten'

        if error is None:
            while True:
                short_url = gen_url()
                if db.execute('SELECT short_url FROM urlpair WHERE short_url = ?',(short_url,)).fetchone() is None:
                    db.execute(
                        'INSERT INTO urlpair (short_url, long_url) VALUES (?,?)',(short_url,url)
                    )
                    db.commit()
                    return render_template('./main/index.html', new_url=short_url)
        flash(error)

    return render_template('./main/index.html',new_url=short_url)


def gen_url():
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    url = ''
    for i in range(6):
        url+= choice(allowed)
    return url

@bp.route('/<string:url>')
def goto_url(url):
    db = get_db()
    nurl = db.execute('SELECT long_url FROM urlpair WHERE short_url = ?',(url,)).fetchall()
    return redirect(nurl[0]['long_url'])