from tkinter import *
from tkinter import messagebox
import pyperclip
import json


# ------------------------------------------ #
# Password Generator Project


def generate():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for i in range(0, 8)]
    [password_list.append(random.choice(numbers)) for i in range(random.randint(1, 2))]
    [password_list.append(random.choice(symbols)) for i in range(random.randint(1, 2))]

    random.shuffle(password_list)
    password_str = ''.join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, f'{password_str}')

    # copies generated password into clipboard
    pyperclip.copy(password_str)


# ------------------------------------------ #
window = Tk()
window.config(padx=50, pady=50)
window.title("Password App")

logo_img = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo_img)

website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

web_input = Entry(width=22)
web_input.focus()
email_input = Entry(width=40)
email_input.insert(0, 'johndoe@sample.com')
password_input = Entry(width=22)


# ------------------------------------------ #
def save():
    website = web_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website.lower(): {
            "email": email.lower(),
            "password": password
        }
    }

    # checks if there are any blank fields
    if web_input.get() == '' or email_input.get() == '' or password_input.get() == '':
        messagebox.showerror(title="Incomplete details", message="Please fill out all fields")
        is_confirmed = False

    else:
        # confirms user input details
        is_confirmed = messagebox.askokcancel(title="Confirmation", message=f"Please confirm entered details:\n"
                                                                            f"Website: {web_input.get()} \n"
                                                                            f"Email: {email_input.get()} \n"
                                                                            f"Password: {password_input.get()}")

    if is_confirmed:
        try:
            # opens, reads and updates existing user_data file
            with open('user_data.json', mode='r') as data_file:
                original_data = json.load(data_file)
                original_data.update(new_data)
        except FileNotFoundError:
            # writes and creates user_data file if not existing
            with open('user_data.json', mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # writes to existing user_data file
            with open('user_data.json', mode='w') as data_file:
                json.dump(original_data, data_file, indent=4)
        finally:
            web_input.delete(0, END)
            password_input.delete(0, END)
            web_input.focus()


def search():
    website = web_input.get()
    try:
        with open('user_data.json', mode='r') as data_file:
            original_data = json.load(data_file)

    except FileNotFoundError:
        print('No existing data!')

    else:
        try:
            messagebox.showinfo(title=f'{website.title()}',
                                message=f'Email: {original_data[website.lower()]["email"]}\n'
                                        f'Password: {original_data[website.lower()]["password"]}')
            pyperclip.copy(original_data[website.lower()]["password"])

        except KeyError:
            messagebox.showerror(title="Error!",
                                 message="Website not found!")


# ------------------------------------------ #
add_password = Button(text="Add", width=35, command=save)
generate_password = Button(text="Generate Password", command=generate)
search_site = Button(text="Search", command=search, width=14)

canvas.grid(column=2, row=1)
website_label.grid(column=1, row=2)
web_input.grid(column=2, row=2)
search_site.grid(column=3, row=2)
email_label.grid(column=1, row=3)
email_input.grid(column=2, row=3, columnspan=2)
password_label.grid(column=1, row=4)
password_input.grid(column=2, row=4)
generate_password.grid(column=3, row=4)
add_password.grid(column=2, row=5, columnspan=2)

while True:
    window.mainloop()
