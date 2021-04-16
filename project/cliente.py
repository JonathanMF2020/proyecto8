from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_security.decorators import roles_accepted
from . import db
from .models import Cliente
import json
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
cliente = Blueprint('clientes', __name__, url_prefix="/clientes")

@cliente.route('/')
@roles_accepted('admin','vendedor')
def getAll():
    clientes = db.session.query(Cliente).filter(Cliente.estatus == 1).all()
    return render_template('clientes.html', clientes=clientes)

#Traer clientes
@cliente.route('/getAll')
def getJson():
    clientes = db.session.query(Cliente).filter(Cliente.estatus == 1).all()
    list_cliente = []
    for m in clientes:
        list_cliente.append(m.toJson())
    return json.dumps(list_cliente)

#Agregar/Modificar
@cliente.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != "":
        idr = request.form.get("txtId")
        nombre_empresa = request.form.get("txtNombreEmpresa")
        email = request.form.get("txtEmail")
        telefono = request.form.get("txtTelefono")
        direccion = request.form.get("txtDireccion")
        contacto = request.form.get("txtContacto")
        rfc = request.form.get("txtRFC")
        cliente = db.session.query(Cliente).filter(Cliente.estatus == 1).filter(Cliente.id == idr).first()
        cliente.nombre_empresa = nombre_empresa
        cliente.email = email
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.contacto = contacto
        cliente.rfc = rfc
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente modificado exitosamente", "success")
    else:
        nombre_empresa = request.form.get("txtNombreEmpresa")
        email = request.form.get("txtEmail")
        telefono = request.form.get("txtTelefono")
        direccion = request.form.get("txtDireccion")
        contacto = request.form.get("txtContacto")
        rfc = request.form.get("txtRFC")
        cliente = Cliente(nombre_empresa=nombre_empresa, email=email, telefono=telefono, direccion=direccion, 
                            contacto=contacto, rfc=rfc, estatus=1)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente agregado exitosamente", "success")
    
    return redirect(url_for('clientes.getAll'))

#Eliminar
@cliente.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    cliente = db.session.query(Cliente).filter(Cliente.estatus == 1).filter(Cliente.id == id).first()
    cliente.estatus = 0
    db.session.add(cliente)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)