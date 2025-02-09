from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json
from flask import Flask, jsonify

# Initialize Flask app for the server
app = Flask(__name__)

# Initialize the global variable to hold JSON data
json_data = {}

@app.route('/')
def index():
    return jsonify(json_data)

@app.route('/update_json', methods=['POST'])
def update_json():
    return jsonify({"message": "Data updated successfully!"})

async def format_text(update: Update, context: CallbackContext):
    global json_data
    # Get the text from the user's message
    message = update.message.text
    result = {}

    # Split the message into lines
    lines = message.splitlines()

    # Process each line
    for line in lines:
        parts = line.split(" - ")
        if len(parts) == 2:
            result[parts[0]] = parts[1]

    # Update global json_data variable and ensure it is available through the API
    json_data = result

    # Print the result as JSON format in terminal
    print(json.dumps(result, indent=4))

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot started! Send text in the format 'ID - Phone' to get the output.")

def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = Application.builder().token('6361809314:AAHsd3UMiO7nS_TJMSJhzSS4F3GSBtHkUPo').build()

    # Register the handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))

    # Run the Flask server in the background
    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=5000)
    
    thread = Thread(target=run_flask)
    thread.daemon = True
    thread.start()

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
