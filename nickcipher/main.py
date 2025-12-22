from nickcipher.core.keygen import load_emojis, load_weights
from nickcipher.config import BASE_DIR
from nickcipher.core.cipher import DynamicEmojiCipher

emoji_path = BASE_DIR / "emoji_pool.json"

weights_path = BASE_DIR / "char_weight.json"

emoji_pool = load_emojis(emoji_path)
weights = load_weights(weights_path)


cipher = DynamicEmojiCipher(emoji_pool, weights)
cipher.generate_key(12345)

text = "I en värld som ständigt förändras har tekniken blivit den osynliga tråden som binder samman oss alla. För bara några decennier sedan var tanken på en global superdator i fickan inget annat än ren science fiction, men idag är det vår verklighet. Vi navigerar genom digitala landskap med en hastighet som våra förfäder aldrig hade kunnat föreställa sig."

encoded_text = cipher.encode(text.lower())

print("Orginal text:")
print(text)
print("Krypterad text:")
print(encoded_text)
