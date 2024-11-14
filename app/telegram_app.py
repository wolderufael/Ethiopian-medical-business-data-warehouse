# from flask import Flask, request, jsonify,render_template
# from flask_cors import CORS
# import asyncio
# import telegram
# # from telegram import Bot, ChatActions
# from telebot.credentials import bot_token, bot_user_name,URL
# from telebot.mastermind import get_response

# global bot
# global TOKEN
# TOKEN = bot_token
# bot = telegram.Bot(token=TOKEN)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# @app.route('/{}'.format(TOKEN), methods=['POST'])
# def respond():
#     # retrieve the message in JSON and then transform it to Telegram object
#     update = telegram.Update.de_json(request.get_json(force=True), bot)

#     # get the chat_id to be able to respond to the same user
#     chat_id = update.message.chat.id
#     # get the message id to be able to reply to this specific message
#     msg_id = update.message.message_id

#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     text = update.message.text.encode('utf-8').decode()
#     print("got text message :", text)

#     # here we call our super AI
#     response = get_response(text)

#     # now just send the message back
#     # notice how we specify the chat and the msg we reply to
#     bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

#     return 'ok'

# # the route here can be anything, you the one who will call it
# @app.route('/setwebhook', methods=['GET', 'POST'])
# def set_webhook():
#     # we use the bot object to link the bot to our app which live
#     # in the link provided by URL
#     s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
#     # something to let us know things work
#     if s:
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"
    
# @app.route('/')
# def index():
#     return '.'

# @app.route('/webhook_status', methods=['GET'])
# async def webhook_status():
#     try:
#         # Await the asynchronous get_webhook_info call
#         webhook_info = await bot.get_webhook_info()
        
#         # Return the webhook information as a JSON response
#         return jsonify(webhook_info.to_dict())
#     except Exception as e:
#         return jsonify({"error": str(e)})


# # Run Flask app
# if __name__ == '__main__':
#     app.run(threaded=True)
#     # app.run(host='0.0.0.0', port=5000,threaded=True)


# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import telegram
# import asyncio
# from telebot.credentials import bot_token, bot_user_name, URL
# from telebot.mastermind import get_response
# from threading import Thread
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Global bot initialization
# global bot
# global TOKEN
# TOKEN = bot_token
# bot = telegram.Bot(token=TOKEN)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Create a session with retry and connection pooling for Telegram API
# def create_session():
#     session = requests.Session()
#     retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
#     session.mount('https://', adapter)
#     return session

# # This session will be used in the bot for making HTTP requests
# session = create_session()

# @app.route('/{}'.format(TOKEN), methods=['POST'])
# def respond():
#     # retrieve the message in JSON and then transform it to Telegram object
#     update = telegram.Update.de_json(request.get_json(force=True), bot)

#     # get the chat_id to be able to respond to the same user
#     chat_id = update.message.chat.id
#     # get the message id to be able to reply to this specific message
#     msg_id = update.message.message_id

#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     text = update.message.text.encode('utf-8').decode()
#     print("got text message :", text)

#     # here we call our super AI
#     response = get_response(text)

#     # now just send the message back asynchronously
#     Thread(target=send_message, args=(chat_id, response, msg_id)).start()

#     return 'ok'

# def send_message(chat_id, text, msg_id):
#     try:
#         bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
#     except Exception as e:
#         print(f"Error sending message: {str(e)}")

# # the route here can be anything, you the one who will call it
# @app.route('/setwebhook', methods=['GET', 'POST'])
# def set_webhook():
#     # we use the bot object to link the bot to our app which live
#     # in the link provided by URL
#     s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
#     # something to let us know things work
#     if s:
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"
    
# @app.route('/')
# def index():
#     return '.'

# @app.route('/webhook_status', methods=['GET'])
# def webhook_status():
#     try:
#         # Run the async call using asyncio.run
#         webhook_info = asyncio.run(bot.get_webhook_info())
        
#         # Return the webhook information as a JSON response
#         return jsonify(webhook_info.to_dict())
#     except Exception as e:
#         return jsonify({"error": str(e)})


# # Run Flask app
# if __name__ == '__main__':
#     app.run(threaded=True, host='0.0.0.0', port=5000)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import telegram
import asyncio
from threading import Thread
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response

# Global bot initialization
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# Create a FastAPI instance
app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a session with retry and connection pooling for Telegram API
def create_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    session.mount('https://', adapter)
    return session

# This session will be used in the bot for making HTTP requests
session = create_session()

@app.post('/{TOKEN}')
async def respond(request: Request):
    # retrieve the message in JSON and then transform it to Telegram object
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # here we call our super AI
    response = get_response(text)

    # now just send the message back asynchronously
    Thread(target=send_message, args=(chat_id, response, msg_id)).start()

    return JSONResponse(content={"status": "ok"})

def send_message(chat_id, text, msg_id):
    try:
        bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
    except Exception as e:
        print(f"Error sending message: {str(e)}")

@app.get("/setwebhook")
async def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    # s = bot.setWebhook(f'{URL}{TOKEN}')
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return JSONResponse(content={"status": "webhook setup ok"})
    else:
        return JSONResponse(content={"status": "webhook setup failed"})

@app.get("/webhook_status")
async def webhook_status():
    try:
        # Run the async call using asyncio.run
        loop = asyncio.get_event_loop()
        webhook_info = await bot.get_webhook_info()
        
        # Return the webhook information as a JSON response
        return JSONResponse(content=webhook_info.to_dict())
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.get("/")
async def index():
    return "Bot is running!"

# Run FastAPI app using `uvicorn`
# uvicorn your_script_name:app --reload
