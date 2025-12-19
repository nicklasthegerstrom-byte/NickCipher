import random
import json
from config import KEYS_DIR, BASE_DIR

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

import json


def load_emojis(emoji_path):
    try:
        with open(emoji_path, "r", encoding="utf-8") as f:
            emoji_pool = json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError("Emoji-fil hittades inte") from e

    except json.JSONDecodeError as e:
        raise ValueError("Emoji-filen är inte giltig JSON") from e

    if not isinstance(emoji_pool, list):
        raise ValueError("Emoji-filen måste innehålla en lista")

    if len(emoji_pool) != 200:
        raise ValueError("Emoji-filen måste innehålla exakt 200 emojis")

    return emoji_pool
        

    

def load_weighted(weights):
    with open(weights, "r", encoding="utf-8") as f:
        weights = json.load(f)

    return weights
   