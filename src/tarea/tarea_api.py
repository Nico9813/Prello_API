from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.db import db

from .tarea import Tarea
from tablero.tablero import Tablero

from main.schemas import TareaSchema

tarea_router = Blueprint('tarea', __name__)

tarea_schema = TareaSchema()

api = Api(tarea_router)

class TareaListResource(Resource):
    def get(self, tablero_id : int):
        tablero = Tablero.get_by_id(tablero_id)
        result = tarea_schema.dump(tablero.tareas, many=True)
        return result

class TareaResource(Resource):
    def get(self, tablero_id : int, tarea_id: int):
        tarea_actual = Tarea.get_by_id(tarea_id)
        if tarea_actual.tablero_id != tablero_id:
            #throw exception
            pass
        result = tarea_schema.dump(tarea_actual)
        return result

api.add_resource(TareaResource, '/tableros/<int:tablero_id>/tareas/<int:tarea_id>/',
                 endpoint='tareas_resource')
api.add_resource(TareaListResource, '/tableros/<int:tablero_id>/tareas',
                 endpoint='tareas_list_resource')
