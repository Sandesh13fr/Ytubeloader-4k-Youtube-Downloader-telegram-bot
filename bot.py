import os
import subprocess
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Define the command to download videos
DOWNLOAD_SCRIPT = "src/multiYT.sh"
AUDIO_SCRIPT = "src/multiYT_A.sh"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a YouTube link to download the video or audio.",
        reply_markup=ForceReply(selective=True),
    )

def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    with open("queue.txt", "w") as f:
        f.write(url + "\n")
    subprocess.Popen([DOWNLOAD_SCRIPT, "queue.txt"])
    update.message.reply_text("Downloading video...")

def download_audio(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    with open("queue.txt", "w") as f:
        f.write(url + "\n")
    subprocess.Popen([AUDIO_SCRIPT, "queue.txt"])
    update.message.reply_text("Downloading audio...")

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, download_video))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, download_audio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()