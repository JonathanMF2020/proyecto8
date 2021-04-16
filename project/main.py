from flask import Blueprint, render_template
#from flask_security import current_user
from flask_security.decorators import roles_accepted
#from . import db


main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/base')
@roles_accepted('admin', 'vendedor','surtidor','almacenista')
def base():
    return render_template('home.html')




