import re
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from src.services import user_store
from src.handlers import crypto
from src.handlers.start import MAIN_MENU_INLINE

# Conversation states
NICKNAME, EMAIL, DOB, LOCATION = range(4)

# Back button
BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("Back to Main Menu", callback_data="back_to_menu")]
])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat.id

    if data == "create_profile":
        await query.edit_message_text("Please enter your nickname (no spaces):")
        return NICKNAME

    elif data == "view_profile":
        profile = user_store.get_user(chat_id)
        msg = (
            f"Your Profile:\n"
            f"Nickname: {profile.get('nickname')}\n"
            f"Email: {profile.get('email')}\n"
            f"Date of Birth: {profile.get('dob')}\n"
            f"Location: {profile.get('location')}"
        ) if profile else "Profile not found. Use Create Profile to create one."
        await query.edit_message_text(msg, reply_markup=BACK_BUTTON)
        return ConversationHandler.END

    elif data == "delete_profile":
        success = user_store.delete_user_profile(chat_id)
        text = "Your profile has been deleted successfully." if success else "No profile found to delete."
        await query.edit_message_text(text, reply_markup=BACK_BUTTON)
        return ConversationHandler.END

    elif data == "help":
        await query.edit_message_text(
            "Available Commands:\n/start – Show main menu\n/view_profile – View your profile\n/delete_profile – Delete your profile",
            reply_markup=BACK_BUTTON
        )
        return ConversationHandler.END
    
    elif data == "crypto_menu":
        # Call the crypto menu show function here
        # We pass the original callback_query update for message editing
        await crypto.show_crypto_menu(update, context)
        return ConversationHandler.END

    elif data == "back_to_menu":
        await query.edit_message_text("Welcome back! Please choose an option:", reply_markup=MAIN_MENU_INLINE)
        return ConversationHandler.END

    await query.edit_message_text("Unknown option selected.", reply_markup=BACK_BUTTON)
    return ConversationHandler.END

# Nickname validation: No spaces, letters/numbers/underscore
async def get_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nickname = update.message.text.strip()
    if not re.fullmatch(r"^\w+$", nickname):
        await update.message.reply_text("Invalid nickname. Use only letters, numbers, or underscores. No spaces.\nTry again:")
        return NICKNAME
    context.user_data["nickname"] = nickname
    await update.message.reply_text("Please enter your email address:")
    return EMAIL

# Email validation
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        await update.message.reply_text("Invalid email format. Please enter a valid email address:")
        return EMAIL
    context.user_data["email"] = email
    await update.message.reply_text("Please enter your date of birth")
    return DOB

# Date of Birth: accept multiple formats and convert to ISO format
async def get_dob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_dob = update.message.text.strip()
    accepted_formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y"]

    for fmt in accepted_formats:
        try:
            dob = datetime.strptime(input_dob, fmt).strftime("%Y-%m-%d")
            context.user_data["dob"] = dob
            await update.message.reply_text("Please enter your location:")
            return LOCATION
        except ValueError:
            continue

    await update.message.reply_text("Invalid date format. Try one of these: MM/DD/YYYY")
    return DOB

# Location: Basic non-empty string validation
async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text.strip()
    if not location or len(location) < 2:
        await update.message.reply_text("Invalid location. Please enter a valid location name:")
        return LOCATION

    context.user_data["location"] = location
    chat_id = update.effective_chat.id
    user_store.save_user(chat_id, context.user_data)

    await update.message.reply_text("Profile created successfully!", reply_markup=MAIN_MENU_INLINE)
    return ConversationHandler.END

async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("view_profile handler triggered")
    chat_id = update.effective_chat.id
    profile = user_store.get_user(chat_id)
    msg = (
        f"Your Profile:\n"
        f"Nickname: {profile.get('nickname')}\n"
        f"Email: {profile.get('email')}\n"
        f"Date of Birth: {profile.get('dob')}\n"
        f"Location: {profile.get('location')}"
    ) if profile else "Profile not found. Use /start to create one."
    await update.message.reply_text(msg)

async def delete_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    success = user_store.delete_user_profile(chat_id)
    msg = "Your profile has been deleted." if success else "No profile found to delete."
    await update.message.reply_text(msg, reply_markup=MAIN_MENU_INLINE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available Commands:\n"
        "/start – Show main menu\n"
        "/view_profile – View your profile\n"
        "/delete_profile – Delete your profile"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Profile creation cancelled.", reply_markup=MAIN_MENU_INLINE)
    return ConversationHandler.END

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unknown command. Use /start to see available options.")
