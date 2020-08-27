from flask import Flask, request, jsonify

from .autentificacion import AuthError, requires_auth
from flask_cors import cross_origin

import os
from main import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
