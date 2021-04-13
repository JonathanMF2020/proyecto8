from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Producto, Ejemplar
import json

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
ejem = Blueprint('ejemplares', __name__, url_prefix="/ejemplares")

@ejem.route('/getByProducto')
def getByProducto():
    idP = request.args.get("txtIdP")
    producto = Producto.query.filter_by(id=idP).first()
    ejemplares = db.session.query(Ejemplar).filter(Ejemplar.producto_id == idP).order_by(Ejemplar.talla.asc()).all()
    return render_template("ejemplares.html", ejemplares=ejemplares, producto=producto.nombre)

@ejem.route('/getTallas')
def getTallas():
    idP = int(request.args.get("txtIdP"))
    tallas = []
    
    ejemplares = Ejemplar.query.filter(Ejemplar.producto_id==idP).order_by(Ejemplar.talla.asc()).all()
    for ejemplar in ejemplares:
        if not ejemplar.talla in tallas:
            tallas.append(ejemplar.talla)
    
    return json.dumps(tallas)

@ejem.route('/getColores')
def getColores():
    idP = int(request.args.get("txtIdP"))
    talla = float(request.args.get("txtTalla"))
    colores = []

    ejemplares = Ejemplar.query.filter(Ejemplar.producto_id==idP, Ejemplar.talla==talla).order_by(Ejemplar.color.asc()).all()
    for ejemplar in ejemplares:
        if not ejemplar.color in colores:
            colores.append(ejemplar.color)
    
    return json.dumps(colores)

@ejem.route('/getCantidad')
def getCantidad():
    idP = int(request.args.get("txtIdP"))
    talla = float(request.args.get("txtTalla"))
    color = request.args.get("txtColor")
    result = {}

    ejemplar = Ejemplar.query.filter(Ejemplar.producto_id==idP, Ejemplar.talla==talla, Ejemplar.color==color).first()
    result["cantidad"] = ejemplar.cantidad
    
    return json.dumps(result)

@ejem.route('/guardar', methods=["POST"])
def guardar():
    idP = int(request.form.get("txtIdP"))
    talla = float(request.form.get("lstTalla"))
    color = request.form.get("txtColor")
    cantidad = int(request.form.get("txtCantidad"))

    tmp = Ejemplar.query.filter(Ejemplar.producto_id==idP, Ejemplar.talla==talla, Ejemplar.color==color).first()
    if tmp != None:
        flash("Ya existe un ejemplar para esa talla y color", "warning")
        return redirect("getByProducto?txtIdP="+str(idP))

    if request.form.get("txtId") != "":
        id=request.form.get("txtId")
        ejemplar = Ejemplar.query.filter_by(id=id).first()
        ejemplar.talla = talla
        ejemplar.color = color
        ejemplar.cantidad = cantidad
        db.session.add(ejemplar)
    else:
        ejemplar = Ejemplar(producto_id=idP, talla=talla, color=color, cantidad=cantidad)
        db.session.add(ejemplar)

    flash("Ejemplar guardado exitosamente", "success")
    db.session.commit()
    return redirect("getByProducto?txtIdP="+str(idP))

@ejem.route('/eliminar', methods=["POST"])
def eliminar():
    id = request.form.get("txtId")
    ejemplar = Ejemplar.query.filter_by(id=id).first()
    result = {"result":ejemplar.producto_id}
    db.session.delete(ejemplar)
    db.session.commit()
    return json.dumps(result)