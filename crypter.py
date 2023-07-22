import tkinter
from tkinter import filedialog
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("klucz", "wb") as key_file:
        key_file.write(key)
    return key

def read_key():
    try:
        with open("klucz", "rb") as key_file:
            key = key_file.read()
            return key
    except FileNotFoundError:
        return None

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        original_data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(original_data)

    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        encrypted_data = file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file, 'wb') as file:
        file.write(decrypted_data)

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tkinter.END)
    file_entry.insert(0, file_path)

def encrypt():
    input_file_path = file_entry.get()
    output_file_path = input_file_path + ".encrypted"
    key = read_key() or generate_key()
    encrypt_file(input_file_path, output_file_path, key)
    lbl_result.config(text=f"Plik zaszyfrowany pomyślnie.\nKlucz szyfrowania zapisany w pliku „klucz”.", fg="green")

def decrypt():
    input_file_path = file_entry.get()
    if input_file_path.endswith(".encrypted"):
        output_file_path = input_file_path[:-len(".encrypted")]
    else:
        output_file_path = input_file_path + ".decrypted"
    key = read_key()
    if key:
        decrypt_file(input_file_path, output_file_path, key)
        lbl_result.config(text="Plik odszyfrowany pomyślnie.", fg="green")
    else:
        lbl_result.config(text="Nie znaleziono klucza szyfrowania.\nWygeneruj go najpierw, szyfrując plik.", fg="red")
# ENGINE
root = tkinter.Tk()
root.title("Mikecrypt - 2023")
root.geometry("360x330")

# MAIN FRAME
frame = tkinter.LabelFrame(root)
frame.pack()

# FIRST LABEL
main_window = tkinter.Label(frame, text="Wybierz plik do zaszyfrowania lub odszyfrowania: ")
main_window.grid(pady=10)

# FILE ENTRY PATH
file_entry = tkinter.Entry(frame, width=50)
file_entry.grid(row=1, column=0, pady=10)

# BUTTONS

btn_przegladaj = tkinter.Button(frame, text="Wybierz plik", command=browse_file)
btn_przegladaj.grid(row=2, column=0, padx=20, pady=10, sticky="news")

btn_encrypt = tkinter.Button(frame, text="Zaszyfruj plik", command=encrypt, fg="red")
btn_encrypt.grid(pady=5, row=3, column=0)

btn_decrypt = tkinter.Button(frame, text="Odszyfruj plik", command=decrypt, fg="green")
btn_decrypt.grid(pady=5, row=4, column=0)

lbl_result = tkinter.Label(root, text="")
lbl_result.pack(pady=10)

author_frame = tkinter.LabelFrame(root)
author_frame.pack()

author_label = tkinter.Label(author_frame, text="Created by Mike Boro - 2023")
author_label.grid(row=0, column=0)

root.mainloop()