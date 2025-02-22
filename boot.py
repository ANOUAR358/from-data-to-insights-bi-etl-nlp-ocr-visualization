import logging
import os
from datetime import datetime  # Import to add timestamp
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
TOKEN = '7812133141:AAEqs6ncM_oBYgegx2IvAP5vDuZDP2KWIVc'  # Replace with your actual bot token

# Directory to save media files
MEDIA_DIR = r"C:\Users\dell\Desktop\BI_prototype\data"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Function to download and save files
async def download_file(file_id: str, context: CallbackContext, file_name: str, extension: str):
    """Download a file from Telegram and save it to the media directory."""
    try:
        # Add timestamp to make the filename unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_file_name = f"{file_name}_{timestamp}{extension}"

        file = await context.bot.get_file(file_id)
        file_path = os.path.join(MEDIA_DIR, unique_file_name)
        await file.download_to_drive(file_path)
        logger.info(f"Downloaded file: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
        return None

# Command to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me an image, audio, video, or PDF, and I will save it.")

# Handler to receive text messages
async def receive_text(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Text message from {user.id}: {text}")
    await update.message.reply_text("Got your text message!")

# Handler to receive images
async def receive_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1]  # Get the highest resolution photo
    file_path = await download_file(photo.file_id, context, f"{user.id}_image", ".jpg")
    if file_path:
        await update.message.reply_text("Image received and saved successfully!")

# Handler to receive audio
async def receive_audio(update: Update, context: CallbackContext):
    user = update.message.from_user
    audio = update.message.audio or update.message.voice  # Handle both audio and voice messages
    extension = ".ogg" if update.message.voice else ".mp3"
    file_path = await download_file(audio.file_id, context, f"{user.id}_audio", extension)
    if file_path:
        await update.message.reply_text("Audio received and saved successfully!")

# Handler to receive video
async def receive_video(update: Update, context: CallbackContext):
    user = update.message.from_user
    video = update.message.video
    file_path = await download_file(video.file_id, context, f"{user.id}_video", ".mp4")
    if file_path:
        await update.message.reply_text("Video received and saved successfully!")

# Handler to receive PDF files
async def receive_pdf(update: Update, context: CallbackContext):
    user = update.message.from_user
    document = update.message.document
    if document.mime_type == 'application/pdf':  # Ensure the file is a PDF
        file_path = await download_file(document.file_id, context, f"{user.id}_document", ".pdf")
        if file_path:
            await update.message.reply_text("PDF received and saved successfully!")
    else:
        await update.message.reply_text("This is not a PDF file. Please send a valid PDF.")

# Error handler
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f'Update {update} caused error {context.error}')

# Main function to set up the bot and handlers
def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # Message handlers for different types of messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))  # Handle text messages
    app.add_handler(MessageHandler(filters.PHOTO, receive_image))                   # Handle photos
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, receive_audio))   # Handle audio and voice
    app.add_handler(MessageHandler(filters.VIDEO, receive_video))                   # Handle videos
    app.add_handler(MessageHandler(filters.Document.PDF, receive_pdf))              # Handle PDF files

    # Error handler
    app.add_error_handler(error_handler)

    # Start polling
    app.run_polling()

if __name__ == '__main__':
    main()
