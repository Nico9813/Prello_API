from flask import Blueprint

tablero_router = Blueprint('tablero', __name__)

@tablero_router.route('/', methods=['Get'])
def getAllBoards():
    return 'all boards'

@tablero_router.route('/<id>', methods=['Get'])
def getBoard(id):
    return 'board' + id