from app.models.models import Category, Product, Supplier, News
import mongoengine as me

me.connect('TS')

p_cat1 = Category.objects.create(title='Бытовая техника')

bcat1 = Category.objects.create(title='Крупная бытовая техника')
p_cat1.add_subcategory(bcat1)

bcat2 = Category.objects.create(title='Климатическая техника')
p_cat1.add_subcategory(bcat2)

bcat3 = Category.objects.create(title='Техника для дома')
p_cat1.add_subcategory(bcat3)


p_cat2 = Category.objects.create(title='Все для дома')

hcat1 = Category.objects.create(title='Мебель')
p_cat2.add_subcategory(hcat1)

hcat2 = Category.objects.create(title='Посуда')
p_cat2.add_subcategory(hcat2)


