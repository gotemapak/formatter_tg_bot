import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
PLATFORM_CHOICE, TEXT_INPUT = range(2)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user to choose platform."""
    keyboard = [
        [
            InlineKeyboardButton("Telegram", callback_data='telegram'),
            InlineKeyboardButton("LinkedIn", callback_data='linkedin')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to the Text Formatter Bot! 📝\n"
        "Which platform do you want to format text for?",
        reply_markup=reply_markup
    )
    return PLATFORM_CHOICE

async def platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle platform choice and ask for text input."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['platform'] = query.data
    await query.edit_message_text(
        f"You selected {query.data.capitalize()}. Please send the text you want to format."
    )
    return TEXT_INPUT

def format_for_telegram(text: str) -> str:
    """Format text for Telegram using Markdown."""
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    list_counter = 0  # Counter for numbered lists
    
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle headings (lines that are capitalized or start with capital letters)
            if (len(line) > 0 and (
                all(c.isupper() for c in line if c.isalpha()) or  # All caps
                (line[0].isupper() and len(line.split()) <= 5)    # Short phrase starting with capital
            )):
                line = f"**{line}**"  # Bold for headings
            
            # Handle numbered lists
            elif line.strip().replace('.', '').strip().isdigit():
                list_counter += 1
                line = f"{list_counter}. {'.'.join(line.split('.')[1:]).strip()}"
            
            # Handle bullet points
            elif line.startswith('•') or line.startswith('-'):
                line = f"• {line.lstrip('•').lstrip('-').strip()}"
            
            # Handle links - keep them as plain text
            elif 'http' in line or 't.me' in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word.startswith(('http', 't.me')):
                        # Keep the link as plain text
                        words[i] = word
                line = ' '.join(words)
            
            # Handle dashes
            line = line.replace('—', '-')
            
            formatted_lines.append(line)
        
        # Reset list counter between paragraphs
        if formatted_lines and not any(l.strip().replace('.', '').strip().isdigit() for l in formatted_lines):
            list_counter = 0
            
        formatted_paragraphs.append('\n'.join(formatted_lines))
    
    return '\n\n'.join(formatted_paragraphs)

def format_for_linkedin(text: str) -> str:
    """Format text for LinkedIn."""
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    list_counter = 0  # Counter for numbered lists
    
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Handle headings (lines that are capitalized or start with capital letters)
            if (len(line) > 0 and (
                all(c.isupper() for c in line if c.isalpha()) or  # All caps
                (line[0].isupper() and len(line.split()) <= 5)    # Short phrase starting with capital
            )):
                line = line.upper()  # Keep headings in uppercase
            
            # Handle numbered lists
            elif line.strip().replace('.', '').strip().isdigit():
                list_counter += 1
                line = f"{list_counter}. {'.'.join(line.split('.')[1:]).strip()}"
            
            # Handle bullet points
            elif line.startswith('•') or line.startswith('-'):
                line = f"• {line.lstrip('•').lstrip('-').strip()}"
            
            # Handle links - keep them as plain text
            elif 'http' in line or 't.me' in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word.startswith(('http', 't.me')):
                        # Keep the link as plain text
                        words[i] = word
                line = ' '.join(words)
            
            # Handle dashes
            line = line.replace('—', '-')
            
            formatted_lines.append(line)
        
        # Reset list counter between paragraphs
        if formatted_lines and not any(l.strip().replace('.', '').strip().isdigit() for l in formatted_lines):
            list_counter = 0
            
        formatted_paragraphs.append('\n'.join(formatted_lines))
    
    return '\n\n'.join(formatted_paragraphs)

async def format_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Format the received text according to chosen platform."""
    platform = context.user_data.get('platform')
    text = update.message.text
    
    if platform == 'telegram':
        formatted_text = format_for_telegram(text)
    else:  # linkedin
        formatted_text = format_for_linkedin(text)
    
    # Send only the formatted text without additional messages
    await update.message.reply_text(formatted_text)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "Operation cancelled. Use /format to start again."
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('format', start)
        ],
        states={
            PLATFORM_CHOICE: [
                CallbackQueryHandler(platform_choice)
            ],
            TEXT_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, format_text)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    
    # Start the bot with drop_pending_updates=True to clear any pending updates
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main() 