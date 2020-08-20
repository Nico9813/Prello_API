from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector

from usuario.usuario_api import usuario_router
from tablero.tablero_api import tablero_router

from .autentificacion import AuthError, requires_auth
from flask_cors import cross_origin

AUTH0_DOMAIN = 'dev-jx8fysvq.us.auth0.com'
API_AUDIENCE = 'https://api-prello/v1'
ALGORITHMS = ["RS256"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-development:3306/testapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def create_app():
    from usuario.rol import Rol
    from tarea.estado import Estado
    from tarea.tarea import Tarea
    from tablero.tablero import Tablero
    from usuario.usuario import Usuario
    from tablero.transicion_realizada import Transicion_realizada
    from evento.observable import Observable
    from evento.evento import Evento
    from evento.accion import Accion_mock
    from evento.subscripcion import Subscripcion
    from workflow.workflow import Workflow
    from workflow.transicion_posible import Transicion_posible
    db.create_all()

app.register_blueprint(usuario_router, url_prefix='/users')
app.register_blueprint(tablero_router, url_prefix='/tableros')


@app.route('/private', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    return jsonify({'message': 'Welcome to my APIIIIII PRIVATE'})

@app.route('/', methods=['GET'])
def index():
    from usuario.rol import Rol
    from tarea.estado import Estado
    from tarea.tarea import Tarea
    from tablero.tablero import Tablero
    from usuario.usuario import Usuario
    from tablero.transicion_realizada import Transicion_realizada
    from evento.observable import Observable
    from evento.evento import Evento
    from evento.accion import Accion_mock
    from evento.subscripcion import Subscripcion
    from workflow.workflow import Workflow
    from workflow.transicion_posible import Transicion_posible

    User : Usuario = Usuario('Rodrigo')
    QA : Rol = Rol('QA')

    TODO : Estado = Estado('TODO')
    DOING : Estado = Estado('DOING')
    
    Accion_tablero : Accion_mock = Accion_mock()
    Accion_tarea : Accion_mock = Accion_mock()
    Accion_estado : Accion_mock = Accion_mock()

    Primer_tarea : Tarea = Tarea(TODO, 'Tituloo', 'Descripcion larga')

    Proyecto : Tablero = Tablero('Proyecto')
    Proyecto.agregar_tarea(Primer_tarea)

    User.agregar_tablero(Proyecto)
    User.subscribirse(Evento.CREACION_TARJETA, Proyecto, Accion_tablero)
    User.subscribirse(Evento.CAMBIO_DE_ESTADO, Primer_tarea, Accion_tarea)
    User.subscribirse(Evento.INGRESO_TARJETA, TODO, Accion_estado)


    accion_transicion : Accion_mock = Accion_mock()

    workflow: Workflow = Workflow()
    Proyecto.workflow = workflow

    workflow.agregar_accion_entre_estados(TODO, DOING, accion_transicion)
    Proyecto.ejecutar_transicion(Primer_tarea, DOING)

    db.session.add(User)
    db.session.commit()
    return jsonify({'message': 'Welcome to my APIIIIII'})


#if __name__ == "__main__":
create_app()
app.run()

# CASOS DE USO

# - CREAR UN USUARIO
# - CREAR UN TABLERO ( ASIGNACION EN MODO ADMIN )
# - INVITAR A UN TABLERO ( ASIGNACION EN MODO INVITADO ) HACE FALTA LA DIFERENCIACION????
# - CRUD LISTA
# - CRUD TAREA
# - CREAR WORKFLOW
# - AGREGAR INTERACCION WORKFLOW { ID_ESTADO_INICIAL, ID_ESTADO_FINAL , ID_ACCION }
# - LISTAR ACCIONES DISPONIBLES
# - MOSTRAR ACCION ESPECIFICA
# - MOVER TAREA

# SESSION
# - algun dato para obtener el usuario logueado de la base de datos

# END POINTS API

# USUARIO
# - POST    perfil/                                                      --> NUEVO USUARIO
# - GET     perfil/<id>                                                  --> OBTENER USUARIO
# - GET     perfil                                                       --> OBTENER USUARIO PROPIO
# - PUT     perfil                                                       --> MODIFICAR USUARIO PROPIO
# - DELETE  perfil                                                       --> BORRAR USUARIO PROPIO

# TABLEROS USUARIO
# - GET     tableros                                                    --> OBTENER TODOS LOS TABLEROS DE USUARIO ID
# - POST    tableros                                                    --> CREAR TABLERO COMO ADMINISTRADOR EN EL USUARIO LOGUEADO
# - POST    tableros/<id_tablero>/shared                                --> ASIGNA COMO INVITADO UN TABLERO AL USUARIO LOGUEADO
# - GET     tableros/<id_tablero>                                       --> OBTENER TABLERO ID_TABLERO
# - PUT     tableros/<id_tablero>                                       --> MODIFICAR TABLERO ID_TABLERO
# - DELETE  tableros/<id_tablero>                                       --> BORRAR TABLERO ID_TABLERO

# LISTAS TABLERO USUARIO
# - GET     tablero/<id_tablero>/estados                                --> OBTENER TODAS LAS estados DE UN TABLERO ????
# - POST    tablero/<id_tablero>/estados                                --> CREAR LISTA ID
# - GET     tablero/<id_tablero>/estados/<id>                           --> OBTENER LISTA ID ????
# - PUT     tablero/<id_tablero>/estados/<id>                           --> MODIFICAR LISTA ID
# - DELETE  tablero/<id_tablero>/estados/<id>                           --> BORRAR LISTA ID

# TAREAS
# - GET     tablero/<id_tablero>/estados/<id>/tareas                    --> OBTENER TODAS LAS TAREAS DE UNA LISTA
# - POST    tablero/<id_tablero>/estados/<id>/tareas                    --> CREAR UNA TAREA ID
# - POST    tablero/<id_tablero>/estados/<id>/tareas/<id>               --> CAMBIAR DE ESTADO UNA TAREA (QUERY PARAMS NUEVO ESTADO)
# - GET     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> OBTENER POSIBLES ESTADOS DESTINO DE UNA TAREA
# - GET     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> OBTENER UNA TAREA ID ????
# - PUT     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> MODIFICAR TAREA ID
# - DELETE  tablero/<id_tablero>/estados/<id>/tareas/<id>               --> BORRAR TAREA ID

# ACCIONES
# - GET     acciones/                                                   --> OBTENER ACCIONES DISPONIBLES
# - GET     acciones/<id>                                               --> OBTENER ACCION ID

# WORKFLOW
# - GET     tableros/<id_tablero>/workflows                             --> OBTENER TODOS LOS WORKFLOWS DE UN TABLERO
# - POST    tableros/<id_tablero>/workflows                             --> CREAR WORKFLOW EN UN TABLERO
# - GET     tableros/<id_tablero>/workflows/<id>                        --> OBTENER WORKFLOW ID
# - PUT     tableros/<id_tablero>/workflows/<id>                        --> MODIFICAR WORKFLOW ID
# - DELETE  tableros/<id_tablero>/workflows/<id>                        --> BORRAR WORKFLOW ID
