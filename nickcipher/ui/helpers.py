from nickcipher.core.cipher import DynamicEmojiCipher
from nickcipher.config import OUTPUT_DIR, KEYS_DIR, DATA_DIR
from nickcipher.core.filehandler import is_safe_path, write_txt, save_json, load_json, select_json_interaction
import getpass
from nickcipher.utils.logger import get_logger


logger = get_logger("cipher")

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
    """Bakar ihop lösenord, nyckelgen och kodning med stöd för sparad nyckel."""
    action = "encryption" if mode == 'encrypt' else "decryption"
    logger.info(f"User requested {action}")
    
    # 1. Kolla om vi redan har en nyckel i minnet
    if cipher.key:
        logger.info("Active key loaded in memory")
        print("\n" + "—" * 40)
        print(f"🔑 ACTIVE KEY DETECTED")
        print(f"An emoji-key is already loaded.")
        print("—" * 40)
        
        use_active = input(f"Use active key for {action}? (y/n): ").lower()
        
        if use_active != 'y':
            logger.info("User discarded loaded key, generating new from password")
            # Om användaren väljer 'n', rensa och kör standard lösenords-input
            print("🔄 Clearing memory...")
            cipher.key = {}
            pwd = get_secure_password(f"Enter NEW password for {action}: ")
            cipher.generate_key(pwd)
        else:
            logger.info("User contiuing with active key")
            print(f"✅ Continuing with active key...")
    else:
        # 2. Om ingen nyckel finns, kör som vanligt
        pwd = get_secure_password(f"Enter password for {action}: ")
        logger.info("User generated key with password")
        cipher.generate_key(pwd)
    
    # 3. Kör själva kodningen/avkodningen
    if mode == 'encrypt':
        logger.info("Text encrypttion activated")
        return cipher.encode(text)
    logger.info("Text decryption activated")
    return cipher.decode(text)

def prompt_save_to_file(content):
    if ask_yes_no("Would you like to save this to a file?"):
        filename = input("Enter filename: ")
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        if is_safe_path(OUTPUT_DIR, filename):
            write_txt(OUTPUT_DIR / filename, content)
            logger.info(f"New file saved as {OUTPUT_DIR / filename}")
            print(f"✅ Saved to {OUTPUT_DIR / filename}")
        else:
            logger.info("Failed to save file")
            print("❌ Invalid filename or path.")

def print_menu():
    # En stilren ASCII-logga
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
    print("—" * 55)
    print("       Welcome to NickCipher – Your friendly Emoji Encryption Tool      ")
    print("—" * 55)
    
    # Menyn i en snygg lista
    print(" [1]  Encrypt text (input)")
    print(" [2]  Decrypt text (input)")
    print(" [3]  Encrypt from file (.txt)")
    print(" [4]  Decrypt from file (.txt)")
    print(" [5]  Key Management (Save/Load)")
    print(" [6]  Information & Security")
    print(" [7]  Exit")
    print("—" * 55)
    print("Selection: ", end="")

def show_information(cipher):
    # Dynamisk hämtning av data från cipher-objektet
    pool_size = len(cipher.emoji_pool)
    total_slots = sum(cipher.weights.values())

    print("\n" + "—" * 65)
    print("🕵️  NICKCIPHER - SECURITY BRIEFING")
    print("—" * 65)
    print("🔑 PASSWORD HASHING (SHA-256)")
    print("   Your password is processed through SHA-256 to create a")
    print("   256-bit unique seed. This ensures that even a tiny change")
    print("   in input creates a completely different emoji-key.")
    print()
    print("🌌 MATHEMATICAL STRENGTH")
    print(f"   Emoji Pool (n): {pool_size} symbols")
    print(f"   Key Slots (k):  {total_slots} positions")
    print()
    print("🧮 THE CALCULATION (Permutations)")
    print(f"   The number of unique ways to arrange the emoji-key is:")
    print(f"   P({pool_size}, {total_slots}) = {pool_size}! / ({pool_size} - {total_slots})!")  
    print()
    print(f"   RESULT: A number with ~589 digits.")
    print(f"   COMPARE: Atoms in the universe ≈ 10^80.")
    print()
    print("   Conclusion: Your key-space is larger than life so a brute-force")
    print("   attack on the emoji-key is physically impossible.")
    print("—" * 65)
    input("\nPress any key to return to menu...")

def manage_key_interaction(cipher):
    print("\n" + "—" * 45)
    print("🔑 KEY MANAGEMENT")
    print("—" * 45)
    print("1. Export: Save Password as Key File (.json)")
    print("2. Import: Load Key File (Bypass Password)")
    
    choice = input("\nChoice: ")

    if choice == "1":
        # 1. Hämta lösenord och generera nyckeln i minnet
        pwd = get_secure_password("Enter password to convert: ")
        cipher.generate_key(pwd)
        
        # 2. Ta emot filnamn och tvinga .json-ändelse
        filename = input("Enter filename for your key (e.g. 'my_key'): ")
        if not filename.endswith(".json"):
            filename += ".json"

        # 3. Säkerhetskontroll 
        if is_safe_path(KEYS_DIR, filename):
            save_path = KEYS_DIR / filename
            
            # 4. Spara cipher.key 
            save_json(save_path, cipher.key)
            logger.info(f"User saved key to {save_path} ")
            print(f"\n✅ Key successfully exported to:")
            print(f"   {save_path}")
        else:
            logger.warning("SECURITY ALERT: Possible path traversal attempt blocked")
            print("\n🚨 SECURITY ALERT: Path traversal attempt blocked!")

    elif choice == "2":
        # Använd din befintliga filväljare för att ladda nyckeln
        filename = select_json_interaction(KEYS_DIR, "keys")
        if filename:
            key_data = load_json(KEYS_DIR / filename)
            
            # Ladda in den i objektet så att encrypt/decrypt kan använda den
            cipher.key = key_data
            #skapa en reversed key
            cipher.load_reversed_key(key_data)
            logger.info(f"User loaded key {filename} from file")
            print(f"\n✅ Key '{filename}' is now ACTIVE.")
            print("   You can now decrypt files without entering a password.")
    else:
        print("Invalid choice.")

