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

@ejem.route('/guardar', methods=["POST"])
def guardar():
    idP = int(request.form.get("txtIdP"))
    talla = float(request.form.get("lstTalla"))
    color = request.form.get("txtColor")
    cantidad = int(request.form.get("txtCantidad"))

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

def restar(id, cantidad):
    ejemplar = Ejemplar.query.filter_by(id=id)
    ejemplar.cantidad = ejemplar.cantidad-cantidad
    db.session.add(ejemplar)
    db.session.commit()
    result = {"result":"OK"}
    return json.dumps(result)

@ejem.route('/eliminar', methods=["POST"])
def eliminar():
    id = request.form.get("txtId")
    ejemplar = Ejemplar.query.filter_by(id=id).first()
    result = {"result":ejemplar.producto_id}
    db.session.delete(ejemplar)
    db.session.commit()
    return json.dumps(result)