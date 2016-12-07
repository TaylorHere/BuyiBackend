#coding:utf-8
###########################框架基础######################################################
from SinglePage.singlepage import register,app
from Model.Base import db_session
###########总数11############业务模型####################################################
from Model.Association_market_pedlar import Association_market_pedlar
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
	Association_market_pedlar:'/association/market_pedlar/',
	Association_specie_supplier:'/association/species_suppliers/',
	Association_supplier_market:'/association/suppliers_markets/',
	Login:'/logins/',
	Market:'/markets/',
	Order:'/orders/',
	Pedlar:'/pedlars/',
	Permission:'/permissions/',
	Specie:'/species/',
	Supplier:'/suppliers/',
	User:'/users/',
	Documents:'/doc/',
	Query:'/query/',
}

for model in url:
	register(model,url[model])
# request结束时断开session链接
# 如果request遇到db错误，自动rollback事务
@app.teardown_request
def teardown_request(exception):
    if exception:
    	print 'auto rollback'
        db_session.rollback()
        db_session.remove()
    db_session.remove()
###########################测试服务######################################################
if __name__ == '__main__':
	app.run(debug=True,port=8080)
# TODO 自动回滚未工作
