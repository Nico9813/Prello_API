from flask import Blueprint, jsonify
from main.autentificacion import requires_auth, get_id_usuario_actual
from main.run import db
from .usuario import Usuario

usuario_router = Blueprint('usuario', __name__)

@usuario_router.route('/', methods=['Get'])
@requires_auth
def getAllUsers():
    return jsonify({'message': Usuario.query.get(get_id_usuario_actual()).__str__()})

@usuario_router.route('/<id>', methods=['Get'])
def getUser(id):
    return 'user' + id
