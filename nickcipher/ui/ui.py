from nickcipher.core.cipher import DynamicEmojiCipher
from nickcipher.config import INPUT_DIR, OUTPUT_DIR
from nickcipher.core.filehandler import is_safe_path, write_txt, select_txt_interaction, read_txt
from nickcipher.ui.helpers import ask_yes_no, print_menu, perform_cipher_op, show_information, prompt_save_to_file, manage_key_interaction
import os



def app():
    
    cipher = DynamicEmojiCipher.from_config()

    while True:
        print_menu()
        choice = input("Make your choice: ")

        if choice in ["1", "2"]:
            mode = 'encrypt' if choice == "1" else 'decrypt'
            text = input(f"Enter text to {mode}: ")
                
            result = perform_cipher_op(cipher, text, mode)
            print(f"\n--- RESULT ---\n{result}\n--------------")

            prompt_save_to_file(result)
                

        elif choice == "3":
            filename = select_txt_interaction(INPUT_DIR, "Input Folder")
            if filename:
                # Använd Path Traversal check i kombination med läsning
                if is_safe_path(INPUT_DIR, filename):
                    content = read_txt(INPUT_DIR / filename)
                    result = perform_cipher_op(cipher, content, 'encrypt')
                        
                    out_name = f"enc_{filename}"
                    write_txt(OUTPUT_DIR / out_name, result)
                    print(f"✅ Success! Encrypted file: {out_name}")

            # --- VAL 4: FIL-AVKODNING ---
        elif choice == "4":
            filename = select_txt_interaction(OUTPUT_DIR, "Output Folder")
            if filename:
                if is_safe_path(OUTPUT_DIR, filename):
                    content = read_txt(OUTPUT_DIR / filename)
                    result = perform_cipher_op(cipher, content, 'decrypt')
                    print(f"\n--- DECRYPTED CONTENT ---\n{result}\n-------------------------")
                        
                    if ask_yes_no("Save decrypted text to a new file?"):
                        write_txt(OUTPUT_DIR / f"decrypted_{filename}", result)
                        print("✅ Saved!")
        
        elif choice == "5":
            manage_key_interaction(cipher)

        elif choice == "6":
            show_information(cipher)
        
        elif choice == "7":
            if ask_yes_no("Are you sure you want to quit?"):
                break

        else:
            print("❌ Not valid input. Try again!")            

