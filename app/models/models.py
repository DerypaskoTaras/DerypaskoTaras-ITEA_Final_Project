from collections import Counter
import mongoengine as me
import datetime

me.connect('TS')


class Category(me.Document):
    title = me.StringField(min_length=2, max_length=128, required=True)
    description = me.StringField(max_length=2048)
    parent = me.ReferenceField('self')
    subcategories = me.ListField(me.ReferenceField('self'))

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    def add_subcategory(self, subcategory: 'Category'):
        subcategory.parent = self
        self.subcategories.append(subcategory)
        subcategory.save()
        self.save()

    def get_products(self):
        return Product.objects(
            category=self,
            in_stock=True
        )


class Parameters(me.EmbeddedDocument):
    width = me.FloatField()
    height = me.FloatField()
    weight = me.FloatField()
    power = me.IntField(min_value=1)


class Product(me.Document):
    title = me.StringField(min_length=2, max_length=128, required=True)
    description = me.StringField(max_length=2048)
    price = me.DecimalField(force_string=True, required=True, min_value=0)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    in_stock = me.BooleanField(default=True)
    category = me.ReferenceField(Category)
    supplier = me.ReferenceField('Supplier')
    image = me.FileField(required=True)
    parameters = me.EmbeddedDocumentField(Parameters)

    @classmethod
    def get_discount_products(cls):
        return cls.objects(discount__gt=0)

    def get_product_info(self):
        product_info = f'{self.title}\nОписание :\n{self.description}' \
                       f'\nХарактеристики :\n{self.parameters}'
        if self.discount > 0:
            discount_price = (self.price - (self.price / 100) * self.discount)
            return product_info + f'\nСтарая цена : {self.price}\nЦена со скидкой : {discount_price}'
        return product_info + f'\nЦена : {self.price}'


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    name = me.StringField(min_length=2, max_length=256)
    phone = me.StringField(min_length=8, max_length=12)
    address = me.StringField(min_length=4, max_length=128)

    @classmethod
    def initial_create(cls, telegram_id: int, name: str):
        try:
            cls.objects.create(
                telegram_id=telegram_id,
                name=name
            )
        except me.errors.NotUniqueError:
            pass

    def get_cart(self):
        cart = Cart.objects.filter(user=self, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=self)
        return cart

    def get_products_in_cart(self):
        cart = Cart.objects.filter(user=self, is_active=True).first()
        return dict(Counter(cart.products))


class Admin(me.Document):
    login = me.StringField(min_length=6, max_length=64, required=True, unique=True)
    password = me.StringField(min_length=8, max_length=128, required=True)
    email = me.EmailField()


class Supplier(me.Document):
    name = me.StringField(required=True, min_length=2, max_length=256)


class News(me.Document):
    title = me.StringField(min_length=2, max_length=256, required=True)
    body = me.StringField(min_length=2, max_length=4096, required=True)
    creation_date = me.DateTimeField()
    modified_date = me.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(News, self).save(*args, **kwargs)

    @classmethod
    def get_news(cls):
        return cls.objects()


class Review(me.Document):
    rating = me.IntField(min_value=0, max_value=10)
    comment = me.StringField(min_length=1, max_length=256)
    product = me.ReferenceField(Product)
    user = me.ReferenceField(User)


class Cart(me.Document):
    user = me.ReferenceField(User)
    products = me.ListField(me.ReferenceField(Product))
    is_active = me.BooleanField(default=True)
    created = me.DateTimeField(default=datetime.datetime.now())

    def add_product(self, product: Product):
        self.products.append(product)
        self.save()

    def delete_products_in_cart(self):
        self.products = []
        self.save()


news = News(title='Мега - распродажа', body='Только 07.11.2020 года в нашем магазине пройдет мега - распродажа товаров.')
news.save()
