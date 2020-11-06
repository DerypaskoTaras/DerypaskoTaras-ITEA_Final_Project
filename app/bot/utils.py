import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .config import CATEGORY_TAG, ADD_TO_CART_TAG, COMPLETE_ORDER_TAG, DELETE_ORDER_TAG
from .keyboards import START_KB
from .texts import ADD_TO_CART, PAY_THE_ORDER, DELETE_ORDER
import datetime


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


def generate_complete_or_delete_order_kb(id_: str):
    kb = InlineKeyboardMarkup()
    delete_data = get_callback_data(id_, DELETE_ORDER_TAG)
    delete_button = InlineKeyboardButton(DELETE_ORDER, callback_data=delete_data)
    complete_data = get_callback_data(id_, COMPLETE_ORDER_TAG)
    complete_button = InlineKeyboardButton(PAY_THE_ORDER, callback_data=complete_data)
    kb.add(delete_button, complete_button)
    return kb


def get_date():
    date = datetime.datetime.now()
    return date