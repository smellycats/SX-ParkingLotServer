# -*- coding: utf-8 -*-
import arrow

from . import db


class Users(db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(64))
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, banned=0):
        self.username = username
        self.password = password
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id
