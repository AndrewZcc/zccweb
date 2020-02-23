#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *

import tushare as ts
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

import json
import datetime


def gen_market_plot(start, end):
    # ts.set_token('26e793731ba78ab867c22f97282597e1b0bfa2515fe4f9b06ec77703')
    # 初始化 tushare pro，设置 TOKEN
    pro = ts.pro_api('26e793731ba78ab867c22f97282597e1b0bfa2515fe4f9b06ec77703')

    # 调用接口查询上证指数数据
    # df_daily = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001',
    #                      fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    # df_daily = pro.daily(ts_code="000001", start_date="20200215", end_date="20200222")
    # print(df_daily)

    # 获取数据
    df_daily = ts.get_k_data(code='sh', ktype='D', autype='qfq', start=start, end=end)
    # print(df_daily)

    # 数据呈现
    df_daily.index = pd.to_datetime(df_daily.date)
    # 采用 plotly 同时画多条数据线
    data = [
        go.Candlestick(x=df_daily['date'],
                       open=df_daily['open'], close=df_daily['close'],
                       high=df_daily['high'], low=df_daily['low']),
        go.Scatter(x=df_daily['date'], y=df_daily['close'], mode='lines')
    ]
    graph_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_data


@main.route('/quant/', methods=['GET', 'POST'])
def tushare_quant():
    if request.method == 'GET':
        start = '2017-01-01'
        end = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        start = request.form.get('start')
        end = request.form.get('end')
    graph_data = gen_market_plot(start, end)
    return render_template('quant/quant.html', data=graph_data, start=start, end=end)
