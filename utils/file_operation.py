#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def sec_readfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def sec_writefile(path, content):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write(content)
