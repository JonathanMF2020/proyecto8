from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,login_required,roles_accepted
from . import db
from .models import MateriaPrima
import json
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
materias = Blueprint('materias', __name__, url_prefix="/materias")

@materias.route('/')
@roles_accepted('admin','almacenista')
def getAll():
    materias = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).all()
    return render_template('materia.html', materias=materias)

@materias.route('/getAll')
def getJson():
    materias = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).all()
    list_materia = []
    for m in materias:
        list_materia.append(m.toJson())
    return json.dumps(list_materia)

#Agregar/Modificar
@materias.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != "":
        idr = request.form.get("txtId")
        nombre = request.form.get("txtNombre")
        costo = request.form.get("txtCosto")
        cantidad = request.form.get("txtCantidad")
        unidad = request.form.get("lstUnidad")
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).filter(MateriaPrima.id == idr).first()
        materia.nombre = nombre
        materia.costo = costo
        materia.cantidad = cantidad
        materia.unidad = unidad
        db.session.add(materia)
        db.session.commit()
        flash("Materia prima modificada exitosamente", "success")
    else:
        nombre = request.form.get("txtNombre")
        costo = request.form.get("txtCosto")
        cantidad = request.form.get("txtCantidad")
        unidad = request.form.get("lstUnidad")
        materia = MateriaPrima(nombre=nombre,costo=costo,cantidad=cantidad,unidad=unidad,estatus=1)
        db.session.add(materia)
        db.session.commit()
        flash("Materia prima agregada exitosamente", "success")
    
    return redirect(url_for('materias.getAll'))

#Eliminar
@materias.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    materia = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).filter(MateriaPrima.id == id).first()
    materia.estatus = 0
    db.session.add(materia)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)