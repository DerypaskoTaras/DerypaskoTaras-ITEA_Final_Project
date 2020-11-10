from flask_restful import Resource
from flask_restful import request
from app.models.models import User, Product, Category, Cart, News, Supplier
import json


class UserResources(Resource):

    def get(self, user_id=None):
        if user_id:
            data_result = User.objects.get(telegram_id=user_id)
        else:
            data_result = User.objects()
        data_result = json.loads(data_result.to_json())
        return data_result


class ProductResources(Resource):

    def get(self, product_id=None):
        if product_id:
            data_result = Product.objects.get(id=product_id)
        else:
            data_result = Product.objects()
        data_result = json.loads(data_result.to_json())
        return data_result

    def post(self):
        product = Product.objects.create(**request.json)
        return json.loads(product.to_json())

    def put(self, product_id):
        product = Product.objects(id=product_id)
        product.update(**request.json)
        return json.loads(product.to_json())

    def delete(self, product_id):
        product = Product.objects(id=product_id)
        product.delete()
        return json.loads(product.to_json())


class CategoryResources(Resource):

    def get(self, category_id=None):
        if category_id:
            data_result = Category.objects.get(id=category_id)
        else:
            data_result = Category.objects()
        data_result = json.loads(data_result.to_json())
        return data_result

    def post(self):
        category = Category.objects.create(**request.json)
        return json.loads(category.to_json())

    def put(self, category_id):
        category = Category.objects(id=category_id)
        category.update(**request.json)
        return json.loads(category.to_json())

    def delete(self, category_id):
        category = Category.objects(id=category_id)
        category.delete()
        return json.loads(category.to_json())


class CartResources(Resource):

    def get(self, cart_id=None):
        if cart_id:
            data_result = Cart.objects.get(is_active=False, id=cart_id)
        else:
            data_result = Cart.objects(is_active=False)
        data_result = json.loads(data_result.to_json())
        return data_result

    def delete(self, cart_id):
        cart = Cart.objects(id=cart_id)
        cart.delete()
        return json.loads(cart.to_json())


class NewsResources(Resource):

    def get(self, news_id=None):
        if news_id:
            data_result = News.objects.get(id=news_id)
        else:
            data_result = News.objects()
        data_result = json.loads(data_result.to_json())
        return data_result

    def post(self):
        news = News.objects.create(**request.json)
        return json.loads(news.to_json())

    def put(self, news_id):
        news = News.objects(id=news_id)
        news.update(**request.json)
        return json.loads(news.to_json())

    def delete(self, news_id):
        news = News.objects(id=news_id)
        news.delete()
        return json.loads(news.to_json())


class SuppliersResources(Resource):

    def get(self, supplier_id=None):
        if supplier_id:
            data_result = Supplier.objects.get(id=supplier_id)
        else:
            data_result = Supplier.objects()
        data_result = json.loads(data_result.to_json())
        return data_result

    def post(self):
        supplier = Supplier.objects.create(**request.json)
        return json.loads(supplier.to_json())

    def put(self, supplier_id):
        supplier = Supplier.objects(id=supplier_id)
        supplier.update(**request.json)
        return json.loads(supplier.to_json())

    def delete(self, supplier_id):
        supplier = Supplier.objects(id=supplier_id)
        supplier.delete()
        return json.loads(supplier.to_json())