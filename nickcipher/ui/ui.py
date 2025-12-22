from nickcipher.core.cipher import DynamicEmojiCipher

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

def app():
    
    while True:
        print_menu()

        choice = input("Make your choice")

        if choice == 1:
            password_input = input("Choose password")
            text_input = input("Input your text to encrypt here:")
            

