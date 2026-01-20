from nickcipher.core.cipher import DynamicEmojiCipher
import pytest
from nickcipher.core.filehandler import is_safe_path

def test_roundtrip_with_real_config():
    """
    Roundtrip-test:
    Om vi krypterar text och sedan dekrypterar den, ska vi få tillbaka originalet.
    """

    # 1) Skapa cipher från din riktiga config (emoji_pool.json + char_weight.json)
    cipher = DynamicEmojiCipher.from_config()

    # 2) Generera nyckel deterministiskt från ett test-lösenord
    cipher.generate_key("pytest-password-12345")

    # 3) Välj en text som bara innehåller tecken du vet stöds av din weights/key
    plaintext = "detta är ett test med åäö yzw och lite !!! och några ... och några ,,, eller varför inte några !!!???"

    # 4) Kryptera
    ciphertext = cipher.encode(plaintext)

    # 5) Dekryptera
    decoded = cipher.decode(ciphertext)

    # 6) Assert: pytest-kärnan. Om detta inte stämmer ska testet FAILA.
    assert decoded == plaintext


def test_decrypt_with_wrong_key_fails():
    c1 = DynamicEmojiCipher.from_config()
    c1.generate_key("key-one")

    plaintext = "detta är ett test med åäö yzw och lite !!! och några ... och några ,,, eller varför inte några !!!???"
    ciphertext = c1.encode(plaintext)

    c2 = DynamicEmojiCipher.from_config()
    c2.generate_key("key-two")

    decoded = c2.decode(ciphertext)

    assert decoded != plaintext

def test_no_key():

    cipher = DynamicEmojiCipher.from_config()
    
    plaintext = "detta är ett test med åäö yzw och lite !!! och några ... och några ,,, eller varför inte några !!!???"

    with pytest.raises(ValueError, match="No key generated"):
        cipher.encode(plaintext)


 
def test_safe_path_allows_relative_file(tmp_path):
    assert is_safe_path(tmp_path, "file.txt") is True

def test_safe_path_blocks_traversal(tmp_path):
    assert is_safe_path(tmp_path, "../evil.txt") is False


def test_emoji_weights_contract():


    weights = {"a": 5, "b": 5}
    emoji_pool = ["😀","😺","🐸"]

    cipher = DynamicEmojiCipher(emoji_pool, weights)
# 10 required emojis, only 3 provided → must fail

    with pytest.raises(ValueError, match="Not enough emojis in pool"):
        cipher.generate_key("failtest")


def test_encode_preserves_length():

    cipher = DynamicEmojiCipher.from_config()
    
    plaintext = "detta är ett test med åäö yzw och lite !!! och några ... och några ,,, eller varför inte några !!!???"

    cipher.generate_key("test12345")
    encoded_plaintext = cipher.encode(plaintext)

    assert len(encoded_plaintext) == len(plaintext)

def test_decode_preserves_length():
    cipher = DynamicEmojiCipher.from_config()
    cipher.generate_key("test12345")

    plaintext = "detta är ett test..."
    ciphertext = cipher.encode(plaintext)
    decoded = cipher.decode(ciphertext)

    assert len(decoded) == len(ciphertext)