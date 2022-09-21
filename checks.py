from tkinter import messagebox
from datetime import date
import re
def check_name(name):
    if len(name.split()) < 2:
        messagebox.showerror("Error", "Please enter the Full Name")
        return False
    else:
        return True

def check_dob(dob):
    today = date.today()
    birthdate = date(int(dob.split('/')[2]), int(dob.split('/')[1]), int(dob.split('/')[0]))
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    print(age)

    if age >= 18:
        return True
    else:
        messagebox.showerror("Error", "The adult is not over the age of 18")

def check_dob_child(dob):
    today = date.today()
    birthdate = date(int(dob.split('/')[2]), int(dob.split('/')[1]), int(dob.split('/')[0]))
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    print(age)

    if age < 18:
        return True
    else:
        messagebox.showerror("Error", "The child is over 18 or older")

def check_email(email):
    email_checker = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(email_checker, email):
        return True
    else:
        messagebox.showerror("Error", "Please Check the email entered")
        return False