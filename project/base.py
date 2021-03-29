from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
clie = Blueprint('clientes', __name__, url_prefix="/clientes")

#getAll
@clie.route('/')
def getAll():
    #productos = Producto.query.all()
    return render_template('clientes.html', clientes=[])

#Agregar/Modificar
@clie.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != None:
        #modificar
        pass
    else:
        #agregar
        pass
    
    #db.session.add(producto)
    #db.session.commit()
    #antes del redirect, enviar un flash
    return redirect("/clientes/")

#Eliminar
@clie.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    #producto = Producto.query.filter_by(id=id)
    #db.session.delete(producto)
    #db.session.commit()
    #antes del redirect, enviar un flash
    return redirect("/clientes/")