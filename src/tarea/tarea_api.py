from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.excepciones import ResourceNotFoundError, PermissionError
from main.db import db

from .tarea import Tarea
from .estado import Estado
from tablero.tablero import Tablero
from tablero.transicion_realizada import Transicion_realizada

import time

from main.schemas import TareaSchema

tarea_router = Blueprint('tarea', __name__)

tarea_schema = TareaSchema()

api = Api(tarea_router)

def get_tarea_actual(tablero_id : int, tarea_id : int):
    tarea_actual = Tarea.get_by_id(tarea_id)
    if tarea_actual == None:
        raise ResourceNotFoundError(
            "error: La tarea " + str(tarea_id) + " no existe")
    if tarea_actual.tablero_id != tablero_id:
        raise PermissionError(
            "error: La tarea " + str(tarea_id) + " no pertenece al tablero " + str(tablero_id))
    return tarea_actual

class TareaListResource(Resource):
    def get(self, tablero_id : int):
        tablero = Tablero.get_by_id(tablero_id)
        result = tarea_schema.dump(tablero.tareas, many=True)
        return result, 200

    @requires_auth
    def post(self, tablero_id: int):
        data = request.get_json()
        tarea_nueva_dicc = tarea_schema.load(data)
        estado_tarea_nueva = Estado.get_by_id(tarea_nueva_dicc['estado_id'])
        tarea_nueva = Tarea(tarea_nueva_dicc['titulo'], tarea_nueva_dicc['descripcion'], estado=estado_tarea_nueva)
        tarea_nueva.tablero_id = tarea_nueva_dicc['tablero_id']
        tarea_nueva.save()
        result = tarea_schema.dump(tarea_nueva)
        return result, 201

class TareaResource(Resource):
    def get(self, tablero_id : int, tarea_id: int):
        tarea_actual = get_tarea_actual(tablero_id, tarea_id)
        result = tarea_schema.dump(tarea_actual)
        print('get')
        return result, 200

    def delete(self, tablero_id : int, tarea_id : int):
        tarea_actual = get_tarea_actual(tablero_id, tarea_id)

        #Se eliminan todas las transiciones realizadas de la tarea eliminada
        transiciones_tarea_a_borrar = Transicion_realizada.simple_filter(tarea_id=tarea_id)

        for transicion in transiciones_tarea_a_borrar:
            transicion.delete()

        result = tarea_schema.dump(tarea_actual)
        tarea_actual.delete()
        return result, 200

    def post(self, tablero_id : int, tarea_id : int):

        inicio = int(round(time.time() * 1000))

        data = request.get_json()
        tarea = get_tarea_actual(tablero_id, tarea_id)

        for key, value in data.items():
            setattr(tarea, key, value)

        tarea.save()
        fin = int(round(time.time() * 1000))
        print(str(fin - inicio) + 'ms')
        return data, 200

api.add_resource(TareaResource, '/tableros/<int:tablero_id>/tareas/<int:tarea_id>/',
                 endpoint='tareas_resource')
api.add_resource(TareaListResource, '/tableros/<int:tablero_id>/tareas',
                 endpoint='tareas_list_resource')
