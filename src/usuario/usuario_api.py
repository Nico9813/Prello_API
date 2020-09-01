from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_id_usuario_actual
from main.db import db
from .usuario import Usuario
from main.schemas import UsuarioSchema

usuario_router = Blueprint('usuario', __name__)

usuario_schema = UsuarioSchema()

api = Api(usuario_router)

class UsuarioPrueba(Resource):
    def get(self):
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
        from workflow.transicion_posible import Transicion_posible

        User: Usuario = Usuario('Rodrigo')
        QA: Rol = Rol('QA')

        TODO: Estado = Estado('TODO')
        DOING: Estado = Estado('DOING')

        Accion_tablero: Accion_mock = Accion_mock()
        Accion_tarea: Accion_mock = Accion_mock()
        Accion_estado: Accion_mock = Accion_mock()

        Primer_tarea: Tarea = Tarea('Tituloo', 'Descripcion larga', estado=TODO)

        Proyecto: Tablero = Tablero('Proyecto')
        SegundoProyecto: Tablero = Tablero('Segundo Proyecto')
        Proyecto.agregar_tarea(Primer_tarea)

        User.agregar_tablero(Proyecto)
        User.agregar_tablero(SegundoProyecto)
        User.subscribirse(Evento.CREACION_TARJETA, Proyecto, Accion_tablero)
        User.subscribirse(Evento.CAMBIO_DE_ESTADO, Primer_tarea, Accion_tarea)
        User.subscribirse(Evento.INGRESO_TARJETA, TODO, Accion_estado)

        accion_transicion: Accion_mock = Accion_mock()

        workflow: Workflow = Workflow()
        Proyecto.workflow = workflow

        workflow.agregar_accion_entre_estados(TODO, DOING, accion_transicion)
        Proyecto.ejecutar_transicion(Primer_tarea, DOING)

        User.save()

        return jsonify({'message': "Usuario de prueba cargado correctamente"})

class UsuarioResource(Resource):
    def get(self):
        usuario_actual = Usuario.get_by_id(get_id_usuario_actual())
        result = usuario_schema.dump(usuario_actual)
        return result

api.add_resource(UsuarioResource, '/perfil', endpoint='usuarios_resource')
api.add_resource(UsuarioPrueba, '/', endpoint='usuario_prueba')
