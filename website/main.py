import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_table import Table, Col
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from website.forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw' # required for wtforms
Bootstrap(app)
moment = Moment(app)

import config
engine = engine_from_config(config.DATABASE, prefix='db.')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from website.models import Card # Circular import

class ItemTable(Table):
    name = Col('NAME')
    mana_cost = Col('COST')
    usd = Col('USD')
    tix = Col('TIX')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.args)
    query = form.data['q']
    table = None
    if query is not None:
        items = Card.query.filter(Card.name.like('%'+query+'%')).all()
        table = ItemTable(items)
    return render_template('index.html', form=form, query=query, table=table)

@app.route('/search', methods=['GET'])
def search():
    form = SearchForm(request.args)
    select = form.select.data
    query = request.args.get('q', None)
    table = None
    if query is not None:
        if select == 'Heirloom':
            items = Card.query.filter(Card.name.like('%'+query+'%')).filter(Card.heirloom_legal == 1).all()
        else:
            items = Card.query.filter(Card.name.like('%'+query+'%')).all()
        table = ItemTable(items)
    return render_template('index.html', form=form, query=query, table=table)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
