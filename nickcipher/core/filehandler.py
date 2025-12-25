from pathlib import Path
import os
import json

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

def list_txt_files(directory):
    """
    Returnerar en lista med namnen på alla .txt-filer i en viss mapp.
    """
    if not Path(directory).exists():
        return []
    
    #  filtrerar så vi bara får filer (inte mappar) som slutar på .txt
    return [f for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f)) 
            and f.endswith('.txt')]


def select_txt_interaction(directory, folder_label):
    """Hanterar listning och val av fil via siffra."""
    files = list_txt_files(directory)
    if not files:
        print(f"\nEmpty! No .txt files found in {folder_label}")
        return None
    
    print(f"\n--- Available Files in {folder_label} ---")
    for i, filename in enumerate(files, 1):
        print(f"{i}. {filename}")
    
    choice = input("\nSelect file number (or 'q' to go back): ")
    if choice.lower() == 'q': return None

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
    
    print("❌ Invalid selection.")
    return None

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def list_json_files(directory):
    path = Path(directory)
    return [f.name for f in path.glob("*.json")]

def select_json_interaction(directory, folder_label):
    """Hanterar listning och val av JSON-nycklar."""
    files = list_json_files(directory) # Använder den nya funktionen ovan
    
    if not files:
        print(f"\nNo keys found in {folder_label}")
        return None
    
    print(f"\n--- Available Keys ---")
    for i, filename in enumerate(files, 1):
        print(f"{i}. {filename}")
    
    choice = input("\nSelect key number (or 'q'): ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
    return None