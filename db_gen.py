from app.models.models import Category, Product, Supplier, Parameters


def add_photo(object_, photo):
    file = open(photo, 'rb')
    object_.image.put(file)
    object_.save()
    file.close()


supplier = Supplier.objects.create(name='<<ОАО Тайфун>>')

ref_parameters1 = Parameters(width=59.5, height=203, weight=74, power=254)
ref_parameters2 = Parameters(width=60, height=203, weight=85, power=273)
wash_parameters1 = Parameters(width=60, height=84, weight=57, power=500)
heater_parameters1 = Parameters(width=68, height=44, weight=10, power=1200)

appliances = Category.objects.create(title='Бытовая техника')


large_home_appliances = Category.objects.create(title='Крупная бытовая техника')
appliances.add_subcategory(large_home_appliances)

refrigerator = Category.objects.create(title='Холодильники')
large_home_appliances.add_subcategory(refrigerator)

refrigerator1 = Product.objects.create(
    title='Холодильник с морозильной камерой LG DoorCooling+ GA-B509SLKM',
    description='Современный двухкамерный холодильник LG GA-B509SLKM может располагаться практически в любом месте и '
                'гарантирует отменное хранение запасов продуктов в охлаждённом и замороженном виде. Двухконтурный '
                'прибор с системой No Frost и классом энергопотребления А++ оснащён линейным компрессором, '
                'который обеспечит стабильную и надёжную работу, с низким уровнем шума – до 36 дБ. В холодильной '
                'камере, объёмом 277 литров, с многопоточной системой охлаждения Multi Air Flow и 5 полками можно '
                'разместить большой запас продуктов, которые будут храниться в одинаковом температурном режиме. '
                'Антибактериальный уплотнитель не допустит проникновение бактерий в камеру.',
    price=14499,
    discount=10,
    category=refrigerator,
    supplier=supplier,
    parameters=ref_parameters1
)
add_photo(refrigerator1, 'ref1.jpg')

refrigerator2 = Product.objects.create(
    title='Холодильник с морозильной камерой Bosch KGN39UL316',
    description='Холодильник с нижней морозильной камерой Bosch KGN39UL316 серебристого цвета будет гармонично '
                'смотреться в любом кухонном интерьере. Модель, полезным объёмом 366 литров, разработана с двумя '
                'независимыми контурами охлаждения. Такая конструкция позволяет регулировать температурный режим в '
                'каждой камере отдельно или отключать одну из них. Холодильная камера, объёмом 279 литров, '
                'с многопоточной системой охлаждения MultiAirflow обеспечивает одинаковый температурный режим на всех '
                'полочках и отделениях, чтобы качественно и длительно хранить упаковки и ёмкости с продуктами. '
                'Агрегат оборудован фильтром и системой защиты от образования бактерий AntiBacteria, '
                'создавая безопасные условия хранения еды.',
    price=12999,
    category=refrigerator,
    supplier=supplier,
    parameters=ref_parameters2
)
add_photo(refrigerator2, 'ref2.jpg')

washing_machine = Category.objects.create(title='Стиральные машины')
large_home_appliances.add_subcategory(washing_machine)

washing_machine1 = Product.objects.create(
        title='Стиральная машина автоматическая Beko WUE7636XCW',
        description='Стиральная машина Beko WUE7636XCW представляет собой отдельно стоящее устройство в белом корпусе '
                    'с серебристым люком. В неё через фронтальный люк загружается до 7 кг сухого белья, '
                    'которое отжимается с максимальной скоростью 1200 оборотов в минуту. Устройство класса '
                    'энергопотребления А+++ оборудовано надёжным и экономичным инверторным двигателем ProSmart и '
                    'никелевым нагревателем. Моющее средство используется полностью благодаря системе AquaFusion. '
                    'Применение пара, поступающего из нижней части барабана Aquawave c волновой перфорацией, '
                    'обеспечивает качественную очистку и избавление от складок одежды из деликатных тканей.',
        price=7677,
        category=washing_machine,
        supplier=supplier,
        parameters=wash_parameters1
)
add_photo(washing_machine1, 'wash1.jpg')


air_conditioning_equipment = Category.objects.create(title='Климатическая техника')
appliances.add_subcategory(air_conditioning_equipment)

heater = Category.objects.create(title='Обогреватели')
air_conditioning_equipment.add_subcategory(heater)

heater1 = Product.objects.create(
    title='Обогреватель Xiaomi SmartMi Electric Heater Smart Edition White (DNQZNB03ZM)',
    description='Обогреватель SmartMi Electric Heater Smart Edition White (DNQZNB03ZM) выполнен в напольном '
                'исполнении в оцинкованном металлическом корпусе белого цвета. Он оборудован нагревательным элементом '
                'из железо-хром-алюминиевого сплава мощностью 1,6 кВт и создаёт конвекционную циркуляцию тёплого '
                'воздуха. Модель предназначена для использования в помещениях площадью 10-15 кв.м. На её сенсорном '
                'дисплее отображается значение влажности и температуры воздуха в помещении. Особенностью прибора '
                'является возможность управления со смартфона. Заданная пользователем температура в диапазоне 16С-32С '
                'поддерживается с помощью интегрированного датчика и термостата.',
    price=2800,
    discount=20,
    category=heater,
    supplier=supplier,
    parameters=heater_parameters1
)
add_photo(heater1, 'heat1.jpg')

conditioner = Category.objects.create(title='Кондиционеры')
air_conditioning_equipment.add_subcategory(conditioner)


home_appliances = Category.objects.create(title='Техника для дома')
appliances.add_subcategory(home_appliances)

vacuum_cleaner = Category.objects.create(title='Пылесосы')
home_appliances.add_subcategory(vacuum_cleaner)

vacuum_cleaner1 = Product.objects.create(
    title='Вертикальный+ручной пылесос (2в1) Rowenta RH9490WO',
    description='Вертикальный+ручной пылесос (2в1) Rowenta RH9490WO является многофукциональным устройством, '
                'с помощью которого можно провести качественную сухую, а также влажную уборку (с насадкой Aqua). '
                'Модель обладает мощностью всасывания 100 Вт, которая регулируется переключателем на ручке. Прибор '
                'оборудован аккумулятором, который обеспечивает непрерывную работу в течение 35 минут, после чего '
                'требуется 3-часовая зарядка. Циклонная технология Air Force, собирая весь мусор в контейнер ёмкостью '
                '0,65 литра, сохраняет высокую производительность, не зависимо от степени заполнения пылесборника.',
    price=11159,
    discount=15,
    category=vacuum_cleaner,
    supplier=supplier,
)
add_photo(vacuum_cleaner1, 'vac1.jpg')

smoothing_iron = Category.objects.create(title='Утюги')
home_appliances.add_subcategory(smoothing_iron)

smoothing_iron1 = Product.objects.create(
    title='Утюг с паром Bosch TDA3026110',
    description='Стильный утюг с паром Bosch TDA3026110 мощностью 2400 Вт выполнен в белом и фиолетовом цветах. '
                'Компактный прибор оснащён алюминиевой подошвой с керамическим покрытием Ceranium Clissee, '
                'которая быстро разогревается, отлично скользит по всем видам тканей и не прилипает к ним. Резервуара '
                'для воды объёмом 320 мл достаточно для обеспечения паром одной продолжительной глажки. Максимальная '
                'скорость подачи пара - 40 г/мин - позволяет справиться с вещами из плотных тканей и разгладить очень '
                'мятые вещи. Скорость подачи пара можно регулировать 6 уровнями, выбирая оптимальную в зависимости от '
                'вида разглаживаемой ткани, её толщины и количества складок. Используя турбо удар силой 160 г/мин, '
                'можно смягчить определенные участки белья и разгладить сложные складки.',
    price=1099,
    category=smoothing_iron,
    supplier=supplier,
)
add_photo(smoothing_iron1, 'smooth1.jpg')


housing = Category.objects.create(title='Все для дома')



furniture = Category.objects.create(title='Мебель')
housing.add_subcategory(furniture)

bed = Category.objects.create(title='Кровати')
furniture.add_subcategory(bed)

bed1 = Product.objects.create(
    title='Односпальная кровать ОЛИМП Лика Стандарт с изножьем без ящиков',
    description='Односпальная кровать • классическая • длина спального места: 200 см • ширина спального места: 90 см '
                '• материал корпуса: дерево - бук • цвет: в ассортименте: бук , венге, белый, темный орех, '
                'светлый орех.',
    price=2792,
    category=bed,
    supplier=supplier,
)
add_photo(bed1, 'bed1.jpg')

dishes = Category.objects.create(title='Посуда')
housing.add_subcategory(dishes)

saucepan = Category.objects.create(title='Кастрюли')
dishes.add_subcategory(saucepan)

saucepan1 = Product.objects.create(
    title='Кастрюля Krauff 26-238-009',
    description='Стильная и удобная посуда от немецкого производителя радует хозяек не один год и кастрюля Krauff '
                '26-238-009, емкостью 2 л, не станет исключением. Она изготовлена из высококачественной нержавеющей '
                'стали, которая отличается прочностью и устойчивостью к царапинам. Поэтому мыть ее можно как вручную, '
                'так и в посудомойке. Утолщенное многослойное дно не допустит пригорания и прилипания пищи, '
                'оно аккумулирует тепло и равномерно распределяет его по всей поверхности. Что значительно ускоряет '
                'процесс приготовления. Крышка из термостойкого стекла имеет отверстия для выхода пара и слива '
                'жидкости. Обратите внимание, что кастрюля Krauff 26-238-009 имеет продуманный дизайн, она с двух '
                'сторон имеет носики для слива отвара.',
    price=368,
    category=saucepan,
    supplier=supplier,
)
add_photo(saucepan1, 'saucepan1.jpg')

knife = Category.objects.create(title='Ножи')
dishes.add_subcategory(knife)

