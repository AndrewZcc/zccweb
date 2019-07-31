#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models.blog_model import *
import random, string


def generate_random_str(randomlength=16):
    """
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def gen_blog_url_id(length=12):
    url_id = generate_random_str(length)
    while 1:
        blog = Blog.query.filter(Blog.url_id == url_id).first()
        if not blog:
            break
        url_id = generate_random_str(length)

    return url_id
