from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
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