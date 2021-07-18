#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from configs.fileserver_config import *
import os, ast

game_dict = dict()


def read_game_info():
    game_info_path = os.path.join(FILESERVER, 'games', 'game_infos.js')
    with open(game_info_path, 'r', encoding='utf-8') as f:
        game_infos = f.read()
    global game_dict
    game_dict = ast.literal_eval(game_infos)


@main.route('/games/')
def playground():
    if len(game_dict) == 0:
        read_game_info()
    return render_template('games/game_home.html', games=game_dict)


@main.route('/game/<name>/')
def game(name):
    if len(game_dict) == 0:
        read_game_info()
    real_title = game_dict[name]['title']
    real_name = game_dict[name]['name']
    return render_template('games/game.html', title=real_title, name=real_name)


@main.route("/datalake/statistic")
def datalake_statistic():
    data = {
        "组织域": ['url1', 'url2'],
        "归档域": ['url1', 'url2'],
        "开发域": 'NA',
        "构建域": 'NA',
        "需求域": 'NA',
        "测试域": 'NA',
        "设计域": 'NA'
    }

    links = {
        "天眼": "god-eye.data.com",
        "云杉搜索": "yunshan.rnd.huawei.com"
    }

    return render_template('datalake/statistic.html', data=data, links=links)
