from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.db import db

from .tablero import Tablero
from tarea.tarea import Tarea
from usuario.usuario import Usuario
from main.schemas import TableroSchema

tablero_router = Blueprint('tablero', __name__)

tablero_schema = TableroSchema()

api = Api(tablero_router)

class TableroListResource(Resource):
    def get(self):
        usuario_actual = Usuario.get_by_id(get_id_usuario_actual())
        result = tablero_schema.dump(usuario_actual.tableros, many=True)
        return result
    
    def post(self):
        data = request.get_json()
        tablero_nuevo_dicc = tablero_schema.load(data)
        usuario_actual = Usuario.get_by_id(get_id_usuario_actual())

        tablero_nuevo = Tablero(tablero_nuevo_dicc['nombre'])

        usuario_actual.agregar_tablero(tablero_nuevo)
        usuario_actual.save()

        result = tablero_schema.dump(tablero_nuevo)
        return result

class TableroResource(Resource):
    def get(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = tablero_schema.dump(tablero_actual)
        return result
    
    def delete(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = tablero_schema.dump(tablero_actual)

        #Borrar todas las tareas asociadas a este tablero
        tareas_a_borrar = Tarea.simple_filter(tablero_id=tablero_id)

        for tarea in tareas_a_borrar:
            tarea.delete()

        tablero_actual.delete()
        return result

api.add_resource(TableroResource, '/tableros/<int:tablero_id>', endpoint='tableros_resource')
api.add_resource(TableroListResource, '/tableros', endpoint='tableros_list_resource')
