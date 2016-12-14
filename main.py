# coding:utf-8
import __builtin__

if getattr(__builtin__, 'profile', None) is None:
    __builtin__.profile = lambda x: x
###########################框架基础######################################################
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from SinglePage.singlepage import register, app
from Model.Base import db_session
###########总数11############业务模型####################################################
from Model.Association_market_pedlar import Association_market_pedlar
from Model.Association_specie_order import Association_specie_order
from Model.Association_specie_supplier import Association_specie_supplier
from Model.Association_supplier_market import Association_supplier_market
from Model.Login import Login
from Model.Market import Market
from Model.Order import Order
from Model.Pedlar import Pedlar
from Model.Permission import Permission
from Model.Specie import Specie
from Model.Supplier import Supplier
from Model.User import User
###########################框架功能######################################################
from SinglePage.Support.document import Documents
from SinglePage.Support.query import Query

###########################接口注册######################################################
url = {
    Association_market_pedlar: '/association/market_pedlar/',
    Association_specie_order: '/association/species_orders/',
    Association_specie_supplier: '/association/species_suppliers/',
    Association_supplier_market: '/association/suppliers_markets/',
    Login: '/logins/',
    Market: '/markets/',
    Order: '/orders/',
    Pedlar: '/pedlars/',
    Permission: '/permissions/',
    Specie: '/species/',
    Supplier: '/suppliers/',
    User: '/users/',
    Documents: '/doc/',
    Query: '/query/',
}
exclude = [Documents, Query]
admin = Admin(app, template_mode='bootstrap3')
for model in url:
    register(model, url[model])
    if model not in exclude:
        admin.add_view(ModelView(model, db_session))


# request结束时断开session链接
# 如果request遇到db错误，自动rollback事务
@app.teardown_request
def teardown_request(exception):
    if exception:
        print 'auto rollback'
        db_session.rollback()
        db_session.remove()
    db_session.remove()

app.config['SECRET_KEY'] = 'SuperSecretKey'
###########################测试服务######################################################
if __name__ == '__main__':
    app.run(debug=True, port=8081)
# TODO 自动回滚未工作
