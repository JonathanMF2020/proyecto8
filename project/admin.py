from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user,SQLAlchemyUserDatastore
from flask_security.decorators import roles_required,login_required,roles_accepted
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User,Role
import json
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
admin = Blueprint('admin', __name__, url_prefix="/admin")

@admin.route('/')
@roles_accepted('admin')
def getAll():
    users = db.session.query(User).all()
    return render_template('admin.html', users=users)

@admin.route('/getRoles')
def getRoles():

    roles = db.session.query(Role).all()
    listaRoles = []
    for rol in roles:
        detalle = {}
        detalle = {"id":rol.id, "name":rol.name}
        listaRoles.append(detalle)
    return json.dumps(listaRoles)


@admin.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != "":
        id = request.form.get("txtId")
        userDataStore = SQLAlchemyUserDatastore(db,User,Role)
        nombre = request.form.get("txtNombre")
        email = request.form.get("txtEmail")
        rol = request.form.get("slctRol")
        password = request.form.get("txtContrasena")
        
        user = db.session.query(User).filter(User.id == id).first()
        if password is not None:
            user.password = generate_password_hash(password, method='sha256')
        user.name = nombre
        user.email = email
        db.session.add(user)
        db.session.commit()
        userDataStore.remove_role_from_user(user.email,user.roles[0].name)
        db.session.commit()
        userDataStore.add_role_to_user(email,rol)
        db.session.commit() 
        flash("Materia prima modificada exitosamente", "success")
    else:
        userDataStore = SQLAlchemyUserDatastore(db,User,Role)
        nombre = request.form.get("txtNombre")
        email = request.form.get("txtEmail")
        rol = request.form.get("slctRol")
        password = request.form.get("txtContrasena")
        userDataStore.create_user(name=nombre,email=email,password=generate_password_hash(password, method='sha256'))
        db.session.commit()
        userDataStore.add_role_to_user(email,rol)
        db.session.commit()
        flash("Materia prima agregada exitosamente", "success")
    
    return redirect(url_for('admin.getAll'))


#Eliminar
@admin.route('/eliminar', methods=["POST"])
def eliminar():
    userDataStore = SQLAlchemyUserDatastore(db,User,Role)
    id = int(request.form.get("txtId"))
    user = db.session.query(User).filter(User.id == id).first()
    userDataStore.delete_user(user)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)