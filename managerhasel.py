import tkinter
from tkinter import messagebox
from cryptography.fernet import Fernet
import os
import random
import string




okno = tkinter.Tk()
okno.title("Manager haseł")
okno.geometry("1000x600")

BASE_dir = os.path.dirname(os.path.abspath(__file__))

def generate_password():
    password_entry.delete(0, tkinter.END)

    litery = string.ascii_letters
    cyfry = string.digits
    znaki_specjalne = string.punctuation

    password_list =[
        random.choice(litery) ,
        random.choice(cyfry),
        random.choice(znaki_specjalne)
    ]

    all_characters = litery + cyfry + znaki_specjalne

    for _ in range(8):
        password_list.append(random.choice(all_characters))
    
    random.shuffle(password_list)

    password = ''.join(password_list)
    password_entry.insert(0, password)

def loadkickey():
    key_path = os.path.join(BASE_dir, "key.key")

    
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    try:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    return key
key = loadkickey()
cipher_suite =Fernet(key)

def serch_password():
    website = website_entry.get()
    hasla_path = os.path.join(BASE_dir, "hasla.txt")

    try:
        with open(hasla_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = eval(line.strip())
                if website in data:
                    email = data[website]["email"]
                    encrypted_password = data[website]["password"]
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    okno.clipboard_clear()
                    okno.clipboard_append(decrypted_password)
                    okno.update()  # Teraz schowek jest zaktualizowany
                    messagebox.showinfo(title=website, message=f"Email: {email}\nHasło: {decrypted_password} \n\nHasło zostało skopiowane do schowka.")
                    return
            messagebox.showwarning(title="Błąd", message="Nie znaleziono danych dla podanej strony!")
    except FileNotFoundError:
        messagebox.showwarning(title="Błąd", message="Plik z hasłami nie istnieje!")

def safe_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    hasla_path = os.path.join(BASE_dir, "hasla.txt")

    if  not website or not email or not password:
        messagebox.showwarning(title="Błąd", message="Proszę wypełnić wszystkie pola!")
    else:
        zaszyfrowane_haslo = cipher_suite.encrypt(password.encode()).decode()

        new_data={
            website: {
                "email": email,
                "password": zaszyfrowane_haslo
            }
        }
          # Prosta "szyfrowanie" przez odwrócenie hasła
        with open(hasla_path, "a") as file:
            file.write(new_data.__str__() + "\n")
        messagebox.showinfo(title="Sukces", message="Hasło zostało zapisane pomyślnie!")
    website_entry.delete(0, tkinter.END)
    email_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)

website_label = tkinter.Label(okno, text="Nazwa strony:")
website_label.grid(row=1, column=0, padx=10, pady=10)
website_email = tkinter.Label(okno, text="Email/Username:")
website_email.grid(row=2, column=0, padx=10, pady=10)
website_password = tkinter.Label(okno, text="Hasło:")
website_password.grid(row=3, column=0, padx=10, pady=10)


website_entry = tkinter.Entry(okno, width=35)
website_entry.grid(row=1, column=1, padx=10, pady=10)

email_entry = tkinter.Entry(okno, width=35)
email_entry.grid(row=2, column=1, padx=10, pady=10)
password_entry = tkinter.Entry(okno, width=35)
password_entry.grid(row=3, column=1, padx=10, pady=10)
add_button = tkinter.Button(okno, text="Dodaj", width=36, command=safe_password)
add_button.grid(row=4, column=1, padx=10, pady=10)
serch_button = tkinter.Button(okno, text="Szukaj", width=13,command=serch_password)
serch_button.grid(row=1, column=2, padx=10, pady=10)
gemerate_button = tkinter.Button(okno, text="Generuj hasło", width=13,command=generate_password
                                 )
gemerate_button.grid(row=3, column=2, padx=10, pady=10)






okno.mainloop()