# -*- coding: utf-8 -*-
u"""helper functions.

    SX-SMSServer.helper
    ~~~~~~~~~~~~~~
    
    辅助函数
    
    :copyright: (c) 2015 by Fire.
    :license: BSD, see LICENSE for more details.
"""
import time

def parkingno_check(parking_no):
    try:
        p = int(parking_no)
        if p > 441302400 and p < 441302600:
            return True
        return False
    except Exception as e:
        return False

def platecolor_check(plate_color):
    if plate_color in set([0, 1, 2, 3, 4, 9]):
        return True
    return False

def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d %H:%M:%S")
    return True
  except:
    return False

def direction_check(direction):
    if direction in set([0, 1]):
        return True
    return False
