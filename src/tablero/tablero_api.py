from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.db import db

from .tablero import Tablero
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

class TableroResource(Resource):
    def get(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = tablero_schema.dump(tablero_actual)
        return result

api.add_resource(TableroResource, '/tableros/<int:tablero_id>', endpoint='tableros_resource')
api.add_resource(TableroListResource, '/tableros', endpoint='tableros_list_resource')
