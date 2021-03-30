from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Ejemplar, Producto
from datetime import datetime
import json

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
ejem = Blueprint('ejemplares', __name__, url_prefix="/ejemplares")

#getAll
@ejem.route('/', methods=["GET"])
def getById():
    id = request.args.get("id")
    ejemplares = Ejemplar.query.filter(id=id[:11], estatus=1)
    return render_template('clientes.html', clientes=ejemplares)

#Agregar
@ejem.route('/guardar', methods=["GET"])
def guardar():
    talla = int(request.args.get("txtTalla"))
    color = request.args.get("txtColor")
    id_producto = int(request.args.get("txtProducto"))
    rango = int(request.args.get("txtDocenas"))*12
    curdate = str(datetime.now())
    curdate = curdate[:10]

    for e in range(rango):
        codigo = str(id_producto)+"-"+curdate+str(e)
        ejemplar = Ejemplar(codigo=codigo, 
                            talla=talla, 
                            color=color, 
                            estatus=1, 
                            producto_id=id_producto)
        db.session.add(ejemplar)
    
    db.session.commit()
    return "OK"

#Eliminar
@ejem.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    #producto = Producto.query.filter_by(id=id)
    #db.session.delete(producto)
    #db.session.commit()
    #antes del redirect, enviar un flash
    return redirect("/clientes/")