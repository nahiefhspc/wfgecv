from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json
from flask import Flask, jsonify, request
from threading import Thread

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
    message = update.message.text.strip()

    # Try to parse the message as JSON
    try:
        # If it's valid JSON, update the global json_data with the parsed content
        parsed_json = json.loads(message)
        if isinstance(parsed_json, dict):  # Make sure it's a dictionary
            json_data = parsed_json
            print(json.dumps(json_data, indent=4))  # Print JSON data in terminal
            await update.message.reply_text("JSON data updated successfully!")
        else:
            await update.message.reply_text("Please send valid JSON format.")
    except json.JSONDecodeError:
        # If the message is not valid JSON, handle it as a non-JSON formatted message
        await update.message.reply_text("Invalid JSON format. Please send a valid JSON.")
    
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot started! Send JSON data to update.")

def run_flask():
    """Run the Flask server in the background."""
    app.run(host="0.0.0.0", port=5000)

def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = Application.builder().token('6361809314:AAHsd3UMiO7nS_TJMSJhzSS4F3GSBtHkUPo').build()

    # Register the handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))

    # Run the Flask server in the background
    thread = Thread(target=run_flask)
    thread.daemon = True
    thread.start()

    # Start the Telegram bot
    application.run_polling()

if __name__ == "__main__":
    main()
