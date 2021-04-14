from .models import Compra,Proveedor,DetalleCompra,MateriaPrima
from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from . import db

compras = Blueprint('compras', __name__, url_prefix="/compras")

@compras.route('/')
def getAll():
    compras = db.session.query(Compra).filter(Compra.estatus == 1).all()
    proveedor = db.session.query(Proveedor).filter(Proveedor.estatus == 1).all()
    return render_template('compras/compras.html', compras=compras,proveedor=proveedor)

#Agregar/Modificar
@compras.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != "":
        compra = db.session.query(Compra).filter(Compra.id == request.form.get("txtId")).first
        compra.precio = request.form.get("txtPrecio")
        compra.comentarios = request.form.get("txtComentario")
        compra.proveedor = request.form.get("slctProveedor")
        db.session.add(compra)
        db.session.commit()        
        flash("Compra modificada exitosamente", "success") 
    else:
        precio = request.form.get("txtPrecio")
        comentario = request.form.get("txtComentario")
        proveedor = request.form.get("slctProveedor")
        print("id prove: -------"+proveedor)
        compra = Compra(proveedor_id=proveedor,precio=precio,comentarios=comentario,estatus=1)
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
    cantidad = request.form.get("txtCantidad")
    precio = request.form.get("txtPrecio")
    detalle = DetalleCompra(materia_id=materia,compra_id=id,cantidad=cantidad,precio_unitario=precio)
    db.session.add(detalle)
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
    db.session.delete(detalle)    
    db.session.commit()
    flash("Detalle eliminado exitosamente", "success")
    return redirect(url_for('compras.getAll'))

    
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
    return redirect(url_for('compras.getAll'))
    
