#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *

# 搜索关键字：div css google首页
# 参考链接：https://blog.csdn.net/courseware/article/details/1912661
@main.route('/google')
def google_index():
    return render_template('webpage2_0/homepage.html')

