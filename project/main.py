from flask import Blueprint, render_template,request
from flask.helpers import url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from werkzeug.utils import redirect
from . import db
from .models import Cliente

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/cliente/', methods=['GET', 'POST'])
def cliente_index():
    if request.method == "GET":
        cliente = db.session.query(Cliente).filter(Cliente.estatus == 1).all()
        return render_template('cliente/index.html', clientes=cliente)
    
@main.route('/cliente/add', methods=['GET', 'POST'])
def cliente_add():
    if request.method == "GET":
        return render_template('cliente/add.html')
    else:
        nombre_empresa = request.form.get("nombre_empresa")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        rfc = request.form.get("rfc")
        direccion = request.form.get("direccion")
        contacto = request.form.get("contacto")
        cliente = Cliente(nombre_empresa=nombre_empresa, email=email, telefono=telefono, rfc=rfc,
                            direccion=direccion, contacto=contacto,estatus=1)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('main.cliente_index'))

@main.route('/cliente/delete', methods=['GET', 'POST'])
def cliente_delete():
    if request.method == "POST":
        id = int(request.form.get("id"))
        cliente = db.session.query(Cliente).filter(Cliente.id == id).first()
        cliente.estatus = 0
        db.session.add(cliente)
        db.session.commit()
        return "Exito"
    
@main.route('/cliente/edit', methods=['GET', 'POST'])
def cliente_edit():
    if request.method == "GET":
        id = request.args.get('id')
        cliente = db.session.query(Cliente).filter(Cliente.id == id).first()
        return render_template('cliente/edit.html', cliente=cliente)
    else:
        id = int(request.form.get("id"))
        nombre_empresa = request.form.get("nombre_empresa")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        rfc = request.form.get("rfc")
        direccion = request.form.get("direccion")
        contacto = request.form.get("contacto")
        cliente = db.session.query(Cliente).filter(Cliente.id == id).first()
        cliente.nombre_empresa = nombre_empresa
        cliente.email = email
        cliente.telefono = telefono
        cliente.rfc = rfc
        cliente.direccion = direccion
        cliente.contacto = contacto
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('main.cliente_index'))
    

@main.route('/admin')
@roles_required('admin')
def admin():
    return render_template('profile.html', name=current_user.name)