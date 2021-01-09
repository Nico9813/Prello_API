from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.db import db
from pommons.list import find

from main.excepciones import ResourceNotFoundError, PermissionError, TransicionNoValidaError

from .accion import Accion_mock, Accion, AccionFactory
from .subscripcion import Subscripcion
from tablero.tablero import Tablero
from tarea.tarea import Tarea
from tarea.estado import Estado

from main.schemas import SubscripcionSchema

subscripciones_router = Blueprint('subscripciones', __name__)

subscripcion_schema = SubscripcionSchema()

api = Api(subscripciones_router)

class SubscripcionResource(Resource):
    def post(self):
        data = request.get_json()
        subscripcion_dicc = subscripcion_schema.load(data)

        observable = {
            "TABLERO": lambda id : Tablero.get_by_id(id),
            "TAREA": lambda id : Tarea.get_by_id(id),
            "ESTADO": lambda id : Estado.get_by_id(id),
        }[subscripcion_dicc['tipo_objeto']](subscripcion_dicc['id_objeto'])

        accion_dicc = subscripcion_dicc['accion']

        accion = AccionFactory.crear_instancia(accion_dicc['tipo_accion'], accion_dicc['payload'])

        evento = find(observable.obtener_eventos_posibles(), lambda evento_actual: evento_actual.value == subscripcion_dicc['evento'])

        if evento is None:
            raise ResourceNotFoundError("No existe el evento " + subscripcion_dicc['evento'])

        subscripcion_nueva = Subscripcion(evento, accion)

        observable.agregar_subscripcion(subscripcion_nueva)

        subscripcion_nueva.save()

        result = subscripcion_schema.dump(subscripcion_nueva)

        return result

api.add_resource(SubscripcionResource, '/subscripciones', endpoint='subscripciones_resource')
