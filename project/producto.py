from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,login_required,roles_accepted
from . import db
from .models import Producto, DetalleProducto, MateriaPrima
import json

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
productos = Blueprint('productos', __name__, url_prefix="/productos")

@productos.route('/')
@roles_accepted('admin','almacenista')
def getAll():
    productos = db.session.query(Producto).filter(Producto.estatus == 1).all()
    return render_template('productos.html', productos=productos)

#Traer clientes
@productos.route('/getAll')
def getJson():
    productos = db.session.query(Producto).filter(Producto.estatus == 1).all()
    list_producto = []
    for m in productos:
        list_producto.append(m.toJson())
    return json.dumps(list_producto)

@productos.route('/getDetalles')
def getDetalles():
    id = int(request.args.get("txtId"))
    detalles = db.session.query(DetalleProducto).filter(DetalleProducto.producto_id == id).all()
    listaDetalles = []
    for dp in detalles:
        detalle = {}
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == dp.materia_id).first()
        detalle["materia"] = {"id":materia.id, "nombre":materia.nombre, "unidad":materia.unidad}
        detalle["cantidad"] = dp.cantidad
        detalle["producto"] = dp.producto_id
        detalle["id"] = dp.id
        listaDetalles.append(detalle)
    return json.dumps(listaDetalles)

@productos.route('/guardar', methods=["POST"])
def guardar():
    idt = request.form.get("txtId")
    if idt != "":
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
        response = {"result":"OK"}
        return json.dumps(response)
    else:
        nombre = request.form.get("txtNombre")
        descripcion = request.form.get("txtDescripcion")
        precio = request.form.get("txtPrecio")
        producto = Producto(nombre=nombre,descripcion=descripcion,precio=precio,cantidad=0,estatus=1)
        db.session.add(producto)
        detalles = json.loads(request.form.get("detalles"))
        pro = db.session.query(Producto).order_by(Producto.id.desc()).first()
        idPro = pro.id
        for r in detalles :
            materias = r
            matee = materias['materia']
            idM = matee['id']
            cantidad = materias['cantidad']

            productito = DetalleProducto(
                cantidad = float(cantidad),
                materia_id = int(idM),
                producto_id = idPro
            )
            db.session.add(productito)

        db.session.commit()
        response = {"result":"OK"}
        return json.dumps(response)

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

#Eliminar_detalle
@productos.route('/eliminar_detalle', methods=["POST"])
def eliminar_detalle():
    id = int(request.form.get("txtId"))
    detallespro = db.session.query(DetalleProducto).filter(DetalleProducto.id == id).first()
    db.session.delete(detallespro)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)

#Agregar_detalle
@productos.route('/agregar_detalle', methods=["POST"])
def agregar_detalle():
    cantidad = float(request.form.get("txtCantidad"))
    idMateria = int(request.form.get("txtIdMateria"))
    idProducto = int(request.form.get("txtIdProducto"))
    productito = DetalleProducto(
                cantidad = float(cantidad),
                materia_id = int(idMateria),
                producto_id = int(idProducto)
            )
    db.session.add(productito)
    db.session.commit()
    response = {"result":productito.id}

    return json.dumps(response)