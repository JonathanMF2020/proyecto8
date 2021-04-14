from flask import Blueprint, render_template, request, redirect,url_for, make_response, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,login_required,roles_accepted
from . import db
from .models import Proveedor
import json


#No sirve UwU
proveedores = Blueprint('proveedores', __name__, url_prefix="/proveedores")

@proveedores.route('/', methods=['GET'])
@roles_accepted('admin','surtidor')
def getAll():    
    proveedores =  db.session.query(Proveedor).filter(Proveedor.estatus == 1).all()    
    return render_template('proveedores.html', proveedores=proveedores)


@proveedores.route('/guardar', methods=['GET', 'POST'])
def guardar():            
    if request.form.get("txtId") != "":
        id = request.form.get("txtId")        
        proveedor = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
        proveedor.nombre_empresa = request.form.get('txtNombreEmpresa')
        proveedor.email = request.form.get('txtEmail')
        proveedor.telefono = request.form.get('txtTelefono')
        proveedor.direccion = request.form.get('txtDireccion')
        proveedor.contacto = request.form.get('txtContacto')
        proveedor.RFC = request.form.get('txtRFC')
        db.session.add(proveedor)
        db.session.commit()
        flash("Proveedor modificado exitosamente", "success")
    else:
        prov = Proveedor()
        prov.nombre_empresa = request.form.get('txtNombreEmpresa')
        prov.email = request.form.get('txtEmail')
        prov.estatus = 1
        prov.telefono = request.form.get('txtTelefono')
        prov.direccion = request.form.get('txtDireccion')
        prov.contacto = request.form.get('txtContacto')
        prov.RFC = request.form.get('txtRFC')
        db.session.add(prov)
        db.session.commit()
        flash("Proveedor agregado exitosamente", "success")            
    return redirect(url_for('proveedores.getAll'))



@proveedores.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    id = int(request.form.get("txtId"))
    prov = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
    prov.estatus = 0
    db.session.add(prov)
    db.session.commit()
    response = {"result":"OK"}
    return json.dumps(response)
    
