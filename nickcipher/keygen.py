import json
from nickcipher.config import KEYS_DIR

#Här bor funktion för att skapa en nyckel (JSON)

"""
NickCipher format

En nyckel består av:
	•	en seed
	•	en mapping där varje tillåtet tecken mappar till exakt 5 unika emojis
	•	ett separat set med exakt 5 unika separator-emojis

Vid kodning ersätts varje tecken med en emoji vald från dess mapping.
Mellan varje token infogas en emoji vald från separator-setet.

Vid avkodning ignoreras separator-emojis helt och övriga emojis mappas entydigt tillbaka.

Varje emoji i systemet måste tillhöra exakt EN kategori.
"""

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
 "n","o","p","q","r","s","t","u","v","w","x","y","z",
 "å","ä","ö"]
symbols = [".", ",","!"," "]

#Här bor emoji-nyckeln:
key_path = KEYS_DIR / "keys.json"

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
    
    print(len(emoji_pool))

    if len(emoji_pool) != 200:
        raise ValueError("Emoji file must contain exactly 200 emojis")

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

        if value <= 1:
            raise ValueError(f"Weight for '{char}' must be greater than one")

    return weights
   