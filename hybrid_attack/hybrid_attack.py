import pikepdf
import itertools
from tkinter import Tk, Label, Button, Text, Frame, Entry, filedialog, messagebox, Scrollbar, WORD

# Function to try opening the PDF file with a given password
def try_open_pdf(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password):
            return True  # Password is correct
    except pikepdf.PasswordError:
        return False  # Incorrect password

# Function to try dictionary attack with brute-force appending numbers
def hybrid_attack_pdf(pdf_file, wordlist, max_digits, status_label, attempts_text):
    # Load the dictionary words
    try:
        with open(wordlist, 'r') as file:
            dictionary = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "Dictionary file not found.")
        return

    # Remove newlines and spaces from dictionary words
    dictionary = [word.strip() for word in dictionary]

    # Try each word in the dictionary
    for word in dictionary:
        # First try the word as-is
        status_label.config(text=f'Trying password: {word}')  # Update status label
        attempts_text.insert("end", f'Trying password: {word}\n')  # Show the attempt
        attempts_text.see("end")  # Scroll to the latest entry

        if try_open_pdf(pdf_file, word):
            attempts_text.insert("end", f'[+] Password found: {word}\n')
            return word

        # Try appending digits (hybrid attack)
        for num_digits in range(1, max_digits + 1):
            for digits in itertools.product('0123456789', repeat=num_digits):
                candidate = word + ''.join(digits)
                status_label.config(text=f'Trying password: {candidate}')  # Update status label
                attempts_text.insert("end", f'Trying password: {candidate}\n')  # Show the attempt
                attempts_text.see("end")  # Scroll to the latest entry

                if try_open_pdf(pdf_file, candidate):
                    attempts_text.insert("end", f'[+] Password found: {candidate}\n')
                    return candidate

    attempts_text.insert("end", '[!] Password not found.\n')
    return None

def select_pdf_file(status_label):
    global selected_pdf
    selected_pdf = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF Files", "*.pdf")])
    if selected_pdf:
        status_label.config(text=f"Selected PDF: {selected_pdf}")

def select_dictionary_file(status_label):
    global selected_dictionary
    selected_dictionary = filedialog.askopenfilename(title="Select Dictionary File", filetypes=[("Text Files", "*.txt")])
    if selected_dictionary:
        status_label.config(text=f"Selected Dictionary: {selected_dictionary}")

def start_attack(status_label, attempts_text):
    if not selected_pdf or not selected_dictionary:
        messagebox.showerror("Error", "Please select both a PDF file and a dictionary file.")
        return

    max_digits = int(max_digits_entry.get())
    hybrid_attack_pdf(selected_pdf, selected_dictionary, max_digits, status_label, attempts_text)

# Initialize global variables for file selections
selected_pdf = None
selected_dictionary = None

# Main GUI function
def main():
    global max_digits_entry

    root = Tk()
    root.title("PDF Hybrid Dictionary Attack Tool")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")

    frame = Frame(root, bg="#ffffff", bd=2, relief="groove")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = Label(frame, text="PDF Hybrid Dictionary Attack Tool", bg="#ffffff", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    status_label = Label(frame, text="", wraplength=400, bg="#ffffff", font=("Arial", 10))
    status_label.pack(pady=5)

    attempts_text = Text(frame, height=10, width=80, wrap=WORD, bg="#e9ecef", font=("Courier New", 10), bd=1, relief="flat")
    attempts_text.pack(pady=5)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    attempts_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=attempts_text.yview)

    max_digits_label = Label(frame, text="Enter max digits to append:", bg="#ffffff", font=("Arial", 12))
    max_digits_label.pack(pady=5)

    max_digits_entry = Entry(frame, width=10, font=("Arial", 12), bd=2, relief="solid")
    max_digits_entry.pack(pady=5)

    pdf_button = Button(root, text="Select PDF File", command=lambda: select_pdf_file(status_label), bg="#007bff", fg="white", font=("Arial", 12), bd=0, relief="raised")
    pdf_button.pack(pady=5)

    dict_button = Button(root, text="Select Dictionary File", command=lambda: select_dictionary_file(status_label), bg="#007bff", fg="white", font=("Arial", 12), bd=0, relief="raised")
    dict_button.pack(pady=5)

    start_button = Button(root, text="Start Attack", command=lambda: start_attack(status_label, attempts_text), bg="#28a745", fg="white", font=("Arial", 12), bd=0, relief="raised")
    start_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
