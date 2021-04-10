import os
from flask import Flask
from flask_security import Security,SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .models import User, Role
userDataStore = SQLAlchemyUserDatastore(db,User,Role)

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/proyecto8'
    app.logger.debug("Conecto a la base de datos")
    app.config['SECURITY_PASSWORD_SALT'] = 'thissecretssalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        app.logger.debug("Genero tablas en caso de necesitarlo")        
        
    security = Security(app,userDataStore)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .materia import materias as materia_blueprint
    app.register_blueprint(materia_blueprint)
    from .compra import compras as compras_blueprint
    app.register_blueprint(compras_blueprint)
    from .proveedor import proveedores as proveedor_blueprint
    app.register_blueprint(proveedor_blueprint)
    app.logger.debug("Inicio la aplicacion")
    return app
