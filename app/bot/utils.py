import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .config import CATEGORY_TAG, ADD_TO_CART_TAG, ADD_TAG, DEL_TAG
from .keyboards import START_KB
from .texts import ADD_TO_CART, ADD_PRODUCT, DEL_PRODUCT


def check_message_match(message, text: str):
    return message.text == START_KB[text]


def check_call_tag_match(call, tag: str):
    return json.loads(call.data)['tag'] == tag


def get_callback_data(id_: str, tag: str):
    return json.dumps(
        {
            'id': id_,
            'tag': tag
        }
    )


def generate_categories_kb(categories_qs):
    buttons = []
    kb = InlineKeyboardMarkup()
    for c in categories_qs:
        data = get_callback_data(str(c.id), CATEGORY_TAG)
        buttons.append(InlineKeyboardButton(c.title, callback_data=data))
    kb.add(*buttons)
    return kb


def generate_add_to_cart_button(id_: str):
    kb = InlineKeyboardMarkup()
    data = get_callback_data(id_, ADD_TO_CART_TAG)
    button = InlineKeyboardButton(ADD_TO_CART, callback_data=data)
    kb.add(button)
    return kb


def generate_add_button(id_: str):
    kb = InlineKeyboardMarkup()
    add_data = get_callback_data(id_, ADD_TAG)
    add_button = InlineKeyboardButton(ADD_PRODUCT, callback_data=add_data)
    del_data = get_callback_data(id_, DEL_TAG)
    del_button = InlineKeyboardButton(DEL_PRODUCT, callback_data=del_data)
    kb.add(add_button, del_button)
    return kb

# def generate_discount_products_kb(discount_products_qs):
#     buttons = []
#     kb = InlineKeyboardMarkup()
#     for dp in discount_products_qs:
#         data = json.dumps(
#             {
#                 'id': str(dp.id)
#             }
#         )
#         buttons.append(InlineKeyboardButton(dp.title, callback_data=data))
#     kb.add(*buttons)
#     return kb

