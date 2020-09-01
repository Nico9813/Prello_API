from flask import Flask, jsonify
from flask_restful import Api
from .db import db
from usuario.usuario_api import usuario_router
from tablero.tablero_api import tablero_router
from tarea.tarea_api import tarea_router
from .ext import ma, migrate
from .excepciones import ResourceNotFoundError, PermissionError, AuthError

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Inicializa las extensiones
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
