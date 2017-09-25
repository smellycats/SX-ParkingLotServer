# -*- coding: utf-8 -*-
import json
from functools import wraps
import shutil
import random

import arrow
import requests
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import func

from . import db, app, auth, cache, limiter, logger, access_logger
from models import *
import helper_parking


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


@app.route('/maxid', methods=['get'])
@limiter.limit('5000/minute')
#@limiter.exempt
@auth.login_required
def maxid_get():
    try:
        q = db.session.query(func.max(Parking.id)).first()
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.exception(e)


@app.route('/carinfo', methods=['get'])
@limiter.limit('5000/minute')
#@limiter.exempt
@auth.login_required
def carinfo_list_get():
    q = request.args.get('q', None)
    if q is None:
	abort(400)
    try:
	args = json.loads(q)
    except Exception as e:
	logger.error(e)
	abort(400)
    try:
        s = db.session.query(Parking)
	if args.get('startid', None) is not None:
	    s = s.filter(Parking.id >= args['startid'])
	if args.get('endid', None) is not None:
            s = s.filter(Parking.id <= args['endid'])

        if len(s.all())==0:
            return jsonify({'items': [], 'total_count': 0})
	items = []
        for i in s.all():
            print i.date_created
	    item = {
                'id': i.id,
                'date_created': i.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'content': i.content
            }
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
        print(e)
	logger.exception(e)


@app.route('/carinfo', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
@auth.login_required
def carinfo_post():
    try:
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

        p = Parking(content=json.dumps(request.json))
        db.session.add(p)
        db.session.commit()
    except Exception as e:
	logger.exception(e)
	return jsonify({'ret': 0, 'msg': 'error'}), 201
    return jsonify({'ret': 1, 'msg': 'ok'}), 201


