#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models import db
from datetime import datetime


class NoteCategory(db.Model):
    __tablename__='note_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    order = db.Column(db.Integer, default=1)


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    content_path = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('notes'))
    cat_id = db.Column(db.Integer, db.ForeignKey('note_category.id'))
    category = db.relationship('NoteCategory', backref=db.backref('notes'))
