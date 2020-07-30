
from app import *

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://new-project-265216.df.r.appspot.com/' + TOKEN)
    return "<h1>Advert Bot is Active!!</h1>", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


print("Running.....")
bot.remove_webhook()
bot.polling()