#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from controllers.book_control import *
from controllers.poetry_control import *
from controllers.notes_control import *

DEFAULT_BLUEPRINT = [
    [main, '']
]


def config_blueprint(app):
    for each in DEFAULT_BLUEPRINT:
        app.register_blueprint(each[0], url_prefix=each[1])
