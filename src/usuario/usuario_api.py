from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.db import db
from .usuario import Usuario
from main.schemas import UsuarioSchema

usuario_router = Blueprint('usuario', __name__)

usuario_schema = UsuarioSchema()

api = Api(usuario_router)

class UsuarioResource(Resource):
    @requires_auth
    def get(self, user_id):
        usuario_actual = Usuario.get_by_id(user_id)
        result = usuario_schema.dump(usuario_actual)
        return result

api.add_resource(UsuarioResource, '/users/<int:user_id>', endpoint='usuarios_resource')
