import PyPDF2

def add_password(input_pdf, output_pdf, password):
    # Open the input PDF file in read-binary mode
    with open(input_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()

        # Add all pages to the writer object
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Add encryption to the PDF with the specified password
        writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)

        # Write the encrypted PDF to a new file
        with open(output_pdf, 'wb') as encrypted_pdf_file:
            writer.write(encrypted_pdf_file)

        print(f"Password added to {output_pdf}")

# Example usage
input_pdf = 'C:\\Users\\Maviya\\Desktop\\Shaik Maviya.pdf'
output_pdf = 'Pass_maviya123.pdf'
password = 'maviya123'

add_password(input_pdf, output_pdf, password)
