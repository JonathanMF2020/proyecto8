from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Producto, DetalleProducto, MateriaPrima, Venta,DetalleVenta
import json

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
ventas = Blueprint('ventas', __name__, url_prefix="/ventas")

@ventas.route('/')
def getAll():
    ventas = db.session.query(Venta).filter(Venta.estatus == 1).all()
    return render_template('ventas.html', ventas=ventas)

#Agregar y modificar
@ventas.route('/guardar', methods=["POST"])
def guardar():
    idt = request.form.get("txtId")
    if idt != "":
        idP = request.form.get("txtId")
        cliente_id = request.form.get("lstCliente")
        date = request.form.get("txtFecha")
        comentarios = request.form.get("txtComentarios")
        vent = db.session.query(Venta).filter(Venta.estatus == 1).filter(Venta.id == idP).first()
        vent.cliente_id = cliente_id
        vent.date = date
        vent.comentarios = comentarios
        db.session.add(vent)
        db.session.commit()
        response = {"result":"OK"}
        return json.dumps(response)
    else:
        idCliente = request.form.get("txtClienteI")
        fecha = request.form.get("txtFecha")
        precioUnitario = request.form.get("txtPrecioUnitario")
        detalles = json.loads(request.form.get("detallesVenta"))
        suma = 0
        for r in detalles :
            producto = r
            cantidad = producto['cantidad']
            prud = producto['producto']
            idP = prud['id']
            producto = db.session.query(Producto).filter(Producto.id == idP).first()
            multi=int(producto.precio)*int(cantidad)
            suma=suma+multi

        comentarios = request.form.get("txtComentarios")
        venta = Venta(cliente_id=idCliente,precio=suma,date=fecha,comentarios=comentarios,estatus=1)
        db.session.add(venta)
        
        venta = db.session.query(Venta).order_by(Venta.id.desc()).first()
        idVenta = venta.id
        for r in detalles :
            producto = r
            
            suma=suma+multi
            prud = producto['producto']
            talla = producto['talla']
            color = producto['color']
            idP = prud['id']
            produc = db.session.query(Producto).filter(Producto.estatus == 1).filter(Producto.id == idP).first()

            preciounir = produc.precio
            cantidad = producto['cantidad']
            multi=int(preciounir)*int(cantidad)
            productitoDeta = DetalleVenta(
                venta_id = int(idVenta),
                producto_id = idP,
                talla = talla,
                color = color,
                cantidad = float(cantidad),
                precio_unitario = produc.precio
            )
            db.session.add(productitoDeta)
        db.session.commit()
        response = {"result":"OK"}
        return json.dumps(response)

#Eliminar
@ventas.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    ventas = db.session.query(Venta).filter(Venta.estatus == 1).filter(Venta.id == id).first()
    ventas.estatus = 0
    db.session.add(ventas)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)

#Eliminar_detalle
@ventas.route('/eliminar_detalle', methods=["POST"])
def eliminar_detalle():
    id = int(request.form.get("txtId"))
    detallesventa = db.session.query(DetalleVenta).filter(DetalleVenta.id == id).first()
    suma= detallesventa.cantidad * detallesventa.precio_unitario
    idV=detallesventa.venta_id
    ventaww = db.session.query(Venta).filter(Venta.id == idV).first()
    cantoo=ventaww.precio
    sumaFin = int(cantoo)-int(suma)
    ventaww.precio= sumaFin
    db.session.delete(detallesventa)
    vent = db.session.query(Venta).filter(Venta.estatus == 1).filter(Venta.id == idV).first()
    vent.precio = sumaFin
    db.session.add(vent)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)

#Ver_detalle_venta
@ventas.route('/getDetalles')
def getDetalles():
    id = int(request.args.get("txtId"))
    detalles = db.session.query(DetalleVenta).filter(DetalleVenta.venta_id == id).all()
    listaDetalles = []
    for dp in detalles:
        detalle = {}
        detalle["venta_id"] = dp.venta_id
        pros = db.session.query(Producto).filter(Producto.id == dp.producto_id).first()

        detalle["producto"] = {"id":pros.id, "nombre":pros.nombre, "descripcion":pros.descripcion, "precio":pros.precio, "cantidad":pros.cantidad}
        detalle["talla"] = dp.talla
        detalle["color"] = dp.color
        detalle["cantidad"] = dp.cantidad
        detalle["precio_unitario"] = dp.precio_unitario
        detalle["id"] = dp.id
        listaDetalles.append(detalle)
    return json.dumps(listaDetalles)

#Agregar_detalle
@ventas.route('/agregar_detalle', methods=["POST"])
def agregar_detalle():
    idV = request.form.get("txtIdVenta")
    idV = request.form.get("txtIdVenta")
    precioProducto = request.form.get("txtPrecioProducto")
    idP = request.form.get("txtProducto")
    talla = request.form.get("txtTalla")
    color = request.form.get("txtColor")
    cantidad = request.form.get("txtCantidad")
    idVentas = request.form.get("txtIdVenta")
    idProdi = request.form.get("txtIdProducto")
    productitoDeta = DetalleVenta(
                venta_id = idVentas,
                producto_id = idProdi,
                talla = talla,
                color = color,
                cantidad = cantidad,
                precio_unitario = precioProducto
        )
    db.session.add(productitoDeta)
    db.session.commit()
    idtut=productitoDeta.id
    suma = int(cantidad)*int(precioProducto)
    venta = db.session.query(Venta).filter(Venta.id == idV).first()
    venta.precio = (venta.precio +suma)
    db.session.add(venta)
    db.session.commit()
    response = {"result":idtut}
    return json.dumps(response)
