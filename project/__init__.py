import os
from flask import Flask
from flask_security import Security,SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
from .models import User, Role
userDataStore = SQLAlchemyUserDatastore(db,User,Role)

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
<<<<<<< HEAD
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://proyecto:yQ2R$p@A6pTL@127.0.0.1/proyecto8'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/proyecto8'
=======
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/proyecto8'
>>>>>>> origin/Diseño
    app.logger.debug("Conecto a la base de datos")
    app.config['SECURITY_PASSWORD_SALT'] = 'thissecretssalt'
    #Almacenista
    #Surtidor
    #Vendedor
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        userDataStore.find_or_create_role(name="admin",description="Administrador")
        userDataStore.find_or_create_role(name="almacenista",description="Almacenista")
        userDataStore.find_or_create_role(name="surtidor",description="Surtidor")
        userDataStore.find_or_create_role(name="vendedor",description="Vendedor")
        if not userDataStore.get_user('admin@test.com'):
            userDataStore.create_user(name="admin",email='admin@test.com',password=generate_password_hash("1234", method='sha256'))
        if not userDataStore.get_user('almacenista@test.com'):
            userDataStore.create_user(name="almacenista",email='almacenista@test.com',password=generate_password_hash("1234", method='sha256'))
        if not userDataStore.get_user('surtidor@test.com'):
            userDataStore.create_user(name="surtidor",email='surtidor@test.com',password=generate_password_hash("1234", method='sha256'))
        if not userDataStore.get_user('vendedor@test.com'):
            userDataStore.create_user(name="vendedor",email='vendedor@test.com',password=generate_password_hash("1234", method='sha256'))
        db.session.commit()
        userDataStore.add_role_to_user('admin@test.com','admin')
        userDataStore.add_role_to_user('almacenista@test.com','almacenista')
        userDataStore.add_role_to_user('surtidor@test.com','surtidor')
        userDataStore.add_role_to_user('vendedor@test.com','vendedor')
        db.session.commit()
        app.logger.debug("Genero tablas en caso de necesitarlo")      
        
    security = Security(app,userDataStore)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .materia import materias as materias_blueprint
    app.register_blueprint(materias_blueprint)
    from .compra import compras as compras_blueprint
    app.register_blueprint(compras_blueprint)
    from .cliente import cliente as cliente_blueprint
    app.register_blueprint(cliente_blueprint)
<<<<<<< HEAD
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    from .producto import productos as productos_blueprint
    app.register_blueprint(productos_blueprint)
    from .proveedor import proveedores as proveedor_blueprint
    app.register_blueprint(proveedor_blueprint)
=======
    from .producto import productos as productos_blueprint
    app.register_blueprint(productos_blueprint)
    from .ejemplar import ejem as ejemplares_blueprint
    app.register_blueprint(ejemplares_blueprint)
    from .ventas import ventas as ventas_blueprint
    app.register_blueprint(ventas_blueprint)
>>>>>>> origin/Diseño
    app.logger.debug("Inicio la aplicacion")
    return app
