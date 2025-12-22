from pathlib import Path
import os

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

def select_file_from_folder(folder_path, folder_name):
    files = list_txt_files(folder_path)
    if not files:
        print(f"\n❌ No .txt files found in {folder_name}")
        return None
    
    print(f"\n--- Available Files in {folder_name} ---")
    for i, filename in enumerate(files, 1):
        print(f"{i}. {filename}")
    
    choice = input("\nSelect file number: ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
    
    print("❌ Invalid selection.")
    return None

def prompt_save_to_file(content):
    if ask_yes_no("Would you like to save this to a file?"):
        filename = input("Enter filename: ")
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        if is_safe_path(OUTPUT_DIR, filename):
            write_txt(OUTPUT_DIR / filename, content)
            print(f"✅ Saved to {OUTPUT_DIR / filename}")
        else:
            print("❌ Invalid filename or path.")