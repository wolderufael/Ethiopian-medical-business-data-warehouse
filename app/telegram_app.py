from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import datetime
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # here we call our super AI
    response = get_response(text)

    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

# the route here can be anything, you the one who will call it
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
    
@app.route('/')
def index():
    return '.'

# # Define a health check route
# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({'status': 'API is running', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,threaded=True)


