# -*- coding: utf-8 -*-
import arrow

from app import db, app
from app.models import *
from app.helper import *


def test_scope_get():
    scope = Scope.query.all()
    for i in scope:
        print i.name

def test_user_get():
    user = Users.query.filter_by(username='admin', banned=0).first()
    print user.scope
    
def test_traffic_get():
    r = Traffic.query.first()
    #help(r)
    print type(r.pass_time)
    #print r.crossing_id

def test_traffic_add():
    t_list = []
    for i in range(3):
        t = Traffic(crossing_id='441302123', lane_no=1, direction_index='IN',
                    plate_no=u'粤L12345', plate_type='',
                    pass_time='2015-12-13 01:23:45', plate_color='0')
        db.session.add(t)
        t_list.append(t)
    db.session.commit()
    r = [{'pass_id': r.pass_id} for r in t_list]
    print r

def test_uci_add():
    t = UserCltxId(user_id=1, city='hcq', cltx_id=123)
    db.session.add(t)
    db.session.commit()

def test_uci_get():
    u = UserCltxId.query.filter_by(user_id=22, city='hcq').first()
    u.cltx_id = 456
    db.session.commit()


def test_temp_add():
    t_list = []
    for i in range(3):
        t = TempDYW(cltx_id=123, hphm=u'粤L12345', jgsj='2015-12-13 01:23:45',
                    hpys=u'蓝牌', hpys_id=1, hpys_code='BU', kkdd=u'交警支队',
                    kkdd_id='441302', fxbh=u'进城', fxbh_code='IN',cdbh=1,
		    clsd=43, hpzl='7', kkbh='020', clbj='F', imgurl=u'http://123.jpg',
		    flag=0, banned=1)
        db.session.add(t)
        t_list.append(t)
    db.session.commit()
    #r = [{'pass_id': r.pass_id} for r in t_list]
    #print r

def test_temp_add2():
    t = TempHCQ2(cltx_id=123, hphm=u'粤L12345', jgsj='2015-12-13 01:23:45',
                 hpys=u'蓝牌', hpys_id=1, hpys_code='BU', kkdd=u'交警支队',
                 kkdd_id='441302', fxbh=u'进城', fxbh_code='IN',cdbh=1,
		 clsd=43, hpzl='7', kkbh='020', clbj='F', imgurl=u'http://123.jpg',
		 flag=0, banned=1)
    db.session.add(t)
    db.session.commit()

def test_temp_add2():
    t = TempZK(cltx_id=123, hphm=u'粤L12345', jgsj='2015-12-13 01:23:45',
               hpys=u'蓝牌', hpys_id=1, hpys_code='BU', kkdd=u'交警支队',
               kkdd_id='441302', fxbh=u'进城', fxbh_code='IN',cdbh=1,
	       clsd=43, hpzl='7', kkbh='020', clbj='F', imgurl=u'http://123.jpg',
	       flag=0, banned=1)
    db.session.add(t)
    db.session.commit()

def test_temp_find():
    c = db.session.query(TempHCQ2).filter(TempHCQ2.id==55382841).first()
    #c = FinalLM.query.filter_by(id=1).first()
    print c.jgsj
    print c.hphm

def test_final_find():
    sql = ("select max(id) from final_lm")
    q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
    print q[0]
    #result = {'maxid': q.fetchone()[0]}

def temp_table_test():
    help(BaseTemp)
    help(TempDYW)

def test_parking():
    q = db.session.query(Parking).filter(Parking.id==1).first()
    #help(q)
    print q.id
    print q.date_created
    print q.content

if __name__ == '__main__':
    test_parking()


