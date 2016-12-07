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
            'parent_id': -1,
            'tag': '一级',
            'name': '水果'
        },
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
        "name":"成都托普蔬菜%s号基地" % random.choice(['1','2','3','4','5','6','7']),
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
        "name":"成都托普%s菜市场" % random.choice(['1','2','3','4','5','6','7']),
    }
    r = _post(url='/markets/', data=data, headers=headers, name='新建市场')
    try:
        market.id = r.json().get('data').get('id')
    except Exception as e:
        pass
def new_pedlar(user, pedlar):
    headers = {'XXX-user-id': user.user_id}
    data = {
        "name":"成都托普猪肉%s号摊位" % random.choice(['1','2','3','4','5','6','7']),
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
        "price":'%s' % random.choice([1,2,3,4,5,6,7,8,9,10]),
        "quantity":'%s' % random.choice([1,2,3,4,5,6,7,8,9,10]),
        "creat_time":''
    }
    r = _post(url='/orders/',
              data=data, headers=headers, name='新建订单')
    try:
        order.id = r.json().get('data').get('id')
        data={
            "order_id":order.id,
            "specie_id":2
        }
        _post(url='/association/species_orders/',
              data=data, headers=headers, name='新建订单')
    except Exception as e:
        pass
def trace(user,pedlar):
    import time
    start = time.time()
    headers = {'XXX-user-id': user.user_id}
    r = requests.get(url=host+'/pedlars/?filter=id='+str(pedlar.id),headers=headers)
    data = r.json().get('data')
    for d in data:
        print u'摊贩名称: '+d.get('name')
        r = requests.get(url=host+'/association/market_pedlar/?filter=pedlar_id='+str(d.get('id')),headers=headers)
        data = r.json().get('data')
        num = 0
        for d in data:
            num = num +1
            print u'    线路%s' % num
            uuid = d.get('from_uuid')
            creat_time = d.get('creat_time')
            market_id = d.get('market_id')
            order_id = d.get('order_id')
            print u'        订单号：%s'%order_id
            print u'        摊贩／市场交接时间: '+creat_time
            r = requests.get(url=host+'/markets/?filter=id='+str(market_id),headers=headers)
            data = r.json().get('data')
            for d in data:
                name = d.get('name')
                print u'        上游市场名称: '+name
                r = requests.get(url=host+"/association/suppliers_markets/?filter=order_id='%s'"% order_id ,headers=headers)
                data = r.json().get('data')
                for d in data:
                    supplier_id = d.get('supplier_id')
                    creat_time = d.get('creat_time')
                    print u'            供货商／市场交接时间: '+creat_time
                    r = requests.get(url=host+'/suppliers/?filter=id='+str(supplier_id),headers=headers)
                    name = r.json().get('data')[0].get('name')
                    print u'            供货商名称: '+name
    end =time.time()
    print u'溯源耗时：'+ str(end-start)
    
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
class Trance():
    id
def random_num():
    header = random.choice(['151', '135', '185', '137', '187', '181'])
    body = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
    tail = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
    return header + ''.join(body) + ''.join(tail)
if __name__ == '__main__':
    try:
        local = sys.argv[1]
        loop = int(sys.argv[2])
        if local == 'true':
            host = 'http://127.0.0.1:8081'
        else:
            host = 'http://seize.space:8080'
    except Exception as e:
        loop = 1
        host = 'http://seize.space:8080'
    start = time.time()
    for x in xrange(0,loop):
        # 随机生成手机号
        user = User()
        user.telephone = random_num()
        print '新建用户A'
        new_user(user)
        add_permission(user)
        user_login(user)
        print '新建用户B'
        userB = User()
        userB.telephone = random_num()
        new_user(userB)
        add_permission(userB)
        user_login(userB)
        print '用户A新建供应商A'
        supplierA = Supplier()
        new_supplyer(user, supplierA)
        speice = Speice()
        new_speice(user, speice)
        speice_supplier = Speice_supplier()
        new_association_species_suppliers(user, speice, supplierA, speice_supplier)
        print '用户B新建供应商B'
        supplierB = Supplier()
        new_supplyer(user, supplierB)
        speice = Speice()
        new_speice(user, speice)
        speice_supplier = Speice_supplier()
        new_association_species_suppliers(user, speice, supplierB, speice_supplier)
        print '用户A新建市场A'
        marketA = Market()
        new_market(user, marketA)
        print '用户B新建市场B'
        marketB = Market()
        new_market(userB, marketB)
        print '用户B新建商贩A'
        pedlarA = Pedlar()
        new_pedlar(userB, pedlarA)
        trance = Trance()
        trance.id =pedlarA.id
        print '用户A新建商贩B'
        pedlarB = Pedlar()
        new_pedlar(user, pedlarB)
        print '用户A新建商贩C'
        pedlarC = Pedlar()
        new_pedlar(user, pedlarC)

        print '供应商A生成订单A'
        orderA=Order()
        new_order(user,orderA)

        print '供应商B生成订单B'
        orderB=Order()
        new_order(user,orderB)
        
        print '供应商A发送订单A给市场A'
        supplier_market = Supplier_market()
        new_association_suppliers_markets(user, supplierA,marketA,supplier_market,orderA)
        
        print '供应商B发送订单B给市场A'
        supplier_market = Supplier_market()
        new_association_suppliers_markets(user, supplierB,marketA,supplier_market,orderB)

        print '供应商A发送订单A给市场B'
        market_pedlar = Market_Pedlar()
        new_association_suppliers_markets(user, supplierA,marketB,supplier_market,orderA)
        

        print '市场A发送订单A给商贩A'
        market_pedlar = Market_Pedlar()
        new_association_markets_pedlar(user, marketA,pedlarA,market_pedlar,supplier_market,orderA)
        
        print '市场A发送订单B给商贩A'
        market_pedlar = Market_Pedlar()
        new_association_markets_pedlar(user, marketA,pedlarA,market_pedlar,supplier_market,orderB)
        
        print '市场B发货给商贩B'
        market_pedlar = Market_Pedlar()
        new_association_markets_pedlar(user, marketB,pedlarB,market_pedlar,supplier_market,orderA)
        
        print '市场B发货给商贩C'
        market_pedlar = Market_Pedlar()
        new_association_markets_pedlar(user, marketB,pedlarC,market_pedlar,supplier_market,orderA)
        
        print '##########溯源##########'
        trace(userB,pedlarA)
        trace(user,pedlarB)
        trace(user,pedlarC)
        print '##########溯源##########'
    end = time.time()
    print '总耗时：' + str(end - start)
