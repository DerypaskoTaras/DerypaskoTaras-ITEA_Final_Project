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


cat1 = Category(title='Электроника')
cat1.save()

cat2 = Category(title='Бытовая техника')
cat2.save()
cat1.add_subcategory(cat2)

cat3 = Category(title='Крупная бытовая техника')
cat3.save()
cat2.add_subcategory(cat3)

c1 = Category(title='Холодильники')
c1.save()
cat3.add_subcategory(c1)

p1 = Product(title='Холодильник с морозильной камерой Samsung RB37J5000SA', price=12000, discount=30, description='Samsung RB37J5000SA – практичный и надежный холодильник с классом энергоэффективности A+. Прибор относится к отдельностоящим двухкамерным моделям и оснащен инверторным компрессором. Он заключен в корпус размерами 595x2006x675 мм, предусматривает электронное управление, предоставляет для размещения любых продуктов питания 367 л внутреннего пространства (общий полезный объем). Среди ключевых особенностей Samsung RB37J5000SA отметим наличие системы Multi Flow для равномерного распределения холодного воздуха,'
                                                                                                                 ' технологии No Frost, специального контейнера Fresh Zone для идеального хранения мяса и рыбы, регулируемых дверных кармашков и большого выдвижного ящика Full Open Box в морозилке. За эффективное освещение всего содержимого отвечает верхняя LED-лампа. Пользователи быстро найдут то, что им нужно. Если говорить о времени автономного поддержания холода, оно достигает 18 ч.', category=c1)
p1.save()
file2 = open('holod.jpeg', 'rb')
p1.image.put(file2)
p1.save()
file2.close()

c2 = Category(title='Стиральные машины')
c2.save()
cat3.add_subcategory(c2)
p2 = Product(title='Стиральная машина узкая SAMSUNG WF60F1R2E2WDUA', price=10500, discount=10, description='Барабан машины может вместить до 6 кг стирки, а для удобства потребителя размер дверцы увеличен до 460 мм, что обеспечит легкую загрузку и извлечение объемных вещей. Автоматическая стиральная машина Samsung WF60F1R2E2WDUA при габаритах 600x850x450 мм, имеет вес 56 кг. Данная модель оборудована керамическим нагревательным элементом, который быстро нагревается и соответственно эффективно расходует электроэнергию. Керамика предотвращает образование накипи, что избавит вас от необходимости использовать дополнительную бытовую химию для удаления налета. Система безопасности Volt Control создана для защиты от перепадов напряжения, устройству не страшны колебания напряжения в сети в диапазоне ± 25%', category=c2)
p2.save()
file = open("nophoto.jpg", 'rb')
p2.image.put(file)
p2.save()
file.close()
p3 = Product(title='Стиральная машина автоматическая LG F2J3WS2W', price=11800, description='Автоматическая стиральная машина LG F2J3WS2W с фронтальной загрузкой изготовлена в белом цвете с серебристым люком. Она относится к классу энергопотребления А+++ и способна за один цикл качественно выстирать до 6,5 кг белья. Технология 6 Motion вращает 44-литровый пузырьковый барабан шестью разнообразными способами, благодаря чему загрязнения эффективно удаляются, а одежда не повреждается и сохраняет внешний вид. Чтобы справиться со сложными пятнами или осуществить антиаллергенную обработку вещей, следует воспользоваться программой SpaSteam, воздействующей на них паром. Стабильную и долговременную эксплуатацию обеспечивает надёжный и малошумящий инверторный двигатель с прямым приводом Inverter Direct Drive, который, к тому же, экономно потребляет электроэнергию. Система мобильной диагностики Smart Diagnosis контролирует работоспособность модели во время работы. Автоматическая стиральная машина LG F2J3WS2W оборудована защитой от перепадов напряжения и функцией блокировки от воздействия детей.', category=c2)
p3.save()
c3 = Category(title='Посудомоечные машины')
c3.save()
cat3.add_subcategory(c3)

cat4 = Category(title='Встраеваемая бытовая техника')
cat4.save()
cat2.add_subcategory(cat4)

cat5 = Category(title='Климатическая техника')
cat5.save()
cat2.add_subcategory(cat5)

cat6 = Category(title='Ноутбуки и компьютеры')
cat6.save()
cat1.add_subcategory(cat6)

cat7 = Category(title='Ноутбуки')
cat7.save()
cat6.add_subcategory(cat7)

cat8 = Category(title='Компьютеры')
cat8.save()
cat6.add_subcategory(cat8)
