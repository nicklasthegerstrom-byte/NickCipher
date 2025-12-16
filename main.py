from nickcipher.keygen import load_keys
from config import KEYS_DIR
from nickcipher.cipher import Emojicipher

key_path = KEYS_DIR / "keys.json"

keys = load_keys(key_path)

original_text = "Hej Susanna vad roligt det är att jobba hela kvällen lång"
cipher = Emojicipher(keys, 200)

results = cipher.encode(original_text)

print("Okodad text:")
print(original_text)
print("Kodad text:")
print(results)
