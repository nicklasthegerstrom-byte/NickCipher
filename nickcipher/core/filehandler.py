
def read_txt(filepath):
    """Läser in text från en fil."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Kunde inte hitta filen: {filepath}")
        return None

def write_txt(filepath, content):
    """Sparar text (t.ex. emojis) till en fil."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Text sparad till {filepath}")