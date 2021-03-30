from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import MateriaPrima
#from .models import Producto

#nombre del blueprint (abreviado), el prefijo debe ser el nombre del modulo
materias = Blueprint('materias', __name__, url_prefix="/materias")

@materias.route('/')
def getAll():
    materias = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).all()
    return render_template('materia/index.html', clientes=[])

#Agregar/Modificar
@materias.route('/guardar', methods=["POST"])
def guardar():
    #obtener los datos
    if request.form.get("txtId") != None:
        #modificar
        pass
    else:
        #agregar
        pass
    
    #db.session.add(producto)
    #db.session.commit()
    #antes del redirect, enviar un flash
    return redirect("/clientes/")

#Eliminar
@materias.route('/eliminar', methods=["POST"])
def eliminar():
    id = int(request.form.get("txtId"))
    #producto = Producto.query.filter_by(id=id)
    #db.session.delete(producto)
    #db.session.commit()
    #antes del redirect, enviar un flash
    return redirect("/clientes/")