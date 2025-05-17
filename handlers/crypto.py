import aiohttp
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from services import user_store
from handlers.start import start


# Constants for callback data states
SHOW_MARKET = "show_market"
SHOW_FAVORITES = "show_favorites"
TOGGLE_FAVORITE_PREFIX = "toggle_fav_"  # followed by coin id
GO_BACK_TO_MAIN = "go_back_main"

# Example top-level keyboard with Market and Favorites buttons
TOP_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📈 Market", callback_data=SHOW_MARKET),
        InlineKeyboardButton("⭐ Favorites", callback_data=SHOW_FAVORITES),
    ],
])

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
VS_CURRENCY = "usd"
ORDER = "market_cap_desc"
PER_PAGE = 10
PAGE = 1

async def fetch_coins():
    """Fetch coin data from CoinGecko API."""
    params = {
        "vs_currency": VS_CURRENCY,
        "order": ORDER,
        "per_page": PER_PAGE,
        "page": PAGE,
        "sparkline": "false",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGECKO_API_URL, params=params) as resp:
            return await resp.json()

def build_coin_row(coin, is_fav):
    """Create a line for a coin with star for favorite."""
    star = "⭐" if is_fav else "☆"
    # Format the 24h price change with sign and color emoji
    change_24h = coin.get("price_change_percentage_24h", 0)
    change_str = f"{change_24h:+.2f}%"
    if change_24h > 0:
        change_str = f"📈 {change_str}"
    elif change_24h < 0:
        change_str = f"📉 {change_str}"
    else:
        change_str = f"{change_str}"
    
    return f"{star} {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:.2f} {change_str}"

def build_coins_keyboard(coins, favorites, current_tab=None):
    """Build inline keyboard with coins as single buttons with favorite toggling."""
    buttons = []

    # Coin rows
    for coin in coins:
        coin_id = coin['id']
        is_fav = coin_id in favorites
        star = "⭐" if is_fav else "☆"
        button_text = f"{star} {coin['symbol'].upper()} ${coin['current_price']:.2f}"
        buttons.append([
            InlineKeyboardButton(button_text, callback_data=f"{TOGGLE_FAVORITE_PREFIX}{coin_id}")
        ])

    # Top Market/Favorites buttons
    nav_buttons = [
        InlineKeyboardButton("📈 Market", callback_data=SHOW_MARKET),
        InlineKeyboardButton("⭐ Favorites", callback_data=SHOW_FAVORITES),
    ]

    # Back to main menu button
    buttons.append([
        InlineKeyboardButton("⬅️ Back to Main Menu", callback_data=GO_BACK_TO_MAIN)
    ])

    return InlineKeyboardMarkup([nav_buttons] + buttons)


def build_top_buttons(active_tab):
    """Build top Market/Favorites buttons, showing only the relevant tab switch button."""
    buttons = []

    if active_tab == "market":
        # On Market tab: show both options, highlight Market
        buttons.append(InlineKeyboardButton("📈 Market ✅", callback_data=SHOW_MARKET))
        buttons.append(InlineKeyboardButton("⭐ Favorites", callback_data=SHOW_FAVORITES))

    elif active_tab == "favorites":
        # On Favorites tab: show only return to Market
        buttons.append(InlineKeyboardButton("⬅️ Back to Market", callback_data=SHOW_MARKET))

    else:
        # Fallback: show both
        buttons.append(InlineKeyboardButton("📈 Market", callback_data=SHOW_MARKET))
        buttons.append(InlineKeyboardButton("⭐ Favorites", callback_data=SHOW_FAVORITES))

    return InlineKeyboardMarkup([buttons])


async def show_crypto_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, current_tab="market"):
    chat_id = update.effective_chat.id
    coins = await fetch_coins()
    user_data = user_store.get_user(chat_id) or {}
    favorites = set(user_data.get("favorites", []))

    if current_tab == "market":
        display_coins = coins
        header = "💰 Crypto Market:\n"
    else:
        # favorites tab
        display_coins = [coin for coin in coins if coin['id'] in favorites]
        header = "⭐ Your Favorite Coins:\n"

    if not display_coins:
        # Handle empty list for favorites or market
        text = "⭐ You have no favorite coins yet." if current_tab == "favorites" else "No coins found."
        keyboard = build_top_buttons(current_tab)
    else:
        lines = [build_coin_row(coin, coin['id'] in favorites) for coin in display_coins]
        text = header + "\n".join(lines)
        keyboard = build_coins_keyboard(display_coins, favorites, current_tab)

    if update.callback_query:
        # Check if new content or keyboard differs to avoid Telegram error
        message = update.callback_query.message
        if message.text == text and message.reply_markup == keyboard:
            await update.callback_query.answer()
        else:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text, reply_markup=keyboard)


async def handle_crypto_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data

    user_data = user_store.get_user(chat_id) or {}
    favorites = set(user_data.get("favorites", []))

    if data == SHOW_MARKET:
        await show_crypto_menu(update, context, current_tab="market")
        return

    if data == SHOW_FAVORITES:
        await show_crypto_menu(update, context, current_tab="favorites")
        return
    
    if data == GO_BACK_TO_MAIN:
        await start(update, context)
        return

    if data.startswith(TOGGLE_FAVORITE_PREFIX):
        coin_id = data[len(TOGGLE_FAVORITE_PREFIX):]
        if coin_id in favorites:
            favorites.remove(coin_id)
        else:
            favorites.add(coin_id)
        user_data['favorites'] = list(favorites)
        user_store.save_user(chat_id, user_data)
        # After toggle, stay in current tab (for simplicity, show market tab)
        current_tab = "market"
        await show_crypto_menu(update, context, current_tab=current_tab)
        return

    # Unknown callback data fallback
    await query.edit_message_text("⚠️ Unknown option.", reply_markup=build_top_buttons(current_tab))
