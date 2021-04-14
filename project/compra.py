from .models import Compra,Proveedor,DetalleCompra,MateriaPrima
from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security.decorators import roles_required,login_required,roles_accepted
from . import db
import json

compras = Blueprint('compras', __name__, url_prefix="/compras")

@compras.route('/')
@roles_accepted('admin','surtidor')
def getAll():
    compras = db.session.query(Compra).filter(Compra.estatus != 0).all()
    proveedor = db.session.query(Proveedor).filter(Proveedor.estatus == 1).all()
    return render_template('compras/compras.html', compras=compras,proveedor=proveedor)

#Agregar/Modificar
@compras.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != "":
        compra = db.session.query(Compra).filter(Compra.id == request.form.get("txtId")).first
        compra.comentarios = request.form.get("txtComentario")
        compra.proveedor = request.form.get("slctProveedor")
        db.session.add(compra)
        db.session.commit()        
        flash("Compra modificada exitosamente", "success") 
    else:
        comentario = request.form.get("txtComentario")
        proveedor = request.form.get("slctProveedor")
        compra = Compra(proveedor_id=proveedor,comentarios=comentario,estatus=1,precio=0)
        db.session.add(compra)
        db.session.commit()
        flash("Compra agregada exitosamente", "success")
    
    return redirect(url_for('compras.getAll'))

#Ver/Ver
@compras.route('/ver', methods=["POST","GET"])
def ver():
    #obtener los datos
    if request.method == "GET":
        id = request.args.get('id')
        detalles = db.session.query(DetalleCompra).filter(DetalleCompra.compra_id == id).all()
        materias = db.session.query(MateriaPrima).all()
        
        return render_template('compras/ver.html',detalles=detalles,materias=materias,id=id)
    else:
        return "1"

#Ver/Ver
@compras.route('/verguardar', methods=["POST"])
def verguardar():
    id = request.form.get("txtId")
    materia = request.form.get("slctMateria")
    cantidad = float(request.form.get("txtCantidad"))
    precio = float(request.form.get("txtPrecio"))
    detalle = DetalleCompra(materia_id=materia,compra_id=id,cantidad=cantidad,precio_unitario=precio)
    db.session.add(detalle)
    db.session.commit()
    compra = db.session.query(Compra).filter(Compra.id == id).first()
    compra.precio += (precio*cantidad)
    db.session.add(compra)
    db.session.commit()
    flash("Detalle de compra agregada exitosamente", "success")
    detalles = db.session.query(DetalleCompra).all()
    materias = db.session.query(MateriaPrima).all()
    id = request.args.get('id')
    return render_template('compras/ver.html',detalles=detalles,materias=materias,id=id)


@compras.route('/eliminarDetalle', methods=["POST"])
def eliminarDetalle():
    id = int(request.form.get("txtId"))
    detalle = db.session.query(DetalleCompra).filter(DetalleCompra.id == id).first()
    percioresa = (detalle.precio_unitario*detalle.cantidad)
    db.session.delete(detalle)    
    db.session.commit()
    compra = db.session.query(Compra).filter(Compra.id == detalle.compra_id).first()
    compra.precio -= percioresa
    db.session.add(compra)    
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)

    
@compras.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    compra = db.session.query(Compra).filter(Compra.id == id).first()
    compra.estatus = 0
    detalle = db.session.query(DetalleCompra).filter(DetalleCompra.compra_id == compra.id).all()
    for det in detalle:
        db.session.delete(det)
    db.session.add(compra)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)

@compras.route('/terminar', methods=["POST"])
def terminar():
    id = int(request.form.get("id"))
    compra = db.session.query(Compra).filter(Compra.id == id).first()
    compra.estatus = 2
    db.session.add(compra)
    detalle = db.session.query(DetalleCompra).filter(DetalleCompra.compra_id == compra.id).all()
    for det in detalle:
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == det.materia_id).first()
        materia.cantidad += det.cantidad
        db.session.add(materia)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)
    
