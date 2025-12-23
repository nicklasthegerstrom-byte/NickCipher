from nickcipher.core.cipher import DynamicEmojiCipher
from nickcipher.config import INPUT_DIR, OUTPUT_DIR

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
    """Bakar ihop lösenord, nyckelgen och kodning."""
    action = "encryption" if mode == 'encrypt' else "decryption"
    pwd = get_secure_password(f"Enter password for {action}: ")
    
    cipher.generate_key(pwd)
    if mode == 'encrypt':
        return cipher.encode(text)
    return cipher.decode(text)

def print_menu():
    print("Welcome to NickCipher – your friendly text to emoji encryption tool.")
    print()
    print("1. Encrypt text (input)")
    print("2. Decrypt text (input)")
    print("3. Encrypt from file")
    print("4. Decrypt from file")
    print("5. Information")
    print("6. Save/load encryption key")
    print("7. Exit")

def show_information():
    print("\n" + "—" * 50)
    print("🕵️  NICKCIPHER - SECURITY BRIEFING")
    print("—" * 50)
    print("🔑 PASSWORDS")
    print("   Your password is the ONLY way to recover encrypted data.")
    print("   NickCipher uses it to generate a unique digital signature.")
    print("   Lose the password, and the data is lost forever.")
    print()
    print("🔄 SYMMETRY")
    print("   This is a symmetric encryption tool. The same key used")
    print("   to hide the message is required to reveal it.")
    print()
    print("🛡️  NO BACKDOORS")
    print("   Everything is handled locally on your machine.")
    print("   No keys are stored in the cloud. Your privacy is absolute.")
    print()
    print("💡 PRO TIP")
    print("   For maximum security, use passwords with symbols and")
    print("   avoid using the same password for different files.")
    print("—" * 50)
    input("\nPress Enter to return to menu...")