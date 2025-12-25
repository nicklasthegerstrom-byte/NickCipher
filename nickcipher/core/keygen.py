import json
from nickcipher.config import KEYS_DIR


def find_duplicate_emojis(key_dict: dict) -> list[str]:
    seen = set()
    duplicates = []

    for char, emojis in key_dict.items():
        for emoji in emojis:
            if emoji in seen:
                duplicates.append(emoji)
            else:
                seen.add(emoji)

    return duplicates

def load_keys(key_path):

    with open(key_path, "r", encoding="utf-8") as f:
        key_dict = json.load(f)

    return key_dict


def load_emojis(emoji_path):
    try:
        with open(emoji_path, "r", encoding="utf-8") as f:
            emoji_pool = json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError("Emoji file not found") from e

    except json.JSONDecodeError as e:
        raise ValueError("Emoji file is not valid JSON") from e

    if not isinstance(emoji_pool, list):
        raise ValueError("Emoji file must contain a list")

    if len(emoji_pool) < 200:
        raise ValueError("Emoji file must contain more than 200 emojis")

    return emoji_pool
        

def load_weights(weights_path):
    try:
        with open(weights_path, "r", encoding="utf-8") as f:
            weights = json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError("Weights file not found") from e

    except json.JSONDecodeError as e:
        raise ValueError("Weights file is not valid JSON") from e

    if not isinstance(weights, dict):
        raise ValueError("Weights file must contain a dictionary")

    for char, value in weights.items():
        if not isinstance(char, str):
            raise ValueError("All weight keys must be strings")

        if not isinstance(value, int):
            raise ValueError(f"Weight for '{char}' must be an integer")

        if value < 1:
            raise ValueError(f"Weight for '{char}' must be greater than one")

    return weights
   
