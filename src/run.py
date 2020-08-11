from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector

from usuario.usuario_api import usuario_router

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-development:3306/testapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

db.create_all()

app.register_blueprint(usuario_router, url_prefix='/users')

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})

if __name__ == "__main__":
    app.run()

# CASOS DE USO

# - CREAR UN USUARIO
# - CREAR UN TABLERO ( ASIGNACION EN MODO ADMIN )
# - INVITAR A UN TABLERO ( ASIGNACION EN MODO INVITADO ) HACE FALTA LA DIFERENCIACION?
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
# - GET     users/                                                      --> OBTENER TODOS LOS USUARIOS ????
# - POST    users/                                                      --> NUEVO USUARIO ?????
# - GET     users/<id>                                                  --> OBTENER USUARIO ID , SE PASA ID????
# - PUT     users/<id>                                                  --> MODIFICAR USUARIO ID , SE PASA ID????
# - DELETE  users/<id>                                                  --> BORRAR USUARIO ID , SE PASA ID????

# TABLEROS USUARIO
# - GET     users/<id>/tableros                                         --> OBTENER TODOS LOS TABLEROS DE USUARIO ID
# - POST    users/<id>/tableros                                         --> CREAR TABLERO DE USUARIO ID
# - GET     users/<id>/tableros/<id_tablero>                            --> OBTENER TABLERO ID_TABLERO
# - PUT     users/<id>/tableros/<id_tablero>                            --> MODIFICAR TABLERO ID_TABLERO
# - DELETE  users/<id>/tableros/<id_tablero>                            --> BORRAR TABLERO ID_TABLERO

# LISTAS TABLERO USUARIO
# - GET     users/<id>/tablero/<id_tablero>/listas                      --> OBTENER TODAS LAS LISTAS DE UN TABLERO ????
# - POST    users/<id>/tablero/<id_tablero>/listas                      --> CREAR LISTA ID
# - GET     users/<id>/tablero/<id_tablero>/listas/<id>                 --> OBTENER LISTA ID ????
# - PUT     users/<id>/tablero/<id_tablero>/listas/<id>                 --> MODIFICAR LISTA ID
# - DELETE  users/<id>/tablero/<id_tablero>/listas/<id>                 --> BORRAR LISTA ID

# TAREAS
# - GET     users/<id>/tablero/<id_tablero>/listas/<id>/estados         --> OBTENER TODAS LAS TAREAS DE UNA LISTA
# - POST    users/<id>/tablero/<id_tablero>/listas/<id>/estados         --> CREAR UNA TAREA ID
# - GET     users/<id>/tablero/<id_tablero>/listas/<id>/estados/<id>    --> OBTENER UNA TAREA ID ????
# - PUT     users/<id>/tablero/<id_tablero>/listas/<id>/estados/<id>    --> MODIFICAR TAREA ID
# - DELETE  users/<id>/tablero/<id_tablero>/listas/<id>/estados/<id>    --> BORRAR TAREA ID

# ACCIONES
# - GET     acciones/                                                   --> OBTENER ACCIONES DISPONIBLES
# - GET     acciones/<id>                                               --> OBTENER ACCION ID

# WORKFLOW
# - GET     users/<id>/tableros/<id_tablero>/workflows                  --> OBTENER TODOS LOS WORKFLOWS DE UN TABLERO
# - POST    users/<id>/tableros/<id_tablero>/workflows                  --> CREAR WORKFLOW EN UN TABLERO
# - GET     users/<id>/tableros/<id_tablero>/workflows/<id>             --> OBTENER WORKFLOW ID
# - PUT     users/<id>/tableros/<id_tablero>/workflows/<id>             --> MODIFICAR WORKFLOW ID
# - DELETE  users/<id>/tableros/<id_tablero>/workflows/<id>             --> BORRAR WORKFLOW ID



