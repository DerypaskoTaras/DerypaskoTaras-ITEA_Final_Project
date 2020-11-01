import json
from .config import TOKEN, CATEGORY_TAG, ADD_TO_CART_TAG
from .keyboards import START_KB
import app.bot.utils as bot_utils
from .texts import GREETINGS, PICK_CATEGORY
from ..models.models import Category, Product, User
from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    User.initial_create(message.chat.id, message.from_user.first_name)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(button) for button in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(
        message.chat.id,
        GREETINGS,
        reply_markup=kb
    )


@bot.message_handler(func=lambda m: bot_utils.check_message_match(m, 'category'))
def show_categories(message):
    kb = bot_utils.generate_categories_kb(Category.get_root_categories())
    bot.send_message(
        message.chat.id,
        PICK_CATEGORY,
        reply_markup=kb
    )


@bot.message_handler(func=lambda d: bot_utils.check_message_match(d, 'discount'))
def show_discount_products(message):
    for discount_product in Product.get_discount_products():
        kb = bot_utils.generate_add_to_cart_button(str(discount_product.id))
        bot.send_photo(
            message.chat.id,
            discount_product.image.read(),
            caption=discount_product.get_product_info(),
            reply_markup=kb
        )


@bot.message_handler(func=lambda c: bot_utils.check_message_match(c, 'cart'))
def show_products_in_cart(message):
    for product in User.show_products_in_cart(message.chat.id):
        bot.send_message(
            message.chat.id,
            product.title,
            reply_markup=bot_utils.generate_add_button(message.chat.id)
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
        for product in category.get_products():
            kb = bot_utils.generate_add_to_cart_button(str(product.id))
            bot.send_photo(
                call.message.chat.id,
                product.image.read(),
                caption=product.get_product_info(),
                reply_markup=kb
            )


@bot.callback_query_handler(func=lambda p: bot_utils.check_call_tag_match(p, ADD_TO_CART_TAG))
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
