#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def sec_readfile(path):
    with open(path, 'r') as f:
        return f.read()


def sec_writefile(path, content):
    with open(path, 'w') as f:
        f.write(content)
