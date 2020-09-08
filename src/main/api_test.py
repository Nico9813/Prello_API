import os
import tempfile

import pytest
from flask import json
from main import create_app
from main.db import db
from usuario.usuario import Usuario

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
	data = {
		'nombre':'tablero_prueba'
	}
	result = client.post('/tableros', json=data)
	assert result.status_code == 201
	result = client.get('/tableros/' + str(result.get_json()['id']))
	assert result.status_code == 200

def test_get_tareas(client):
	result = client.get('/tableros/1/tareas/')
	assert result.status_code == 200

def test_post_get_tarea(client):
	data = {
		'titulo': 'tarea_prueba',
		'descripcion': 'descripcion',
		'tablero_id': 1,
		'estado_id': 1
	}
	result = client.post('/tableros/1/tareas/', json=data)
	assert result.status_code == 201
	result = client.get('/tableros/1/tareas/' + str(result.get_json()['id']))
	assert result.status_code == 200


