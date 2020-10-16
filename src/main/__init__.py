from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin
from .db import db
from usuario.usuario import Usuario
from usuario.usuario_api import usuario_router
from tablero.tablero_api import tablero_router
from tarea.tarea_api import tarea_router
from tarea.estado_api import estado_router
from evento.accion_api import acciones_router
from evento.subscripcion_api import subscripciones_router
from .ext import ma, migrate
from .excepciones import ResourceNotFoundError, PermissionError, AuthError

def create_app(settings_module):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(settings_module)

    # Inicializa las extensiones
    from usuario.rol import Rol
    from tarea.estado import Estado
    from tarea.tarea import Tarea
    from tablero.tablero import Tablero
    from usuario.usuario import Usuario
    from tablero.transicion_realizada import Transicion_realizada
    from evento.observable import Observable
    from evento.evento import Evento
    from evento.accion import Accion_mock
    from evento.subscripcion import Subscripcion
    from workflow.workflow import Workflow
    from workflow.transicion_posible import TransicionPosible
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Captura todos los errores 404
    Api(app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False

    # Registra los blueprints
    app.register_blueprint(usuario_router)
    app.register_blueprint(tablero_router)
    app.register_blueprint(tarea_router)
    app.register_blueprint(estado_router)
    app.register_blueprint(acciones_router)
    app.register_blueprint(subscripciones_router)

    # Registra manejadores de errores personalizados
    register_error_handlers(app)

    return app

def register_error_handlers(app):

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(PermissionError)
    def handle_permissionError(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404
