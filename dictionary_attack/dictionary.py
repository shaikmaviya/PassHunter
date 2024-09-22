import pikepdf

def dictionary(pdf_file, password_list):
    # Open the password list file
    with open(password_list, 'r') as file:
        passwords = file.readlines()

    # Try each password from the list
    for password in passwords:
        password = password.strip()
        print(f'[~] Attempting: {password}')  # Print attempting message before each try
        try:
            with pikepdf.open(pdf_file, password=password):
                print(f'[+] Password found: {password}')
                return password
        except pikepdf.PasswordError:
            print(f'[-] Failed: {password}')
    
    print('[!] Password not found in the list.')
    return None
