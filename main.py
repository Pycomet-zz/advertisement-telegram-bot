
from app import *
from resources import User

@app.route('/' + TOKEN, methods=['POST', 'GET'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "<h1>Advert Bot is Active!!</h1>", 200


api.add_resource(User, "/testapi")

if __name__ == "__main__":

    if DEBUG is False:
        app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    else:
        print("Running.....")
        bot.remove_webhook()
        bot.polling()