from flask import render_template
from . import main

@main.route('/home')
@main.route('/')
def index():
    return render_template('index.html')