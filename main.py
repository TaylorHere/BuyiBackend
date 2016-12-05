#coding:utf-8
from SinglePage.singlepage import register,app

from Model.Base import db_session
#coding:utf-8
from Model.User import User 
from Model.Login import Login 
from Model.Permission import Permission
from Model.Order import Order
from Model.Association_specie_supplier import Association_specie_supplier
from Model.Specie import Specie
from Model.Supplier import Supplier
from SinglePage.Support.document import Documents
from SinglePage.Support.query import Query

url = {
	User:'/users/',
	Login:'/logins/',
	Permission:'/permissions/',
	Order:'/orders/',
	Documents:'/doc/',
	Query:'/query/',
	Association_specie_supplier:'/association/species_suppliers/',
	Specie:'/species/',
	Supplier:'/suppliers/'
}

for model in url:
	register(model,url[model])

if __name__ == '__main__':
	app.run(debug=True,port=8081)
# TODO 自动回滚未工作
@app.teardown_request
def teardown_request(exception):
    if exception:
        db_session.rollback()
        db_session.remove()
    db_session.remove()