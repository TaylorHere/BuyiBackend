from SinglePage.singlepage import register,app
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
	app.run(debug=True,port=8080)
