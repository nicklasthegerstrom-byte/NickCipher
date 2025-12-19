from nickcipher.keygen import load_keys
from config import KEYS_DIR

key_path = KEYS_DIR / "keys.json"

keys = load_keys(key_path)
print(keys.keys())

for char, emojis in keys.items():
    print(char, "→", emojis)