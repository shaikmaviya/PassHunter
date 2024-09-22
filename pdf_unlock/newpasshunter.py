import pikepdf
import zipfile
import rarfile
import string
import os
from tkinter import Tk, Label, Button, Text, Frame, Entry, messagebox, Scrollbar, WORD
from tkinter import filedialog

# Global variables to hold the selected file and password length
selected_file = None
password_length = 0
cancelled = False  # Variable to track cancellation

def check_password_range(input_file, file_type, password_length, start, end, status_label, attempts_text):
    characters = string.ascii_letters + string.digits + string.punctuation

    for index in range(start, end):
        if cancelled:
            status_label.config(text="Process cancelled.")
            return None

        password = ''
        temp_index = index

        for i in range(password_length):
            password = characters[temp_index % len(characters)] + password
            temp_index //= len(characters)

        # Update the status label and attempts text
        status_label.config(text=f"Attempting password: {password}")
        attempts_text.insert("end", f"Attempting: {password}\n")
        attempts_text.see("end")
        status_label.update_idletasks()

        try:
            if file_type == "pdf":
                with pikepdf.open(input_file, password=password):
                    status_label.config(text=f"Password found: {password}")
                    attempts_text.insert("end", f"Password found: {password}\n")
                    return password
            elif file_type == "zip":
                with zipfile.ZipFile(input_file) as zf:
                    zf.extractall(pwd=bytes(password, 'utf-8'))
                    status_label.config(text=f"Password found: {password}")
                    attempts_text.insert("end", f"Password found: {password}\n")
                    return password
            elif file_type == "rar":
                with rarfile.RarFile(input_file) as rf:
                    rf.extractall(pwd=password)
                    status_label.config(text=f"Password found: {password}")
                    attempts_text.insert("end", f"Password found: {password}\n")
                    return password
        except (pikepdf.PasswordError, RuntimeError, zipfile.BadZipFile, rarfile.RarWrongPassword):
            pass  # Incorrect password, continue checking
        except Exception as e:
            status_label.config(text=f"An error occurred: {e}")
            attempts_text.insert("end", f"An error occurred: {e}\n")
            status_label.update_idletasks()

    return None

def brute_force_password(input_file, file_type, password_length, status_label, attempts_text):
    global cancelled
    cancelled = False
    characters = string.ascii_letters + string.digits + string.punctuation
    total_combinations = len(characters) ** password_length

    status_label.config(text=f"Total combinations: {total_combinations}")
    status_label.update_idletasks()

    for index in range(total_combinations):
        result = check_password_range(input_file, file_type, password_length, index, index + 1, status_label, attempts_text)
        if result:
            return result
        if cancelled:
            break

    status_label.config(text="Password not found.")

def select_file(status_label, password_entry):
    global selected_file, password_length
    selected_file = filedialog.askopenfilename(title="Select the encrypted file")
    if selected_file:
        status_label.config(text=f"Selected file: {selected_file}")
        try:
            password_length = int(password_entry.get())
            if password_length <= 0:
                messagebox.showerror("Error", "Password length must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid password length. Please enter a number.")
            return

def start_brute_force(status_label, attempts_text):
    global selected_file, password_length
    if selected_file and password_length > 0:
        _, file_extension = os.path.splitext(selected_file)
        file_extension = file_extension.lower()

        if file_extension == ".pdf":
            file_type = "pdf"
        elif file_extension == ".zip":
            file_type = "zip"
        elif file_extension == ".rar":
            file_type = "rar"
        else:
            status_label.config(text="Unsupported file type.")
            return

        brute_force_password(selected_file, file_type, password_length, status_label, attempts_text)
    else:
        messagebox.showerror("Error", "Please select a file and enter a valid password length.")

def cancel_process(status_label):
    global cancelled
    cancelled = True
    status_label.config(text="Cancelling...")

def main():
    root = Tk()
    root.title("Password Brute Forcer")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")

    frame = Frame(root, bg="#ffffff", bd=2, relief="groove")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = Label(frame, text="Password Brute Forcer", bg="#ffffff", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    label = Label(frame, text="Select an encrypted file:", bg="#ffffff", font=("Arial", 12))
    label.pack(pady=5)

    status_label = Label(frame, text="", wraplength=400, bg="#ffffff", font=("Arial", 10))
    status_label.pack(pady=5)

    password_label = Label(frame, text="Enter password length:", bg="#ffffff", font=("Arial", 12))
    password_label.pack(pady=5)

    password_entry = Entry(frame, width=10, font=("Arial", 12), bd=2, relief="solid")
    password_entry.pack(pady=5)

    attempts_text = Text(frame, height=10, width=80, wrap=WORD, bg="#e9ecef", font=("Courier New", 10), bd=1, relief="flat")
    attempts_text.pack(pady=5)

    select_button = Button(root, text="Select File", command=lambda: select_file(status_label, password_entry), bg="#007bff", fg="white", font=("Arial", 12), bd=0, relief="raised")
    select_button.pack(pady=5)

    submit_button = Button(root, text="Submit", command=lambda: start_brute_force(status_label, attempts_text), bg="#28a745", fg="white", font=("Arial", 12), bd=0, relief="raised")
    submit_button.pack(pady=5)

    # Change the cancel button color to orange
    cancel_button = Button(root, text="Cancel", command=lambda: cancel_process(status_label), bg="#28a745", fg="black", font=("Arial", 12), bd=0, relief="raised")
    cancel_button.pack(pady=5)

    root.mainloop()
if __name__ == "__main__":
    main()
