from flask import Flask
from flask_restful import Api
from .app.api.resources import (
    UserResources,
    ProductResources,
    CategoryResources,
    CartResources,
    NewsResources,
    SuppliersResources
)

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResources, '/users', '/users/<user_id>')
api.add_resource(ProductResources, '/products', '/products/<product_id>')
api.add_resource(CategoryResources, '/categories', '/categories/<category_id>')
api.add_resource(CartResources, '/carts', '/carts/<carts_id>')
api.add_resource(NewsResources, '/news', '/news/<news_id>')
api.add_resource(SuppliersResources, '/suppliers', '/suppliers/<supplier_id>')

app.run(host='127.0.0.1', port=27018, debug=True)
