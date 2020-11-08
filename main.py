from app.api.routers import app_flask
from app.bot.config import WEBHOOK_URL
from flask import Flask, request, abort
from telebot.types import Update
from app.bot.bot import bot

# bot.remove_webhook()
# bot.polling()

app = Flask(__name__)


@app.route('/tg/webhook/', methods=['GET', 'POST'])
def handle_webhook():
    if request.content_type == 'application/json':
        data_string = request.get_data().decode('utf-8')
        update = Update.de_json(data_string)
        bot.process_new_updates([update])
        return 'OK'
    else:
        return abort(403)


if __name__ == '__main__':

    app_flask.run(host='127.0.0.1', port=27018, debug=True)

    from time import sleep

    bot.remove_webhook()
    sleep(1)
    bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=open('webhook_cert.pem', 'r')
    )
    app.run(host='127.0.0.1', port=8000, debug=True)
