from nickcipher.keygen import load_emojis, load_weights
from nickcipher.config import BASE_DIR
from nickcipher.cipher import DynamicEmojiCipher

emoji_path = BASE_DIR / "emoji_pool.json"

weights_path = BASE_DIR / "char_weight.json"

emoji_pool = load_emojis(emoji_path)
weights = load_weights(weights_path)


cipher = DynamicEmojiCipher(emoji_pool, weights, 123456)
cipher.generate_key()

text = "Hej här är text som jag bara vill testa för att se om kryptering funkar"

encoded_text = cipher.encode(text.lower())

print("Orginal text:")
print(text)
print("Krypterad text:")
print(encoded_text)
