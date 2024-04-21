from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/chart')
def chart():
    return render_template('chart.html', title='Transit Chart')
