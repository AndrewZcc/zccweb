#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    authority = db.Column(db.String(20), nullable=False, default="General")
