import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- BACKGROUND COLOUR ------------------------------- #
def choose_background():
    if window["bg"] == "#F3F1F5":
        new_background = "#082032"
        new_font = "#F7F7F7"
    else:
        new_background = "#F3F1F5"
        new_font = "#000000"
    window.config(bg=new_background)
    canvas.config(bg=new_background)
    website_label.config(bg=new_background, fg=new_font)
    email_label.config(bg=new_background, fg=new_font)
    password_label.config(bg=new_background, fg=new_font)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # My solution
    # password_list = [choice(letters) for _ in range(randint(8, 10))]
    # password_list += [choice(symbols) for _ in range(randint(2, 4))]
    # password_list += [choice(numbers) for _ in range(randint(2, 4))]

    # Angela's solution
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(symbols) for _ in range(randint(2, 4))]
    password_symbols = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)

    # password = ""
    # for char in password_list:
    #   password += char
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        # Angela's solution
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", mode='w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            messagebox.showinfo(title="Successful", message="Your data was saved!")
            website_entry.delete(0, END)
            password_entry.delete(0, END)

        # My solution
        # try:
        #     with open("data.json", mode="r") as data_file:
        #         # Reading old data
        #         data = json.load(data_file)
        # except FileNotFoundError:
        #     data = new_data
        # else:
        #     # Updating old data with new data
        #     data.update(new_data)
        # finally:
        #     with open("data.json", mode='w') as data_file:
        #         # Saving updated data
        #         json.dump(data, data_file, indent=4)
        #
        #     website_entry.delete(0, END)
        #     password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD -------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No Details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# Radio buttons
menubar = Menu(window)
options = Menu(menubar, tearoff=0)
options.add_command(label="Change colour", command=choose_background)
menubar.add_cascade(label="Background", menu=options)
window.config(menu=menubar)


canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=43)
website_entry.focus()
website_entry.grid(row=1, column=1)
email_entry = Entry(width=61)
email_entry.insert(END, "680633@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=43)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(row=3, column=2)
add_button = Button(text="Add", width=52, command=save)
add_button.grid(row=4, column=1, columnspan=2)

choose_background()
window.mainloop()
