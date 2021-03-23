
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug import security
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user,logout_user
from .models import User
from . import db, userDataStore

auth = Blueprint('auth',__name__,url_prefix='/security')

@auth.route('/login_users')
def login_users():
    return render_template('/security/login_users.html')

@auth.route('/login_users', methods=['POST'])
def login_users_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o la contraseña son incorrectos')
        current_app.logger.error("El usuario y/o la contraseña son incorrectos")
        return redirect(url_for('auth.login_users')) 
    login_user(user, remember=remember)
    current_app.logger.debug("Se ha logueado")
    return redirect(url_for('main.profile'))

@auth.route('/register_users')
def register_users():
    return render_template('/security/register_user.html')

@auth.route('/register_users', methods=['POST'])
def register_users_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('El correo electrónico ya existe')
        current_app.logger.error("El correo electrónico ya existe")
        return redirect(url_for('auth.register_users'))
    userDataStore.create_user(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.commit()
    current_app.logger.debug("Se ha registrado")
    return redirect(url_for('auth.login_users'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))