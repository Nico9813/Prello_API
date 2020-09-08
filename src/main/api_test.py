import os
import tempfile

import pytest
from flask import json
from main import create_app
from main.db import db
from usuario.usuario import Usuario

def obtener_tablero_prueba(client):
	data = {
		'nombre': 'tablero_prueba'
	}
	result = client.post('/tableros', json=data)
	if result.status_code != 201:
		raise Exception()
	return str(result.get_json()['id'])


def obtener_tarea_prueba(client, tablero_id, estado_id):
	data = {
		'titulo': 'tarea_prueba',
		'descripcion': 'descripcion',
		'tablero_id': tablero_id,
		'estado_id': estado_id
	}
	result = client.post('/tableros/' + tablero_id + '/tareas/', json=data)
	if result.status_code != 201:
		raise Exception()
	return str(result.get_json()['id'])

def obtener_estado_prueba(client, tablero_id):
	data = {
		'nombre': 'TESTING'
	}
	result = client.post('/tableros/' + tablero_id + '/estados/', json=data)
	if result.status_code != 201:
		raise Exception()
	return str(result.get_json()['id'])

def obtener_transicion_prueba(client, tablero_id, estado_id, estado_id_destino):
	data = {
		'id_estado_inicial':estado_id,
		'id_estado_final':estado_id_destino
	}
	result = client.post('/tableros/' + tablero_id +
	                     '/transiciones_posibles', json=data)
	if result.status_code != 201:
		raise Exception()
	return str(result.get_json()['id'])

@pytest.fixture
def client():
	flaskr = create_app("main.config")
	with flaskr.test_client() as client:
		with flaskr.app_context():
			db.create_all()
		yield client

def test_carga_usuario_prueba(client):
	result = client.get('/')
	assert result.status_code == 200

def test_perfil(client):
	result = client.get('/perfil')
	assert result.status_code == 200

def test_get_tableros(client):
	result = client.get('/tableros')
	assert result.status_code == 200

def test_post_get_tablero(client):
	result = client.get('/tableros/' + obtener_tablero_prueba(client))
	assert result.status_code == 200

def test_get_tareas(client):
	result = client.get('/tableros/' + obtener_tablero_prueba(client) + '/tareas/')
	assert result.status_code == 200

def test_post_get_tarea(client):
	tablero_id = obtener_tablero_prueba(client)
	estado_id = obtener_estado_prueba(client, tablero_id)
	tarea_id = obtener_tarea_prueba(client, tablero_id, estado_id)
	result = client.get('/tableros/' + tablero_id +
	                    '/tareas/' + tarea_id)
	assert result.status_code == 200

def test_get_estados(client):
	tablero_id = obtener_tablero_prueba(client)
	result = client.get(
		'/tableros/' + tablero_id + '/estados')
	assert result.status_code == 200

def test_post_get_estados(client):
	tablero_id = obtener_tablero_prueba(client)
	estado_id = obtener_estado_prueba(client, tablero_id)
	result = client.get(
		'/tableros/' + tablero_id + '/estados/' + estado_id
	)
	assert result.status_code == 200

def test_estados_posibles(client):
	tablero_id = obtener_tablero_prueba(client)
	estado_id = obtener_estado_prueba(client, tablero_id)
	result = client.get(
        '/tableros/' + tablero_id + '/estados/' + estado_id + '/posibles'
    )
	assert result.status_code == 200

def test_post_transicion_posible(client):
	tablero_id = obtener_tablero_prueba(client)
	estado_id = obtener_estado_prueba(client, tablero_id)
	estado_id_destino = obtener_estado_prueba(client, tablero_id)
	transicion_posible_id = obtener_transicion_prueba(client, tablero_id, estado_id, estado_id_destino)
	assert transicion_posible_id != None

def test_post_get_transicion_tarea(client):
	tablero_id = obtener_tablero_prueba(client)
	estado_id = obtener_estado_prueba(client, tablero_id)
	tarea_id = obtener_tarea_prueba(client, tablero_id, estado_id)
	estado_id_destino = obtener_estado_prueba(client, tablero_id)
	obtener_transicion_prueba(client, tablero_id, estado_id, estado_id_destino)
	data = {
		'id_tarea': int(tarea_id),
		'id_estado_final':int(estado_id_destino)
	}
	result = client.post(
		'/tableros/' + tablero_id + '/transiciones', json=data
	)
	assert result.status_code == 201
