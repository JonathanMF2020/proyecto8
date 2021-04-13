from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_security import UserMixin,RoleMixin
import datetime
import json

users_roles = db.Table('users_roles',
    db.Column('userId',db.Integer,db.ForeignKey('user.id'))  ,
    db.Column('roleId',db.Integer,db.ForeignKey('role.id'))                    
)

class User(UserMixin, db.Model):
    """User account model."""
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',
        secondary=users_roles,
        backref=db.backref('user',lazy='dynamic')                        
    )

class Role(RoleMixin, db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
class MateriaPrima(db.Model):
    __tablename__ = "materia_prima"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50))
    costo  = db.Column(db.Float)
    cantidad = db.Column(db.Float)
    unidad = db.Column(db.String(50))
    estatus = db.Column(db.Integer)

    def toJson(self):
        lis = {
            "id": self.id,
            "nombre": self.nombre,
            "costo": self.costo,
            "cantidad": self.cantidad,
            "unidad": self.unidad,
        }
        return json.dumps(lis)

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer,primary_key=True)
    nombre_empresa = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(250))
    contacto = db.Column(db.String(150))
    rfc = db.Column(db.String(50))
    estatus = db.Column(db.Integer)

    def toJson(self):
        lis = {
            "id": self.id,
            "nombre_empresa": self.nombre_empresa,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "contacto": self.contacto,
            "rfc": self.rfc
        }
        return json.dumps(lis)

class Proveedor(db.Model):
    __tablename__ = "proveedor"    
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(25))
    direccion = db.Column(db.String(250))
    contacto = db.Column(db.String(250))
    RFC = db.Column(db.String(125))
    estatus = db.Column(db.Integer, default=1)

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column(db.Integer,primary_key=True)
    proveedor_id = db.Column(db.Integer,db.ForeignKey('proveedor.id_proveedor'))
    precio = db.Column(db.Float)
    fecha_compra = db.Column(db.DateTime,default=datetime.date.today())
    comentarios = db.Column(db.String(50))
    estatus = db.Column(db.Integer)
    proveedor = db.relationship(Proveedor,backref="proveedor")
class DetalleCompra(db.Model):
    __tablename__ = "detalle_compra"
    id = db.Column(db.Integer,primary_key=True)
    materia_id = db.Column(db.Integer,db.ForeignKey('materia_prima.id'))
    compra_id = db.Column(db.Integer,db.ForeignKey('compra.id'))
    cantidad = db.Column(db.Float)
    precio_unitario = db.Column(db.Float)
    materia = db.relationship(MateriaPrima,backref="materia_prima")
    compra = db.relationship(Compra,backref="compra")

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float)
    cantidad = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    detalles = relationship('MateriaPrima', secondary='detalle_producto')

    def toJson(self):
        pro = {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "estatus": self.estatus,
        }
        return json.dumps(pro)

class DetalleProducto(db.Model):
    __tablename__ = "detalle_producto"
    id = db.Column(db.Integer,primary_key=True)
    producto_id = db.Column(db.Integer(),db.ForeignKey('productos.id'))
    producto = db.relationship(Producto,backref="detalle_productos")
    materia_id = db.Column(db.Integer(),db.ForeignKey('materia_prima.id'))
    materia = db.relationship(MateriaPrima,backref="detalle_productos")
    cantidad = db.Column(db.Float)

    def toJson(self):
        prode = {
            "id": self.id,
            "producto_id": self.producto_id,
            "materia_id": self.materia_id,
            "cantidad": self.cantidad
        }
        return json.dumps(prode)

class Ejemplar(db.Model):
    __tablename__ = "ejemplar"
    id = db.Column(db.Integer,primary_key=True)
    producto_id = db.Column(db.Integer(),db.ForeignKey('productos.id'))
    producto = db.relationship(Producto, backref="ejemplar")
    talla = db.Column(db.Float)
    color = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)

    def toJson(self):
        dictEjemplar = {
            "id": self.id,
            "producto_id": self.producto_id,
            "talla": self.talla,
            "color": self.color,
            "cantidad": self.cantidad
        }
        return dictEjemplar
class Venta(db.Model):
    __tablename__ = "venta"
    id = db.Column(db.Integer,primary_key=True)
    cliente_id = db.Column(db.Integer(),db.ForeignKey('cliente.id'))
    cliente = db.relationship(Cliente,backref="clientess")
    precio = db.Column(db.Float)
    date = db.Column(db.Date)
    comentarios = db.Column(db.String(200))
    estatus = db.Column(db.Integer)
    def toJson(self):
        venta = {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "precio": self.precio,
            "date": str(self.date),
            "comentarios": self.comentarios,
            "estatus": self.estatus
        }
        return json.dumps(venta)
class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"
    id = db.Column(db.Integer,primary_key=True)
    venta_id = db.Column(db.Integer(),db.ForeignKey('venta.id'))
    venta = db.relationship(Venta,backref="ventas")
    producto_id = db.Column(db.Integer(),db.ForeignKey('productos.id'))
    producto = db.relationship(Producto,backref="productos")
    talla = db.Column(db.Integer)
    color = db.Column(db.String(200))
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    def toJson(self):
        detalleVenta = {
            "id": self.id,
            "producto_id": self.producto_id,
            "venta_id": self.venta_id,
            "talla": self.talla,
            "color": self.color,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario
        }
        return json.dumps(detalleVenta)