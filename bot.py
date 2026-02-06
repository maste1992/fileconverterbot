import os
import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

import utils
import converters

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# State management for file processing
# In a real-world high-traffic bot, you'd use a database or Redis
user_files = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message and instructions."""
    await update.message.reply_text(
        "👋 Welcome to the File Converter Bot!\n\n"
        "I can help you convert files between different formats.\n\n"
        "**Supported Conversions:**\n"
        "📄 PDF to Word\n"
        "📝 Word to PDF\n"
        "🖼️ Image (JPG/PNG) to PDF\n\n"
        "To get started, simply **upload a file** you want to convert!"
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles uploaded documents (PDF, DOCX)."""
    document = update.message.document
    file_name = document.file_name
    file_ext = os.path.splitext(file_name)[1].lower()
    
    keyboard = []
    
    if file_ext == '.pdf':
        keyboard = [
            [InlineKeyboardButton("📄 PDF to Word 📝", callback_data='pdf_to_docx')],
            [InlineKeyboardButton("🖼️ PDF to Image (PNG) 🖼️", callback_data='pdf_to_image')]
        ]
    elif file_ext in ['.docx', '.doc']:
        keyboard = [
            [InlineKeyboardButton("📝 Word to PDF 📄", callback_data='docx_to_pdf')],
            [InlineKeyboardButton("📊 Word to Excel 📈", callback_data='docx_to_excel')],
            [InlineKeyboardButton("🖼️ Word to Image 🖼️", callback_data='docx_to_image')]
        ]
    elif file_ext in ['.xlsx', '.xls']:
        keyboard = [
            [InlineKeyboardButton("📈 Excel to PDF 📄", callback_data='excel_to_pdf')],
            [InlineKeyboardButton("📝 Excel to Word 📝", callback_data='excel_to_word')]
        ]
    elif file_ext in ['.png', '.jpg', '.jpeg']:
        keyboard = [
            [InlineKeyboardButton("🖼️ Image to PDF 📄", callback_data='image_to_pdf')],
            [InlineKeyboardButton("📝 Image to Word 📝", callback_data='image_to_word')],
            [InlineKeyboardButton("📊 Image to Excel 📉", callback_data='image_to_excel')]
        ]
    else:
        await update.message.reply_text(f"❌ Unsupported format ({file_ext}). Try PDF, Word, Excel, or Image.")
        return

    # Download file
    sent_message = await update.message.reply_text("⏳ Downloading file...")
    file = await context.bot.get_file(document.file_id)
    input_path = utils.get_temp_path(file_ext.strip('.'))
    await file.download_to_drive(input_path)
    
    # Store path for later
    user_files[update.effective_user.id] = {
        'input_path': input_path,
        'file_name': file_name,
        'message_id': sent_message.message_id
    }
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await sent_message.edit_text(f"✅ File '{file_name}' received! Choose conversion type:", reply_markup=reply_markup)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles uploaded photos."""
    photo = update.message.photo[-1] # Get highest resolution
    
    sent_message = await update.message.reply_text("⏳ Downloading image...")
    file = await context.bot.get_file(photo.file_id)
    input_path = utils.get_temp_path('jpg')
    await file.download_to_drive(input_path)
    
    user_files[update.effective_user.id] = {
        'input_path': input_path,
        'file_name': 'image.jpg',
        'message_id': sent_message.message_id
    }
    
    keyboard = [
        [InlineKeyboardButton("🖼️ Image to PDF 📄", callback_data='image_to_pdf')],
        [InlineKeyboardButton("📝 Image to Word 📝", callback_data='image_to_word')],
        [InlineKeyboardButton("📊 Image to Excel 📉", callback_data='image_to_excel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await sent_message.edit_text("✅ Image received! Choose conversion type:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if user_id not in user_files:
        await query.edit_message_text("❌ No active file found. Please upload the file again.")
        return
    
    file_data = user_files[user_id]
    input_path = file_data['input_path']
    action = query.data
    
    output_path = None
    success = False
    
    await query.edit_message_text("⚙️ Converting file... Please wait.")
    
    if action == 'pdf_to_docx':
        output_ext = 'docx'
        success = converters.pdf_to_docx(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'pdf_to_image':
        output_ext = 'png'
        success = converters.pdf_to_image(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'docx_to_pdf':
        output_ext = 'pdf'
        success = converters.docx_to_pdf(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'docx_to_excel':
        output_ext = 'xlsx'
        success = converters.docx_to_excel(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'docx_to_image':
        output_ext = 'png'
        success = converters.docx_to_image(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'excel_to_pdf':
        output_ext = 'pdf'
        success = converters.excel_to_pdf(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'excel_to_word':
        output_ext = 'docx'
        success = converters.excel_to_word(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'image_to_pdf':
        output_ext = 'pdf'
        success = converters.image_to_pdf(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'image_to_word':
        output_ext = 'docx'
        success = converters.image_to_word(input_path, output_path := utils.get_temp_path(output_ext))
    elif action == 'image_to_excel':
        output_ext = 'xlsx'
        success = converters.image_to_excel(input_path, output_path := utils.get_temp_path(output_ext))
    
    if success:
        await query.edit_message_text("📤 Conversion complete! Sending file...")
        try:
            # Construct original filename with new extension
            orig_base = os.path.splitext(file_data['file_name'])[0]
            final_filename = f"{orig_base}.{output_ext}"
            
            with open(output_path, 'rb') as f:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=f,
                    filename=final_filename
                )
            await query.delete_message()
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            await query.edit_message_text("❌ Error sending converted file.")
    else:
        await query.edit_message_text("❌ Conversion failed. Please try again later or check the file.")
    
    # Cleanup
    utils.cleanup_files(input_path, output_path)
    del user_files[user_id]

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(f"Exception while handling an update: {context.error}")
    # We don't want to crash on network errors
    if isinstance(context.error, (httpx.ReadError, httpx.NetworkError)):
        logger.warning("Network/Read error occurred. The bot will automatically retry.")
        return

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment.")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    doc_handler = MessageHandler(filters.Document.ALL, handle_document)
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    callback_handler = CallbackQueryHandler(handle_callback)
    
    application.add_handler(start_handler)
    application.add_handler(doc_handler)
    application.add_handler(photo_handler)
    application.add_handler(callback_handler)
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("Bot started...")
    application.run_polling()
