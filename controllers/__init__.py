#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from controllers.book_control import *
from controllers.poetry_control import *
from controllers.notes_control import *
from controllers.blog_control import *
from controllers.web_tools import *
from controllers.file_server import *
from controllers.games import *
from controllers.tools import *
from controllers.webpage2_0 import *


DEFAULT_BLUEPRINT = [
    [main, '']
]


def config_blueprint(app):
    for each in DEFAULT_BLUEPRINT:
        app.register_blueprint(each[0], url_prefix=each[1])
