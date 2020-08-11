from flask import Blueprint

usuario_router = Blueprint('usuario', __name__)

@usuario_router.route('/', methods=['Get'])
def getAllUsers():
    return 'all users'

@usuario_router.route('/<id>', methods=['Get'])
def getUser(id):
    return 'user' + id