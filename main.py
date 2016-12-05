#coding:utf-8
from SinglePage.singlepage import register,app

from Model.Base import db_session
from Model.User import User 
from Model.Permission import Permission
from Model.Order import Order

url = {
	User:'/users/',
	Permission:'/permissions/',
	Order:'/orders/',
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