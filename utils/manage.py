#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import sys
sys.path.append("..")
from web import app
from models.user_model import db

from models.user_model import User
from models.book_model import Book, Author, Year
from models.poetry_model import Poeter, Poetry, PoetryCategory

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
