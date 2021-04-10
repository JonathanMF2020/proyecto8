from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@roles_required('admin')
def admin():
    return render_template('profile.html', name=current_user.name)