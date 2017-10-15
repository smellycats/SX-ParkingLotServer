# -*- coding: utf-8 -*-
import json
import shutil
import uuid
import time
import copy

import arrow
import requests
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, app, auth, cache, limiter, logger, access_logger
from . import helper_kafka
from . import helper_parking
from .models import Users


@auth.verify_password
def verify_pw(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        g.uid = user.id
        return password == user.password
    return False

@app.route('/')
@limiter.limit("5000/hour")
def index_get():
    result = {
        'carinfo_url': '%sparking/carinfo' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header


@app.route('/carinfo', methods=['POST'])
@limiter.exempt
@auth.login_required
def carinfo_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415

    if request.json.get('parkingNo', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'parkingNo',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not helper_parking.parkingno_check(request.json['parkingNo']):
        error = {
            'resource': 'carinfo',
            'field': 'parkingNo',
            'code': 'invalid_data'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422 
    if request.json.get('license', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'license',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if request.json.get('plateColor', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'plateColor',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not helper_parking.platecolor_check(request.json['plateColor']):
        error = {
            'resource': 'carinfo',
            'field': 'plateColor',
            'code': 'invalid_data'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422 
    if request.json.get('snapTime', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'snapTime',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not helper_parking.is_valid_date(request.json['snapTime']):
        error = {
            'resource': 'carinfo',
            'field': 'snapTime',
            'code': 'invalid_data'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422 
    if request.json.get('direction', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'direction',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not helper_parking.direction_check(request.json['direction']):
        error = {
            'resource': 'carinfo',
            'field': 'direction',
            'code': 'invalid_data'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422 
    if request.json.get('gateNo', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'gateNo',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not type(request.json['gateNo']) == int:
        error = {
            'resource': 'carinfo',
            'field': 'gateNo',
            'code': 'invalid_data'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if request.json.get('gateName', None) is None:
        error = {
            'resource': 'carinfo',
            'field': 'gateName',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    try:
        ka = app.config['KA']
        uid = str(uuid.uuid4())   # uuid编号
        lost_msg = {}             # 未上传数据字典
        def acked(err, msg):
            if err is not None:
                lost_msg[msg.key().decode('utf-8')] = msg.value().decode('utf-8')
                logger.error(msg.key().decode('utf-8'))
                logger.error(err)
        value = {'timestamp': arrow.now('PRC').format('YYYY-MM-DD HH:mm:ss'), 'message': request.json}
        ka.produce_info(key=uid, value=json.dumps(value), cb=acked)
        ka.flush()
        
        if uid not in lost_msg:
            return jsonify({'ret': 1, 'msg': 'ok'}), 201

        for i in range(3):
            del(lost_msg[uid])     # 先删除数据记录
            value = {'timestamp': arrow.now('PRC').format('YYYY-MM-DD HH:mm:ss'), 'message': request.json}
            ka.produce_info(key=uid, value=json.dumps(value))
            ka.flush()
            if uid in lost_msg:
                time.sleep(0.1)
            else:
                break
    except Exception as e:
        logger.error(e)
        return jsonify({'ret': 0, 'msg': 'error'}), 201
    if uid in lost_msg:
        return jsonify({'ret': 0, 'msg': 'error'}), 201
    else:
        return jsonify({'ret': 1, 'msg': 'ok'}), 201

