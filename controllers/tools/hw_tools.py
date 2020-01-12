#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from configs.fileserver_config import *
from redis import Redis
import os, json

redis = Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

path = os.path.join(FILESERVER, 'guides', 'delta', 'test_delta.js')


@main.route('/delta-info/edit/<id>/', methods=['GET', 'POST'])
def delta_info_editor(id):
    username = "zcc"
    redis_key = username + id
    if request.method == "GET":
        with open(path, 'r') as f:
            data = json.load(f)
        redis.set(redis_key, json.dumps(data))
        return render_template('webtools/delta_info_editor.html', data=data)
    else:
        data = json.loads(redis.get(redis_key))
        if data:
            # print("Before:\n" + json.dumps(data))
            out_counter = 0
            for file in data['delta_info']:
                out_counter += 1
                if file['type'] != "modified":
                    file['reason'] = request.form.get('reason'+str(out_counter))
                else:
                    in_counter = 0
                    for func in file['funcs']:
                        in_counter += 1
                        func['reason'] = request.form.get('reason' + str(out_counter) + str(in_counter))
            print(" After:\n" + json.dumps(data, indent=4))
            redis.delete(redis_key)
            return "success"
        else:
            return 'Error! No Delta Info Exist!'
