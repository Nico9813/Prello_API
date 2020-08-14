from .tablero import Tablero
from usuario.usuario import Usuario
from evento.evento import Evento_tablero
from evento.accion import Accion_mock

def test_crear_tablero():
    tabler = Tablero("asda")
    assert tabler.nombre == "asda"

def test_obtener_eventos():
	tablero = Tablero("Tablero")
	eventosPosibles = tablero.obtener_eventos_posibles()
	assert Evento_tablero.CREACION_TARJETA in eventosPosibles
	assert Evento_tablero.BORRACION_TARJETA in eventosPosibles
	assert Evento_tablero.MOVICION_TARJETA in eventosPosibles
	assert Evento_tablero.AGREGACION_USUARIO in eventosPosibles

def test_suscripcion_tablero():
	user = Usuario("asd")
	tablero = Tablero("Tablero")
	accion_realizada = Accion_mock()
	accion_no_realizada = Accion_mock()
	user.subscribirse(Evento_tablero.CREACION_TARJETA, tablero, accion_realizada)
	user.subscribirse(Evento_tablero.AGREGACION_USUARIO, tablero, accion_no_realizada)
	tablero.procesar_evento(Evento_tablero.CREACION_TARJETA)
	tablero.procesar_evento(Evento_tablero.CREACION_TARJETA)
	assert accion_realizada.contador == 2
	assert accion_no_realizada.contador == 0