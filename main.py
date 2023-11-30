from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# Password Generator
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# Password Storage
def save():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="All fields are not complete.")

    else:
        confirm = messagebox.askokcancel(title="Confirmation", message=f"Are you sure these are the details?"
                                                                       f"\nEmail: {email} \nPassword: {password}")
        if confirm:
            try:
                with open("data.json", "r") as data_file:
                    # Read the data.
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    # Writing new data.
                    json.dump(new_data, data_file, indent=4)
            else:
                # Update data in memory (data is a dictionary data structure)
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Write new data from memory to file.
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)


# Find password in storage
def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Website does not exist in storage.")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# User Interface
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=250, width=250)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(125, 125, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=40)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="W")

email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2, sticky="W")

password_entry = Entry(width=40)
password_entry.grid(row=3, column=1, columnspan=2, sticky="W")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password, width=15)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=21, command=save)
add_button.grid(row=4, column=1, pady=10, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(row=1, column=2)
window.mainloop()
