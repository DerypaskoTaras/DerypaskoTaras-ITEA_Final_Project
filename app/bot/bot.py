import json
from .config import (
    TOKEN,
    CATEGORY_TAG,
    ADD_TO_CART_TAG,
    DELETE_ORDER_TAG,
    COMPLETE_ORDER_TAG)
from .keyboards import START_KB
import app.bot.utils as bot_utils
from .texts import GREETINGS, PICK_CATEGORY
from ..models.models import Category, Product, User, News
from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    User.initial_create(message.chat.id, message.from_user.first_name)
    user = User.objects.get(telegram_id=message.chat.id)
    user.get_cart()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(button) for button in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(
        message.chat.id,
        GREETINGS,
        reply_markup=kb
    )


@bot.message_handler(func=lambda c: bot_utils.check_message_match(c, 'category'))
def show_categories(message):
    kb = bot_utils.generate_categories_kb(Category.get_root_categories())
    bot.send_message(
        message.chat.id,
        PICK_CATEGORY,
        reply_markup=kb
    )


@bot.message_handler(func=lambda n: bot_utils.check_message_match(n, 'news'))
def show_news(message):
    for news in News.get_news():
        bot.send_message(
            message.chat.id,
            f'{news.title}\n'
            f'{news.body}\n'
            f'{news.modified_date.strftime("%Y.%m.%d %H:%M:%S")}'
        )


@bot.message_handler(func=lambda d: bot_utils.check_message_match(d, 'discount'))
def show_discount_products(message):
    if len(Product.get_discount_products()) != 0:
        for discount_product in Product.get_discount_products():
            kb = bot_utils.generate_add_to_cart_button(str(discount_product.id))
            bot.send_photo(
                message.chat.id,
                discount_product.image.read(),
                caption=discount_product.get_product_info(),
                reply_markup=kb
            )
    else:
        bot.send_message(
            message.chat.id,
            f'В данный момент нет товаров со скидками'
        )


@bot.message_handler(func=lambda c: bot_utils.check_message_match(c, 'cart'))
def show_products_in_cart(message):
    products_in_cart = User.get_products_in_cart(message.chat.id)
    if len(products_in_cart) == 0:
        bot.send_message(
            message.chat.id,
            f'Корзина пуста'
        )
    else:
        total_price = 0
        for product, quantity in products_in_cart.items():
            price_all_products = product.price * quantity
            total_price += price_all_products
            bot.send_message(
                message.chat.id,
                f'Товар : {product.title}\n'
                f'Количество : {quantity}\n'
                f'Стоимость за {quantity} ед. : {price_all_products}'
            )
        kb = bot_utils.generate_complete_or_delete_order_kb(str(User.get_cart(message.chat.id)))
        bot.send_message(
            message.chat.id,
            f'Стоимость всех товаров : {total_price}',
            reply_markup=kb
        )


@bot.callback_query_handler(func=lambda c: bot_utils.check_call_tag_match(c, CATEGORY_TAG))
def categories(call):
    category = Category.objects.get(id=json.loads(call.data)['id'])
    if category.subcategories:
        kb = bot_utils.generate_categories_kb(category.subcategories)
        bot.edit_message_text(
            category.title,
            call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb
        )
    else:
        if len(category.get_products()) != 0:
            for product in category.get_products():
                kb = bot_utils.generate_add_to_cart_button(str(product.id))
                bot.send_photo(
                    call.message.chat.id,
                    product.image.read(),
                    caption=product.get_product_info(),
                    reply_markup=kb
                )
        else:
            bot.send_message(
                call.message.chat.id,
                f'В этой категории еще нет товаров'
            )


@bot.callback_query_handler(func=lambda a: bot_utils.check_call_tag_match(a, ADD_TO_CART_TAG))
def handle_add_to_cart(call):
    product_id = json.loads(call.data)['id']
    product = Product.objects.get(id=product_id)
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_cart()
    cart.add_product(product)
    bot.send_message(
        call.message.chat.id,
        f'Товар "{product.title}" добавлен в корзину.'
    )


@bot.callback_query_handler(func=lambda d: bot_utils.check_call_tag_match(d, DELETE_ORDER_TAG))
def delete_order(call):
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_cart()
    if len(cart.products) != 0:
        cart.delete_products_in_cart()
        bot.send_message(
            call.message.chat.id,
            f'Корзина удалена'
        )


@bot.callback_query_handler(func=lambda c: bot_utils.check_call_tag_match(c, COMPLETE_ORDER_TAG))
def complete_order(call):
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_cart()
    if len(cart.products) != 0:
        cart.is_active = False
        cart.save()
        user.get_cart()
        bot.send_message(
            call.message.chat.id,
            f'Благодарим за покупку.'
        )
