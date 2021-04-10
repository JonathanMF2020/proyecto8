from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_security import UserMixin,RoleMixin
import json
import datetime

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
"""
class Venta(db.Model):
    __tablename__ = "venta"
    id = db.Column(db.Integer,primary_key=True)
    cliente_id = db.Column(db.Integer(),db.ForeignKey('cliente.id'))
    cliente = db.relationship(MateriaPrima,backref="clientess")
    precio = db.Column(db.Float)
    date = db.Column(db.DateTime)
    comentarios = db.Column(db.String(200))
    estatus = db.Column(db.Integer)

    def toJson(self):
        venta = {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "precio": self.precio,
            "date": self.date,
            "comentarios": self.comentarios,
            "estatus": self.estatus
        }
        return json.dumps(venta)

class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"
    id = db.Column(db.Integer,primary_key=True)
    venta_id = db.Column(db.Integer(),db.ForeignKey('venta.id'))
    venta = db.relationship(Producto,backref="ventas")
    producto_id = db.Column(db.Integer(),db.ForeignKey('productos.id'))
    producto = db.relationship(Producto,backref="detalle_productos")
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

class Ejemplar(db.Model):
    __tablename__ = "ejemplar"
    id = db.Column(db.Integer,primary_key=True)
    producto_id = db.Column(db.Integer(),db.ForeignKey('productos.id'))
    producto = db.relationship(Producto,backref="detalle_productos")
    venta_id = db.Column(db.Integer(),db.ForeignKey('venta.id'))
    venta = db.relationship(Producto,backref="ventas")
    talla = db.Column(db.Integer)
    color = db.Column(db.String(200))
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
        """