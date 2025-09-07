from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

# Main menu buttons
MAIN_MENU_INLINE = InlineKeyboardMarkup([
    [InlineKeyboardButton("Create Profile", callback_data="create_profile")],
    [InlineKeyboardButton("View Profile", callback_data="view_profile")],
    [InlineKeyboardButton("Crypto", callback_data="crypto_menu")],
    [InlineKeyboardButton("Delete Profile", callback_data="delete_profile")],
    [InlineKeyboardButton("Help", callback_data="help")],
])

# Start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    greeting = f"Hello, {user.first_name or 'User'}! Welcome to Testronaut Bot.\n\n" \
               "Choose an option to get started:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(greeting, reply_markup=MAIN_MENU_INLINE)
    else:
        await update.message.reply_text(greeting, reply_markup=MAIN_MENU_INLINE)

    logger.info(f"Sent greeting to user {user.id}: {greeting}")
