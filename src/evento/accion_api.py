from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.db import db

from main.excepciones import ResourceNotFoundError, PermissionError, TransicionNoValidaError

from .accion import Accion_mock, Accion, AccionFactory

from main.schemas import AccionMockSchema, AccionSchema

acciones_router = Blueprint('acciones', __name__)

accion_schema = AccionSchema()

api = Api(acciones_router)

class AccionesResource(Resource):
    def get(self):
        return jsonify(AccionFactory.get_acciones_posibles())

api.add_resource(AccionesResource, '/acciones', endpoint='acciones_resource')
