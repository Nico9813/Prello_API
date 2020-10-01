from six.moves.urllib.request import urlopen
from functools import wraps
from flask import request, _request_ctx_stack, jsonify
from usuario.usuario import Usuario
from jose import jwt
import json
from .config import AUTH0_DOMAIN, API_AUDIENCE, ALGORITHMS
from .excepciones import AuthError

# Para obtener el token de acceso POST https://dev-jx8fysvq.us.auth0.com/oauth/token HEADERS { "content-type": "application/json"}
# Para acceder a una ruta privada HEADERS { "content-type": "application/json", "Authorization": "Bearer TOKEN_ACCESO"}

def get_usuario_actual():
    id_actual = _request_ctx_stack.top.current_user['sub']
    usuario_actual = Usuario.get_by_id(id_actual)
    if not usuario_actual:
        from usuario.rol import Rol
        from tarea.estado import Estado
        from tarea.tarea import Tarea
        from tablero.tablero import Tablero
        from tablero.transicion_realizada import Transicion_realizada
        from evento.observable import Observable
        from evento.evento import Evento
        from evento.accion import Accion_mock
        from evento.subscripcion import Subscripcion
        from workflow.workflow import Workflow
        from workflow.transicion_posible import TransicionPosible

        usuario_actual = Usuario(id_actual)
        usuario_actual.nombre = 'Rodrigo'
        QA: Rol = Rol('QA')

        TODO: Estado = Estado('TODO')
        DOING: Estado = Estado('DOING')

        Accion_tablero: Accion_mock = Accion_mock()
        Accion_tarea: Accion_mock = Accion_mock()
        Accion_estado: Accion_mock = Accion_mock()

        Primer_tarea: Tarea = Tarea('Tituloo', 'Descripcion larga', estado=TODO)

        Proyecto: Tablero = Tablero('Proyecto')

        Proyecto.agregar_estado(TODO)
        Proyecto.agregar_estado(DOING)

        SegundoProyecto: Tablero = Tablero('Segundo Proyecto')
        Proyecto.agregar_tarea(Primer_tarea)

        usuario_actual.agregar_tablero(Proyecto)
        usuario_actual.agregar_tablero(SegundoProyecto)
        usuario_actual.subscribirse(Evento.CREACION_TARJETA, Proyecto, Accion_tablero)
        usuario_actual.subscribirse(Evento.CAMBIO_DE_ESTADO, Primer_tarea, Accion_tarea)
        usuario_actual.subscribirse(Evento.INGRESO_TARJETA, TODO, Accion_estado)

        accion_transicion: Accion_mock = Accion_mock()

        workflow: Workflow = Workflow()
        Proyecto.workflow = workflow

        workflow.agregar_accion_entre_estados(TODO, DOING, accion_transicion)
        Proyecto.ejecutar_transicion(Primer_tarea, DOING)

        usuario_actual.save()
    return usuario_actual

def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)
    return decorated
