from flask import Flask
from flask_restful import Api
import IteaProject.app.api.resources as res

app = Flask(__name__)
api = Api(app)

api.add_resource(res.UserResources, '/users', '/users/<user_id>')
api.add_resource(res.ProductResources, '/products', '/products/<product_id>')
api.add_resource(res.CategoryResources, '/categories', '/categories/<category_id>')
api.add_resource(res.CartResources, '/carts', '/carts/<carts_id>')
api.add_resource(res.NewsResources, '/news', '/news/<news_id>')
api.add_resource(res.SuppliersResources, '/suppliers', '/suppliers/<supplier_id>')

app.run(host='127.0.0.1', port=27018, debug=True)