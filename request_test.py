# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

IP = '127.0.0.1'
PORT = 5004

def parking_post():
    """POST请求"""
    url = 'http://{0}:{1}/parking/carinfo'.format(IP, PORT)
    headers = {'content-type': 'application/json'}
    data = {
        'parkingNo': '441302401',
        'license': '粤L12345',
        'plateColor': 0,
        'snapTime': '2017-08-12 14:00:00',
        'direction': 1,
        'gateNo': 1,
        'gateName': '丽日停车场入口1',
        'carOwner': '车主姓名',
        'homeAddress': '住址',
        'phone': '13610010001',
        'weChat': '微信号',
        'picurl': 'http://10.0.0.1/pic/20170812140000.jpg'
    }
    username = 'test'
    password = 'test123'
    r = requests.post(url, headers=headers, data=json.dumps(data),
                      auth=HTTPBasicAuth(username, password))
    print r.status_code
    print r.text
    return r


if __name__ == '__main__':  # pragma nocover
    parking_post()
