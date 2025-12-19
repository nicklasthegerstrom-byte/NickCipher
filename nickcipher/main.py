from nickcipher.keygen import load_emojis, load_weights
from nickcipher.config import BASE_DIR
from nickcipher.cipher import DynamicEmojiCipher

emoji_pool_path = BASE_DIR / "emoji_pool.json"
weights_path = BASE_DIR / "char_weight.json"
emoji_pool = load_emojis(emoji_pool_path)
weights = load_weights(weights_path)

text ="Vi testar att översätta detta med min nya klass"

#cipher = DynamicEmojiCipher(emoji_pool, weights, 12345)
#cipher.generate_key()
#encoded_text = cipher.encode(text)


print(len(emoji_pool))