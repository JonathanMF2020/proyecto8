from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Producto
import json

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
productos = Blueprint('productos', __name__, url_prefix="/productos")

@productos.route('/')
def getAll():
    productos = db.session.query(Producto).filter(Producto.estatus == 1).all()
    return render_template('productos.html', productos=productos)

#Agregar/Modificar
@productos.route('/guardar', methods=["POST"])
def guardar():
    idt = request.form.get("txtId")
    #print(idt)
    if request.form.get("txtId") != "":
        idP = request.form.get("txtId")
        nombre = request.form.get("txtNombre")
        descripcion = request.form.get("txtDescripcion")
        precio = request.form.get("txtPrecio")
        producto = db.session.query(Producto).filter(Producto.estatus == 1).filter(Producto.id == idP).first()
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        db.session.add(producto)
        db.session.commit()
        flash("El producto se modificó", "success")
    else:
        print("Hola")
        nombre = request.form.get("txtNombre")
        descripcion = request.form.get("txtDescripcion")
        precio = request.form.get("txtPrecio")
        producto = Producto(nombre=nombre,descripcion=descripcion,precio=precio,cantidad=0,estatus=1)
        db.session.add(producto)
        db.session.commit()
        flash("Producto agregado", "success")
    
    return redirect(url_for('productos.getAll'))

#Eliminar
@productos.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    producto = db.session.query(Producto).filter(Producto.estatus == 1).filter(Producto.id == id).first()
    producto.estatus = 0
    db.session.add(producto)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)