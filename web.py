#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from flask import Flask
from controllers import *
from models import db
from configs import db_config

app = Flask(__name__)
config_blueprint(app)
app.config.from_object(db_config)
db.init_app(app)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port='8001')
    app.run(host='0.0.0.0', port='8001')
