import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from website.forms import SearchForm
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(config.ROOT_DIR, 'oracle.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
from website.models import Card # Circular import

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm(request.form)
    #if request.method == 'POST':
    #return search_results(search_form)
    search_string = search_form.data['search']
    results = Card.query.filter_by(name=search_string).first()
    #return render_template('home.html', form=search_form, results=results)
    return results

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search_string != '':
        results = Card.query.filter_by(name=search_string).all()
    if not results:
        flash('No results found!')
        return redirect('/')
    # display results
    return render_template('results.html', results=results)

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
