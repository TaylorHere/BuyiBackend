# coding:utf-8
import requests
import json
import random
import time
import sys



def _post(url=None, data=None, headers=None, name=None):
    start = time.time()
    _url = host + url
    r = requests.post(_url, json=data, headers=headers)
    end = time.time()
    t = end - start
    if r.status_code == 200:
        print name + '成功    耗时：' + str(t)
    else:
        print name + '失败!!!!    耗时：' + str(t)
    return r


def new_user(user):

    data = {
        "pwd": user.pwd,
        "nickname": user.nickname,
        "img_url": user.img,
        "telephone": user.telephone,
        "sex": user.sex
    }
    r = _post(url='/users/', data=data, name='新建用户')
    try:
        data = r.json().get('data')
        user.user_id = data.get('id')
        user.openid = data.get('openid')
    except:
        pass


def add_permission(user):
    data = {
        "name": user.permission,
        "user_id": user.user_id
    }
    r = _post(url='/permissions/', data=data,
              name='赋予用户 ' + str(user.user_id) + ' Base权限')


def user_login(user):
    data = {
        'openid': user.openid,
        'pwd': user.pwd
    }
    r = _post(url='/logins/', data=data,
              name='用户 ' + str(user.user_id) + ' 登录')
    try:
        user.base = r.json().get('data').get('base')
    except Exception as e:
        pass


def new_speice(user, speice):
    headers = {'XXX-user-id': user.user_id}
    _data = [
        {
            'parent_id': -1,
            'tag': '一级',
            'name': '水果'
        },
        {
            'parent_id': 1,
            'tag': '二级',
            'name': '西瓜'
        },
        {
            'parent_id': 1,
            'tag': '二级',
            'name': '西红柿'
        },
    ]
    _data = random.choice(_data)
    data = {
        "parent_id": _data['parent_id'],
        "tag": _data['tag'],
        "name": _data['name'],
        "img_url": "xxxxxxx.jpg",
        "describe": "xxx"
    }
    r = _post(url='/species/', data=data, headers=headers, name='新建种类')
    try:
        speice.id = r.json().get('data').get('id')
    except Exception as e:
        pass


def new_supplyer(user, supplier):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "name":"成都托普蔬菜基地",
        "address":"成都托普",
        "tag":"一级供货商"
    }
    r = _post(url='/suppliers/', data=data, headers=headers, name='新建供应商')
    try:
        supplier.id = r.json().get('data').get('id')
    except Exception as e:
        pass

def new_market(user, market):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "name":"成都托普菜市场",
    }
    r = _post(url='/markets/', data=data, headers=headers, name='新建市场')
    try:
        market.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def new_pedlar(user, pedlar):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "name":"成都托普猪肉一号摊位",
    }
    r = _post(url='/pedlars/', data=data, headers=headers, name='新建摊贩')
    try:
        pedlar.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def new_association_species_suppliers(user, speice, supplier, speice_supplier):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "specie_id": speice.id,
        "supplier_id": supplier.id,
        'creat_time':'',
        'uuid':''
    }
    r = _post(url='/association/species_suppliers/',
              data=data, headers=headers, name='新建供应商与种类关联表')
    try:
        speice_supplier.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def new_association_suppliers_markets(user, supplier,market,supplier_market,order):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "market_id":market.id,
        "supplier_id":supplier.id,
        'creat_time':'',
        'uuid':'',
        'order_id':order.id
    }
    r = _post(url='/association/suppliers_markets/',
              data=data, headers=headers, name='新建供应商与市场关联表')
    try:
        supplier_market.id = r.json().get('data').get('uuid')
    except Exception as e:
        pass
def new_association_markets_pedlar(user, market,pedlar,market_pedlar,supplier_market,order):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "market_id":market.id,
        "pedlar_id":pedlar.id,
        'creat_time':'',
        'uuid':'',
        "from_uuid":supplier_market.id,
        'order_id':order.id
    }
    r = _post(url='/association/market_pedlar/',
              data=data, headers=headers, name='新建市场与摊贩关联表')
    try:
        market_pedlar.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def new_order(user,order):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "price":10
    }
    r = _post(url='/orders/',
              data=data, headers=headers, name='新建订单')
    try:
        order.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def trace(user,pedlar):
    headers = {'XXX-user-id': user.user_id}
    r = requests.get(url=host+'/pedlars/?filter=id='+str(pedlar.id),headers=headers)
    data = r.json().get('data')
    for d in data:
        print u'摊贩名称: '+d.get('name')
        r = requests.get(url=host+'/association/market_pedlar/?filter=pedlar_id='+str(d.get('id')),headers=headers)
        data = r.json().get('data')
        for d in data:
            uuid = d.get('from_uuid')
            time = d.get('creat_time')
            market_id = d.get('market_id')
            print u'摊贩／市场交接时间: '+time
            r = requests.get(url=host+'/markets/?filter=id='+str(market_id),headers=headers)
            data = r.json().get('data')
            for d in data:
                name = d.get('name')
                print u'上游市场名称: '+name
                r = requests.get(url=host+'/association/suppliers_markets/?filter=_uuid='+"\'"+uuid+"\'",headers=headers)
                data = r.json().get('data')
                for d in data:
                    supplier_id = d.get('supplier_id')
                    time = d.get('creat_time')
                    print u'供货商／市场交接时间: '+time
                    r = requests.get(url=host+'/suppliers/?filter=id='+str(supplier_id),headers=headers)
                    name = r.json().get('data')[0].get('name')
                    print u'供货商名称: '+name
    
class User():
    user_id = -1
    base = ''
    pwd = "TaylorHere"
    nickname = "TaylorHere"
    img = "https://www.baidu.com/link?url=NrHckADZl95r3xeCcGoTNaOnK2XrEaZmn-ojglDQB__ua0vNXkMw19LJHCnJ6waEvk_vlV73I5qt4jHZvrMhJHBhAplFktgYN7ScecrthcdJ_TTQXPYfF0bZPODpCDGDIjQwZkCREeKVCQN_SxXXFIsUZuPlcAf2CgJskkpsDZq&wd=&eqid=867d4e430000ade50000000558456f0c"
    telephone = ''
    sex = "male"
    openid = ''
    permission = 'Base'


class Speice():
    id


class Supplier():
    id

class Market():
    id

class Speice_supplier():
    id
class Market_Pedlar():
    id
class Supplier_market():
    id
class Pedlar():
    id
class Order():
    id
if __name__ == '__main__':
    try:
        local = bool(sys.argv[1])
        loop = int(sys.argv[2])
        if local:
            host = 'http://127.0.0.1:8081'
        else:
            host = 'http://seize.space:8080'
    except Exception as e:
        loop = 1
        host = 'http://seize.space:8080'
    start = time.time()
    for x in xrange(0,loop):
        # 随机生成手机号
        header = random.choice(['151', '135', '185', '137', '187', '181'])
        body = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        tail = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        telephone = header + ''.join(body) + ''.join(tail)
        user = User()
        user.telephone = telephone
        print '########用户模块########'
        new_user(user)
        add_permission(user)
        user_login(user)
        print '########供货商模块######'
        supplier = Supplier()
        new_supplyer(user, supplier)
        speice = Speice()
        new_speice(user, speice)
        speice_supplier = Speice_supplier()
        new_association_species_suppliers(user, speice, supplier, speice_supplier)
        print '#########市场模块######'
        market = Market()
        new_market(user, market)
        supplier_market = Supplier_market()
        # 发货
        order=Order()
        new_order(user,order)
        new_association_suppliers_markets(user, supplier,market,supplier_market,order)
        print '#########商贩模块######'
        pedlar = Pedlar()
        new_pedlar(user, pedlar)
        market_pedlar = Market_Pedlar()
        new_association_markets_pedlar(user, market,pedlar,market_pedlar,supplier_market,order)
        print '##########溯源##########'
        trace(user,pedlar)
        print '##########溯源##########'
    end = time.time()
    print '总耗时：' + str(end - start)
