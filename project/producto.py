from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Producto, DetalleProducto
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
    detalles = json.loads(request.form.get("detalles"))
    print(detalles)
    print(idt)
    if request.form.get("txtId") != "":
        data = request.detalles
        print(data)
        print(type(data))
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
        nombre = request.form.get("txtNombre")
        descripcion = request.form.get("txtDescripcion")
        precio = request.form.get("txtPrecio")
        producto = Producto(nombre=nombre,descripcion=descripcion,precio=precio,cantidad=0,estatus=1)
        print(type(detalles))
        pro = db.session.query(Producto).order_by(Producto.id.desc()).first()
        idPro = pro.id
        for r in detalles :
            print(r)
            materias = detalles[0]
            print(materias)
            print(type(materias))
            matee = materias['materia']
            print(matee)
            print(type(matee))
            idM = matee['id']
            print("idMaterial"+str(idM))
            print("idProducto"+str(idPro))
            cantidad = materias['cantidad']
            print("Cantidad"+cantidad)
            productito = DetalleProducto(
                cantidad = float(cantidad),
                materia_id = int(idM),
                producto_id = idPro
            )
            db.session.add(productito)
            db.session.commit()

        db.session.add(producto)
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
    db.session.add(detallespro)
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
    response = {"result":"OK"}
    return json.dumps(response)