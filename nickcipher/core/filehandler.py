from pathlib import Path

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


def is_safe_path(base_dir, user_input):
    # Skapa en absolut sökväg för basmappen och den sökta filen
    base_path = Path(base_dir).resolve()
    target_path = (base_path / user_input).resolve()
    
    # Kolla om target_path faktiskt börjar med base_path
    return base_path in target_path.parents or base_path == target_path