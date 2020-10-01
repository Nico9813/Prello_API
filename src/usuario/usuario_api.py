from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.db import db
from .usuario import Usuario
from main.schemas import UsuarioSchema

usuario_router = Blueprint('usuario', __name__)

usuario_schema = UsuarioSchema()

api = Api(usuario_router)

class UsuarioPrueba(Resource):
    def get(self):
        return jsonify({'msg': 'Welcome to PRELLO API'}), 200

class UsuarioResource(Resource):
    @requires_auth
    def get(self):
        usuario_actual = get_usuario_actual()
        result = usuario_schema.dump(usuario_actual)
        return result, 200

api.add_resource(UsuarioResource, '/perfil', endpoint='usuarios_resource')
api.add_resource(UsuarioPrueba, '/', endpoint='usuario_prueba')
