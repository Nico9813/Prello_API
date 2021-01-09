from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.db import db
from .usuario import Usuario
from main.schemas import UsuarioSchema, TransicionPosibleSchema, WorkflowSchema
from workflow.workflow import Workflow
from workflow.transicion_posible import TransicionPosible
from tarea.estado import Estado
import time

usuario_router = Blueprint('usuario', __name__)

usuario_schema = UsuarioSchema()
tp_schema = WorkflowSchema()

api = Api(usuario_router)

class UsuarioPrueba(Resource):
    def get(self):
        return jsonify({'msg': "Welcome to PRELLO API"})

class UsuarioResource(Resource):
    @requires_auth
    def get(self):
        usuario_actual = get_usuario_actual()
        for tablero in usuario_actual.tableros:
            for tarea in tablero.tareas:
                tarea.get_estados_posibles(tablero.workflow)
        result = usuario_schema.dump(usuario_actual)
        return result, 200

api.add_resource(UsuarioResource, '/perfil', endpoint='usuarios_resource')
api.add_resource(UsuarioPrueba, '/', endpoint='usuario_prueba')
