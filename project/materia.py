from flask import Blueprint, render_template, request, redirect,url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from flask import jsonify
from .models import MateriaPrima
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
materias = Blueprint('materias', __name__, url_prefix="/materias")

@materias.route('/')
def getAll():
    materias = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).all()
    return render_template('materia/index.html', materias=materias)

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
    else:
        nombre = request.form.get("txtNombre")
        costo = request.form.get("txtCosto")
        cantidad = request.form.get("txtCantidad")
        unidad = request.form.get("lstUnidad")
        materia = MateriaPrima(nombre=nombre,costo=costo,cantidad=cantidad,unidad=unidad,estatus=1)
        db.session.add(materia)
        db.session.commit()
    return redirect(url_for('materias.getAll'))

#Eliminar
@materias.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("id"))
    materia = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).filter(MateriaPrima.id == id).first()
    materia.estatus = 0
    db.session.add(materia)
    db.session.commit()
    return redirect(url_for('materias.getAll'))