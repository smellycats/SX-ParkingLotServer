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


class Parking(db.Model):
    """停车场"""
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    content = db.Column(db.Text)
    banned = db.Column(db.Integer, default=0)
    
    def __init__(self, date_created=None, content='', banned=0, time=''):
        if date_created is None:
            self.date_created = arrow.now('PRC').datetime.replace(tzinfo=None)
        else:
            self.date_created = date_created
        self.content = content
        self.banned = banned

    def __repr__(self):
        return '<Parking %r>' % self.id
