from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector

from usuario.usuario_api import usuario_router
from tablero.tablero_api import tablero_router

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-development:3306/testapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

def create_app():
    from usuario.rol import Rol
    from tarea.estado import Estado
    from tarea.tarea import Tarea
    from tablero.tablero import Tablero
    from usuario.usuario import Usuario
    from tablero.transicion import Transicion
    db.create_all()

app.register_blueprint(usuario_router, url_prefix='/users')
app.register_blueprint(tablero_router, url_prefix='/tableros')


@app.route('/', methods=['GET'])
def index():
    estado_prueba = Estado()
    estado_prueba.nombre = 'TO DO'

    estado_prueba_2 = Estado()
    estado_prueba_2.nombre = 'DOING'

    tarea_prueba = Tarea()
    tarea_prueba.estado = estado_prueba
    tarea_prueba.titulo = 'primera tarea'
    tarea_prueba.descripcion = 'una muy muy larga descripcion'

    transicion_prueba = Transicion()
    transicion_prueba.tarea = tarea_prueba
    transicion_prueba.estado_inicial = estado_prueba
    transicion_prueba.estado_final = estado_prueba_2

    tablero_prueba = Tablero('tablerito')
    tablero_prueba.tareas = [tarea_prueba]
    tablero_prueba.transiciones = [transicion_prueba]

    rol_prueba = Rol()
    rol_prueba.nombre = 'QA'

    usuario_prueba = Usuario()
    usuario_prueba.nombre = 'nicolas'
    usuario_prueba.edad = 17
    usuario_prueba.roles = [rol_prueba]
    usuario_prueba.tableros = [tablero_prueba]

    db.session.add(usuario_prueba)
    db.session.commit()
    return jsonify({'message': 'Welcome to my APIIIIII'})


if __name__ == "__main__":
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
