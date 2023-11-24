import os
from flask import Flask
from flask_restful import Api
from db import db
from resources.product_resources import ProductListResource, ProductResource
from resources.orders import OrderResource
from resources.add_user import AddUser

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@192.168.128.3/FDS"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
api = Api(app)

api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/product/<int:product_id>', '/product')
api.add_resource(OrderResource, '/order/<int:order_id>', '/order')
api.add_resource(AddUser, '/user/<int:user_id>', '/user')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0')