from nickcipher.core.keygen import load_emojis, load_weights
from nickcipher.config import BASE_DIR
from nickcipher.core.cipher import DynamicEmojiCipher

emoji_path = BASE_DIR / "emoji_pool.json"

weights_path = BASE_DIR / "char_weight.json"

emoji_pool = load_emojis(emoji_path)
weights = load_weights(weights_path)


cipher = DynamicEmojiCipher(emoji_pool, weights)
cipher.generate_key(12345)

text = "Denna mening mäter om d-tecken och n-tecken hamnar rätt. Mamma och pappa minns nio nätter i november. 123 456 789. Det fungerar nu? Hoppas!"

encoded_text = cipher.encode(text.lower())

print("Orginal text:")
print(text)
print("Krypterad text:")
print(encoded_text)

decoded_text = cipher.decode(encoded_text)

print("Avkodad text:")
print(decoded_text)