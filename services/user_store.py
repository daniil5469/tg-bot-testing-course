import json
import os

DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")


def _load_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_user(chat_id: int, profile: dict):
    data = _load_data()
    data[str(chat_id)] = profile
    _save_data(data)


def get_user(chat_id: int):
    data = _load_data()
    return data.get(str(chat_id))


def delete_user_profile(user_id: int) -> bool:
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    user_key = str(user_id)
    if user_key in data:
        del data[user_key]
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True

    return False


# -- Favorites management ---

def get_favorites(user_id: int) -> list:
    """
    Returns the list of favorite coin IDs for the user,
    or empty list if none stored.
    """
    data = _load_data()
    user_data = data.get(str(user_id), {})
    return user_data.get("favorites", [])


def add_favorite(chat_id: int, coin_id: str):
    profile = get_user(chat_id) or {}
    favs = set(profile.get("favorites", []))
    favs.add(coin_id)
    profile["favorites"] = list(favs)
    save_user(chat_id, profile)


def remove_favorite(chat_id: int, coin_id: str):
    profile = get_user(chat_id) or {}
    favs = set(profile.get("favorites", []))
    favs.discard(coin_id)
    profile["favorites"] = list(favs)
    save_user(chat_id, profile)
