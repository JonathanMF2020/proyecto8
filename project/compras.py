from .models import DetalleCompra

compras = Blueprint('compras', __name__, url_prefix="/compras")

@compras.route('/')
def getAll():
    materias = db.session.query(DetalleCompra).filter(DetalleCompra.estatus == 1).all()
    return render_template('materia.html', materias=materias)