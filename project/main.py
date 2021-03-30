
from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from .models import Proveedor

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@roles_required('admin')
def admin():
    return render_template('profile.html', name=current_user.name)


@main.route('/proveedores/', methods=['GET'])
def proveedor():    
    
    proveedores =  db.session.query(Proveedor).filter(Proveedor.estatus == 1).all()
    
    return render_template('proveedores.html', proveedores=proveedores)


@main.route('/proveedores/guardar', methods=['GET', 'POST'])
def provAdd():
    prov = Proveedor()
    prov.nombre_empresa = request.form.get('txtNombreEmpresa')
    prov.email = request.form.get('txtEmail')
    prov.telefono = request.form.get('txtTelefono')
    prov.direccion = request.form.get('txtDireccion')
    prov.contacto = request.form.get('txtContacto')
    prov.RFC = request.form.get('txtRFC')
    db.session.add(prov)
    db.session.commit()
    
    return redirect(url_for('main.proveedores'))


@main.route('/proveedores/decidirProveedores', methods=['GET', 'POST'])
def decidirProveedores():
    if request.method == "GET":
        id = request.args.get('id')
        proveedor = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
        return render_template('proveedor/edit.html',proveedor=proveedor)
    else:
        prov = Proveedor()
        prov.nombre_empresa = request.form.get('txtNombreEmpresa')
        prov.email = request.form.get('txtEmail')
        prov.telefono = request.form.get('txtTelefono')
        prov.direccion = request.form.get('txtDireccion')
        prov.contacto = request.form.get('txtContacto')
        prov.RFC = request.form.get('txtRFC')
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for('main.proveedores'))
    

@main.route('/proveedores/eliminarProveedor', methods=['GET', 'POST'])
def eliminarProveedor():
    if request.form.get('btnEliminar') is not None:
        id = int(request.form.get("id"))
        prov = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
        prov.estatus = 0
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for('main.proveedores'))
    
