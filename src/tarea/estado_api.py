from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.excepciones import ResourceNotFoundError, PermissionError
from main.db import db

from tarea.estado import Estado

from main.schemas import EstadoSchema

estado_router = Blueprint('estado', __name__)

estado_schema = EstadoSchema()

api = Api(estado_router)

def get_estado_actual(tablero_id : int, estado_id : int):
    estado_actual = Estado.get_by_id(estado_id)
    if estado_actual == None:
        raise ResourceNotFoundError(
            "error: El estado " + str(estado_id) + " no existe")
    if estado_actual.tablero_id != tablero_id:
        raise PermissionError(
            "error: El estado " + str(estado_id) + " no pertenece al tablero " + str(tablero_id))
    return estado_actual

class EstadoListResource(Resource):
    def get(self, tablero_id: int):
        estados_actuales = Estado.simple_filter(tablero_id=tablero_id)
        result = estado_schema.dump(estados_actuales, many=True)
        return result
    
    def post(self, tablero_id : int):
        data = request.get_json()
        estado_nuevo_dicc = estado_schema.load(data)
        estado_nuevo = Estado(estado_nuevo_dicc['nombre'])
        estado_nuevo.tablero_id = tablero_id
        estado_nuevo.save()
        result = estado_schema.dump(estado_nuevo)
        return result, 201

class EstadoResource(Resource):
    def get(self, tablero_id : int, estado_id : int):
        estado_actual = get_estado_actual(tablero_id, estado_id)
        result = estado_schema.dump(estado_actual)
        return result

api.add_resource(EstadoResource, '/tableros/<int:tablero_id>/estados/<int:estado_id>/',
                 endpoint='estado_resource')
api.add_resource(EstadoListResource, '/tableros/<int:tablero_id>/estados',
                 endpoint='estado_list_resource')
