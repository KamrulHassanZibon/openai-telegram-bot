import telegram
from telegram.ext import Updater, MessageHandler, Filters
import time
import openai
import os

bot = telegram.Bot(token='BOT_TOKEN')
openai.api_key = 'OPENAI_API'

# Define the filtered text
filtered_text = '/start'

#time limiteing of API USE
last_request_time = 0

def respond_to_message(update, context):
    global last_request_time

    # Get the text of the message sent to the bot
    message_text = update.message.text

      # Check if the message contains the filtered text
    if filtered_text in message_text:
        bot.send_message(chat_id=update.message.chat_id, text="This word is not allowed.")
        return

    # Limit the API usage by introducing a delay between requests
    now = time.time()
    if now - last_request_time < 1:
        time.sleep(1 - (now - last_request_time))
    last_request_time = time.time()

    # Send the message text to the OpenAI API
    response = openai.Completion.create(
        engine='text-curie-001',
        prompt=message_text,
        max_tokens=100
    )

    # Send the response back to the user
    bot.send_message(chat_id=update.message.chat_id, text=response.choices[0].text)

# Set up the Telegram bot to listen for messages
updater = Updater(token='OPENAI_API')
updater.dispatcher.add_handler(MessageHandler(Filters.text, respond_to_message))
updater.start_polling()
updater.idle()
