
from flask import Blueprint, render_template,request
from flask.helpers import url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from werkzeug.utils import redirect
from . import db
from .models import MateriaPrima

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/materia/', methods=['GET', 'POST'])
def material_index():
    if request.method == "GET":
        materias = db.session.query(MateriaPrima).filter(MateriaPrima.estatus == 1).all()
        return render_template('materia/index.html',materias=materias)
    
@main.route('/materia/add', methods=['GET', 'POST'])
def material_add():
    if request.method == "GET":
        return render_template('materia/add.html')
    else:
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        unidad = request.form.get("unidad")
        materia = MateriaPrima(nombre=nombre,precio=precio,cantidad=cantidad,unidad=unidad,estatus=1)
        db.session.add(materia)
        db.session.commit()
        return redirect(url_for('main.material_index'))

@main.route('/materia/delete', methods=['GET', 'POST'])
def material_delete():
    if request.method == "POST":
        id = int(request.form.get("id"))
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        materia.estatus = 0
        db.session.add(materia)
        db.session.commit()
        return "Exito"
    
@main.route('/materia/edit', methods=['GET', 'POST'])
def material_edit():
    if request.method == "GET":
        id = request.args.get('id')
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        return render_template('materia/edit.html',materia=materia)
    else:
        id = int(request.form.get("id"))
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        unidad = request.form.get("unidad")
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        materia.nombre = nombre
        materia.precio = precio
        materia.cantidad = cantidad
        materia.unidad = unidad
        db.session.add(materia)
        db.session.commit()
        return redirect(url_for('main.material_index'))
    

@main.route('/admin')
@roles_required('admin')
def admin():
    return render_template('profile.html', name=current_user.name)