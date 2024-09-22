# main_script.py
from dictionary_attack.dictionary import dictionary  # Import the dictionary attack function
from hybrid_attack.hybrid_attack import hybrid_attack_pdf  # Import the hybrid attack function
from pdf_unlock.newpasshunter import main  # Import the brute force password recovery function

def password_recovery():
    # Ask the user to choose an attack method
    print("Choose a password recovery method:")
    print("1. Dictionary Attack")
    print("2. Hybrid Attack")
    print("3. Brute Force Attack")  # New option for brute force attack
    
    choice = input("Enter 1, 2, or 3: ")

    if choice == '1':
        # Dictionary Attack
        pdf_file = r'F:\PassHunter\Pass_maviya.pdf'  # Path to the PDF file
        password_list = r'F:\PassHunter\dictionary.txt'  # Path to the password dictionary file
        
        try:
            found_password = dictionary(pdf_file, password_list)
            if found_password:
                print(f'[+] Success! The password for {pdf_file} is: {found_password}')
            else:
                print(f'[!] Could not find the password for {pdf_file}.')
        except FileNotFoundError as e:
            print(f'[!] File not found: {e}')
        except Exception as e:
            print(f'[!] An error occurred: {e}')

    elif choice == '2':
        # Hybrid Attack
        pdf_file = r'F:\PassHunter\Pass_maviya123.pdf'  # Path to the PDF file
        password_list = r'F:\PassHunter\dictionary.txt'  # Path to the password dictionary file
        
        try:
            found_password = hybrid_attack_pdf(pdf_file, password_list, max_digits=3)
            if found_password:
                print(f'[+] Success! The password for {pdf_file} is: {found_password}')
            else:
                print(f'[!] Could not find the password for {pdf_file}.')
        except FileNotFoundError as e:
            print(f'[!] File not found: {e}')
        except Exception as e:
            print(f'[!] An error occurred: {e}')
    
    elif choice == '3':
        # Brute Force Attack (calls the `main` function from newpasshunter)
        try:
            print("[*] Starting brute force attack...")
            main()  # This will call the brute force logic implemented in the `main` function
        except Exception as e:
            print(f'[!] An error occurred: {e}')
    
    else:
        print('[!] Invalid choice. Please enter 1, 2, or 3.')

if __name__ == '__main__':
    password_recovery()
