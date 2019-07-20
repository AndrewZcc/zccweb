#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models import db
from datetime import datetime
import time


class Author(db.Model):
    __tablename__ = 'book_author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(10), nullable=False)


class Year(db.Model):
    __tablename__ = 'book_year'
    year = db.Column(db.Integer, primary_key=True, default=datetime.now().year)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    title_desc = db.Column(db.String(100), nullable=False, default=title)
    imagePath = db.Column(db.Text)
    mdNotePath = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False, default=3)
    finish_date = db.Column(db.Text, default=str(time.strftime("%Y-%m-%d")))
    one_sentence = db.Column(db.Text)
    eBookPath = db.Column(db.Text)
    likes = db.Column(db.Integer, nullable=False, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey('book_author.id'))
    year_id = db.Column(db.Integer, db.ForeignKey('book_year.year'))

    author = db.relationship('Author', backref=db.backref('books'))
    year = db.relationship('Year', backref=db.backref('books'))
