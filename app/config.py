# -*- coding: utf-8 -*-
from . import helper_kafka

class Config(object):
    # 密码 string
    SECRET_KEY = 'showmethemoney'
    # 服务器名称
    HEADER_SERVER = 'SX-ParkingLotServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认2小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../kakou.db'
    # 数据库连接绑定 dict
    SQLALCHEMY_BINDS = {}
    # 连接池大小 int
    # SQLALCHEMY_POOL_SIZE = 5
    # 用户权限范围 dict
    SCOPE_USER = {}
    # 白名单启用 bool
    WHITE_LIST_OPEN = True
    # 白名单列表 set
    WHITE_LIST = set()
    # kafka实例
    KA = helper_kafka.KafkaData(**{'services': '10.123.123.123:9092', 'topic': 'kakou'})


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


class Testing(Config):
    TESTING = True
