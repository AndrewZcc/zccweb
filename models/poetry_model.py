#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models import db
from datetime import datetime


class Poeter(db.Model):
    __tablename__ = 'poeter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(10))


poetry_tag = db.Table('poetry_tag',
    db.Column('poetry_id', db.Integer, db.ForeignKey('poetry.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('poetry_category.id'), primary_key=True)
)


class PoetryCategory(db.Model):
    __tablename__ = 'poetry_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)


class Poetry(db.Model):
    __tablename__ = 'poetry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    content_path = db.Column(db.Text)
    poet_id = db.Column(db.Integer, db.ForeignKey('poeter.id'))

    poet = db.relationship('Poeter', backref=db.backref('poetries'))
    categories = db.relationship('PoetryCategory', secondary=poetry_tag, backref=db.backref('poetries'))
