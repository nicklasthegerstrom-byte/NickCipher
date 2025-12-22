from nickcipher.core.cipher import DynamicEmojiCipher
import os

def ask_yes_no(prompt):
    
    while True:
        answer = input(f"{prompt} (y/n): ").lower().strip()
        if answer in ['y', 'yes']:
            return True
        if answer in ['n', 'no']:
            return False
        print("❌ Invalid input, please enter 'y' or 'n'.")

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
    
    cipher = DynamicEmojiCipher.from_config()

    while True:
        print_menu()
        choice = input("Make your choice: ")

        if choice == "1": 
            password_input = input("Choose password: ")
            text_input = input("Input your text to encrypt here: ")

            cipher.generate_key(password_input)
            result = cipher.encode(text_input)

            print(f"\n--- ENCRYPTED RESULT ---\n{result}\n------------------------\n")
            
            if not ask_yes_no("Do you want to perform another action?"):
                print("Exiting NickCipher. Have a secure day!")
                break

        elif choice == "2":
            password_input = input("Input unique key password: ")
            text_input = input("Input your text to decrypt here: ")

            cipher.generate_key(password_input)
            result = cipher.decode(text_input)

            print(f"\n--- DECRYPTED RESULT ---\n{result}\n------------------------\n")
            
            if not ask_yes_no("Do you want to perform another action?"):
                print("Exiting NickCipher. Have a secure day!")
                break
        
        elif choice == "7":
            if ask_yes_no("Are you sure you want to quit?"):
                break
            

