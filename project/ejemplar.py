from flask import Blueprint, render_template, request, redirect, flash
#from flask_security import login_required, current_user
#from flask_security.decorators import roles_required
from . import db
from .models import Producto, Ejemplar, DetalleProducto, MateriaPrima
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
    result = {"result":ejemplar.cantidad}

    return json.dumps(result)

@ejem.route('/guardar', methods=["POST"])
def guardar():
    idP = int(request.form.get("txtIdP"))
    talla = float(request.form.get("lstTalla"))
    color = request.form.get("txtColor")
    cantidad = int(request.form.get("txtCantidad"))
    message="El ejemplar se guardo correctamente"
    status="success"

    if request.form.get("txtId") != "":
        id=request.form.get("txtId")
        ejemplar = Ejemplar.query.filter_by(id=id).first()

        if cantidad > ejemplar.cantidad:
            if restarMaterias(ejemplar.producto_id, (cantidad-ejemplar.cantidad)):
                ejemplar.talla = talla
                ejemplar.color = color
                ejemplar.cantidad = cantidad
                db.session.add(ejemplar)
                db.session.commit()
            else:
                db.session.rollback()
                message="No hay materia prima suficiente para modificar el ejemplar"
                status="warning"
        else:
            message="El campo cantidad no puede disminuir"
            status="warning"
    else:
        tmp = Ejemplar.query.filter(Ejemplar.producto_id==idP, Ejemplar.talla==talla, Ejemplar.color==color).first()
        if tmp != None:
            message="Ya existe un ejemplar para esa talla y color"
            status="warning"
        else:
            ejemplar = Ejemplar(producto_id=idP, talla=talla, color=color, cantidad=cantidad)
            db.session.add(ejemplar)
            if restarMaterias(ejemplar.producto_id, ejemplar.cantidad):
                db.session.commit()
            else:
                db.session.rollback()
                message="No hay materia prima suficiente para insertar el ejemplar"
                status="warning"

    flash(message, status)
    return redirect("getByProducto?txtIdP="+str(idP))

@ejem.route('/eliminar', methods=["POST"])
def eliminar():
    id = request.form.get("txtId")
    ejemplar = Ejemplar.query.filter_by(id=id).first()
    result = {"result":ejemplar.producto_id}
    db.session.delete(ejemplar)
    db.session.commit()
    return json.dumps(result)

def restarMaterias(idP, cantidadE):
    result = True
    detalles = DetalleProducto.query.filter(DetalleProducto.producto_id==idP).all()
    for detalle in detalles:
        cantidadT = detalle.cantidad*cantidadE
        materia = MateriaPrima.query.filter_by(id=detalle.materia_id).first()
        if cantidadT <= materia.cantidad:
            materia.cantidad = materia.cantidad-cantidadT
            db.session.add(materia)
        else:
            result = False
            db.session.rollback()
            break
    return result