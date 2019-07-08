#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
from flask_api import FlaskAPI, status
import json
import logging
from logging.handlers import RotatingFileHandler
from decoder import Decoder
import requests

app = FlaskAPI(__name__)
_host = '0.0.0.0'
_port = 5000
_appDebug = False
_DBNAME = 'db.json'
l = 42

@app.route('/decode', methods=['POST'])
def decode():
    l.debug("/decode :: data received :: {}".format(request.data))
    
    if set(("id","time", "data")) <= request.data.keys():
        trame = Decoder(request.data["data"])
        datas = trame.getDatas()
        toAdd = {"device_id" : request.data["id"], "timestamp" : request.data["time"]}
        datas.update(toAdd)
        
        # requests.post(url, json=json.dumps(datas))
        l.info("datas :: {}".format(datas))
        return '', status.HTTP_200_OK
    else:
        return '', status.HTTP_409_CONFLICT
    return '', status.HTTP_417_EXPECTATION_FAILED

def initLog(level=logging.DEBUG):
    # création de l'objet logger qui va nous servir à écrire dans les logs
    global l

    l = logging.getLogger()
    l.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    l.addHandler(stream_handler)

    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    l.addHandler(file_handler)

if __name__ == '__main__':
    initLog()
    app.run(host=_host, port=_port, debug=_appDebug)
