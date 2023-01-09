from . import app
from flask import render_template

@app.route('/')
def home_page():
    return render_template('layout.html', title='Envy Free Bipartite Matching')

@app.route('/Article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')
