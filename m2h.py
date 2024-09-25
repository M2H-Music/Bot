import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

loop = asyncio.get_event_loop()

# Token and Database Configurations
TOKEN = 'your-telegram-bot-token'
MONGO_URI = 'your-mongo-uri'
FORWARD_CHANNEL_ID = -1001970210072
CHANNEL_ID = -1001970210072
error_channel_id = -1001970210072

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['zoya']
users_collection = db.users

bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

running_processes = []

REMOTE_HOST = '4.213.71.147'

# Bot commands and message handling
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    
    btn1 = KeyboardButton("Subscribe to Instant Plan 😇")
    btn2 = KeyboardButton("Subscribe to Instant++ Plan 😇😇")
    btn3 = KeyboardButton("Download Canary Version ✅")
    btn4 = KeyboardButton("View My Account Details🏦")
    btn5 = KeyboardButton("Get Assistance❓")
    btn6 = KeyboardButton("Contact Support✔️")
    btn7 = KeyboardButton("Bot Owner: @m2hgamerz")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    
    bot.send_message(message.chat.id, "Welcome to the system! Please select one of the options below to continue:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Subscribe to Instant Plan 😇":
        bot.reply_to(message, "You have successfully subscribed to the *Instant Plan*. Enjoy the benefits!", parse_mode='Markdown')
    elif message.text == "Subscribe to Instant++ Plan 😇😇":
        bot.reply_to(message, "You have successfully subscribed to the *Instant++ Plan*. The premium features are now available!", parse_mode='Markdown')
        # You can call the attack command here if needed
    elif message.text == "Download Canary Version ✅":
        bot.send_message(message.chat.id, "Click the following link to download the Canary version:\nhttps://t.me/c/1970210072/488", parse_mode='Markdown')
    elif message.text == "View My Account Details🏦":
        user_id = message.from_user.id
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            username = message.from_user.username
            plan = user_data.get('plan', 'N/A')
            valid_until = user_data.get('valid_until', 'N/A')
            current_time = datetime.now().isoformat()
            response = (f"*Account Information:*\n"
                        f"Username: {username}\n"
                        f"Subscription Plan: {plan}\n"
                        f"Valid Until: {valid_until}\n"
                        f"Current Time: {current_time}")
        else:
            response = "We couldn't find your account details. Please contact support for assistance."
        bot.reply_to(message, response, parse_mode='Markdown')
    elif message.text == "Get Assistance❓":
        help_text = """
Here is an explanation of the available commands:

1. **Subscribe to Instant Plan 😇**: This option allows you to subscribe to the Instant Plan, giving you access to basic features of the bot.
2. **Subscribe to Instant++ Plan 😇😇**: This plan provides you with advanced features, unlocking premium functionalities within the bot.
3. **Download Canary Version ✅**: Use this command to download the Canary Version of the system. It provides early access to new features.
4. **View My Account Details🏦**: Displays your current subscription status, the plan you're enrolled in, and other account details.
5. **Get Assistance❓**: You are here! This option gives you a brief overview of the available commands.
6. **Contact Support✔️**: If you need further help, you can contact the support team directly for any assistance or queries.
7. **Bot Owner: @m2hgamerz**: Learn more about the bot owner, M2H, and contact him for further information.
        """
        bot.reply_to(message, help_text, parse_mode='Markdown')
    elif message.text == "Contact Support✔️":
        bot.reply_to(message, "You can contact our support team directly by messaging @admin_username.", parse_mode='Markdown')
    elif message.text == "Bot Owner: @m2hgamerz":
        bot.reply_to(message, "This bot is managed by M2H (@m2hgamerz). For any queries or concerns, feel free to reach out.", parse_mode='Markdown')
    else:
        bot.reply_to(message, "Sorry, the option you selected is not valid. Please use the menu to choose a valid action.", parse_mode='Markdown')

# Function to start asyncio loop in a separate thread
def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

# Running the bot
if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Bot is now running...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Error occurred during polling: {e}")
        time.sleep(REQUEST_INTERVAL)
