from nickcipher.core.cipher import DynamicEmojiCipher
from nickcipher.config import OUTPUT_DIR, KEYS_DIR, DATA_DIR
from nickcipher.core.filehandler import is_safe_path, write_txt, save_json, load_json, select_json_interaction
import getpass
from nickcipher.utils.logger import get_logger
import math


logger = get_logger("helpers")

def ask_yes_no(prompt):
    
    while True:
        answer = input(f"{prompt} (y/n): ").lower().strip()
        if answer in ['y', 'yes']:
            return True
        if answer in ['n', 'no']:
            return False
        print("❌ Invalid input, please enter 'y' or 'n'.")

def get_secure_password(prompt="Enter password: "):
    while True:
        # getpass döljer vad man skriver i terminalen
        pwd = getpass.getpass(prompt)
        if len(pwd) >= 4: # Enkel validering
            return pwd
        print("❌ Password must be at least 4 characters.")


def perform_cipher_op(cipher, text, mode='encrypt'):
    action = "encryption" if mode == 'encrypt' else "decryption"
    logger.info(f"User requested {action}")

    # 1. Nyckelhantering
    if cipher.key is None:
        pwd = get_secure_password(f"Enter password for {action}: ")
        cipher.generate_key(pwd)
        
        if cipher.session_lock is None:
            if ask_yes_no("Do you want to save this key in session memory (No password, proceed with caution!)"):
                cipher.session_lock = True
                print("✅ Key locked to session memory.")
            else:
                cipher.session_lock = False
                print("🛡️ High-security mode: Key will be cleared after this operation.")

    # 2. Utförande med garanterad städning
    try:
        if mode == 'encrypt':
            logger.info("Encoding text...")
            return cipher.encode(text)
        else:
            logger.info("Decoding text...")
            return cipher.decode(text)
            
    finally:
        # Körs ALLTID, även efter en 'return' i try-blocket för att säkerställa nyckeln städas bort.
        if cipher.session_lock is False:
            cipher.erase_key()
            print("\n[Security] Session memory cleared. Password required for next use.")
            logger.info("Key erased from RAM as per user security preference.")

def prompt_save_to_file(content):
    if ask_yes_no("Would you like to save this to a file?"):
        filename = input("Enter filename: ")
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        if is_safe_path(OUTPUT_DIR, filename):
            write_txt(OUTPUT_DIR / filename, content)
            print(f"✅ Saved to {OUTPUT_DIR / filename}")
        else:
            logger.info("Failed to save file")
            print("❌ Invalid filename or path.")

def print_menu(cipher):
    # Definiera bredden baserat på dina streck (55 tecken)
    width = 55

    print(r"""
    _   _ _      _      _____ _       _               
   | \ | (_)    | |    / ____(_)     | |              
   |  \| |_  ___| | __| |     _ _ __ | |__   ___ _ __ 
   | . ` | |/ __| |/ /| |    | | '_ \| '_ \ / _ \ '__|
   | |\  | | (__|   < | |____| | |_) | | | |  __/ |   
   |_| \_|_|\___|_|\_\ \_____|_| .__/|_| |_|\___|_|   
                               | |                    
                               |_|                    
    """)
    print("—" * width)
    print("Welcome to NickCipher – Your friendly Emoji Encryption Engine".center(width))
    print("—" * width)

    # Status-logik centrerad
    if cipher.key:
        status_msg = "STATUS: SESSION ACTIVE (No password needed) 🔒"
    else:
        status_msg = "STATUS: NO KEY LOADED / SESSION SECURED 🛡️"
    
    print(status_msg.center(width))
    
    print("—" * width)
    # Listan ser oftast bäst ut vänsterjusterad med lite indrag
    print(" [1]  Encrypt text (input)")
    print(" [2]  Decrypt text (input)")
    print(" [3]  Encrypt from file (.txt)")
    print(" [4]  Decrypt from file (.txt)")
    print(" [5]  CLEAR ACTIVE KEY / LOGOUT")
    print(" [6]  Key Management (Save/Load)")
    print(" [7]  Information & Security")
    print(" [8]  Exit")
    print("—" * width)
    

def estimate_keyspace_digits(pool_size: int, total_slots: int) -> int:
    """Return approx number of decimal digits in P(pool_size, total_slots)."""
    if total_slots > pool_size:
        return 0  

    log10_p = 0.0
    for i in range(pool_size - total_slots + 1, pool_size + 1):
        log10_p += math.log10(i)
    return int(log10_p) + 1

def show_information(cipher):
    pool_size = len(cipher.emoji_pool)
    total_slots = sum(cipher.weights.values())
    digits = estimate_keyspace_digits(pool_size, total_slots)

    print("\n" + "—" * 65)
    print("🕵️  NICKCIPHER - SECURITY BRIEFING".center(65))
    print("—" * 65)
    
    print("🔑 THE HUMAN ELEMENT (The Bottleneck)")
    print("   SHA-256 turns your password into a deterministic 256-bit seed.")
    print("   It does NOT prevent guessing — it only transforms the input.")
    print("   • If you use '1234', an attacker can replicate your key in milliseconds.")
    print("   💡 TIP: Use a long passphrase. Entropy (length + randomness) matters most.")
    print()
    
    print("🌌 THE MAPPING STRENGTH (Theoretical Key Space)")
    print(f"   If your password is strong, the mathematical barrier is massive:")
    print(f"   • Emoji Pool: {pool_size} symbols")
    print(f"   • Key Slots:  {total_slots} positions")
    print()
    
    print("🧮 MATHEMATICAL MAGNITUDE")
    # LaTeX för den tekniska biten
    print(f"   Permutations: $P({pool_size}, {total_slots}) = \\frac{{{pool_size}!}}{{({pool_size} - {total_slots})!}}$")
    print(f"   Possible Keys: A number with ~{digits} digits.")
    print()
    
    print("🛡️ ATTACK VECTORS")
    print("   • Brute-forcing the emoji-key mapping: Computationally infeasible.")
    print("     (The search space is astronomically large)")
    print("   • Dictionary/Guessing attacks: HIGH RISK.")
    print("     (Security depends entirely on your password's entropy)")
    print("—" * 65)
    input("\nPress any key to return to menu...")

def manage_key_interaction(cipher):
    print("\n" + "—" * 45)
    print("🔑 KEY MANAGEMENT".center(45))
    print("—" * 45)
    print(" 1. Export: Save current key to file (.json)")
    print(" 2. Import: Load key from file (Bypass password)")
    
    choice = input("\nChoice: ")

    if choice == "1":
        # Om det inte finns en nyckel i minnet, be användaren generera en först
        if cipher.key is None:
            print("\n[!] No active key to export.")
            pwd = get_secure_password("Enter password to generate key for export: ")
            cipher.generate_key(pwd)
        
        filename = input("Enter filename for your key: ").strip()
        if not filename:
            print("❌ Filename cannot be empty.")
            return

        if not filename.endswith(".json"):
            filename += ".json"

        if is_safe_path(KEYS_DIR, filename):
            save_path = KEYS_DIR / filename
            save_json(save_path, cipher.key)
            logger.info(f"User saved key to {save_path}")
            print(f"\n✅ Key successfully exported to {filename}")
        else:
            logger.warning("Path traversal attempt blocked")
            print("\n🚨 Invalid path/filename!")

    elif choice == "2":
        filename = select_json_interaction(KEYS_DIR, "keys")
        if filename:
            #Kolla om en nyckel redan finns inläst
            if cipher.key:
                if not ask_yes_no("An active key is already in memory. Override it?"):
                    print("Load cancelled.")
                    return
            
            key_data = load_json(KEYS_DIR / filename)
            #måste skapa en reverse nyckel för den nya nyckeln.
            cipher.load_reversed_key(key_data)
            
            #Fortsätt session lock så att nyckeln inte läses över
            cipher.session_lock = True
            
            logger.info(f"User loaded key {filename}")
            print(f"\n✅ Key '{filename}' is now ACTIVE and LOCKED to session.")

    else:
        print("Invalid choice.")

