from flask import Flask, request, jsonify

from .autentificacion import AuthError, requires_auth
from flask_cors import cross_origin

import os
from main import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

@app.route('/private', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    return jsonify({'message': 'Welcome to my APIIIIII PRIVATE'})

@app.route('/', methods=['GET'])
def index():
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

    User : Usuario = Usuario('Rodrigo')
    QA : Rol = Rol('QA')

    TODO : Estado = Estado('TODO')
    DOING : Estado = Estado('DOING')
    
    Accion_tablero : Accion_mock = Accion_mock()
    Accion_tarea : Accion_mock = Accion_mock()
    Accion_estado : Accion_mock = Accion_mock()

    Primer_tarea : Tarea = Tarea(TODO, 'Tituloo', 'Descripcion larga')

    Proyecto : Tablero = Tablero('Proyecto')
    Proyecto.agregar_tarea(Primer_tarea)

    User.agregar_tablero(Proyecto)
    User.subscribirse(Evento.CREACION_TARJETA, Proyecto, Accion_tablero)
    User.subscribirse(Evento.CAMBIO_DE_ESTADO, Primer_tarea, Accion_tarea)
    User.subscribirse(Evento.INGRESO_TARJETA, TODO, Accion_estado)


    accion_transicion : Accion_mock = Accion_mock()

    workflow: Workflow = Workflow()
    Proyecto.workflow = workflow

    workflow.agregar_accion_entre_estados(TODO, DOING, accion_transicion)
    Proyecto.ejecutar_transicion(Primer_tarea, DOING)

    db.session.add(User)
    db.session.commit()
    return jsonify({'message': __name__})
