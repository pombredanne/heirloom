import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
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

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm(request.form)

    search_string = search_form.data['search']
    if search_string != '' and request.method == 'POST':
        return search_results(search_form)
    #results = Card.query.filter(Card.name.like("%isperia%")).first()
    #return render_template('index.html', results=results)
    return render_template('search.html', form=search_form)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search_string != '':
        results = Card.query.filter(Card.name.like('%'+search_string+'%')).all()
    if not results:
        flash('No results found!')
        return redirect('/')
    # display results
    return render_template('index.html', results=results)

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
