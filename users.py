from encodings import search_function
from database_init import *
from tkinter import LEFT, font as tkFont
from tkinter import ttk
from members import *
from PIL import Image, ImageTk
from colors import *
import datetime
from tkinter import *
from checks import *
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import askyesno
from search_func import searchFunctionUser

def addUser(frame, canvas):
    
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    # Name
    namePrompt = tkinter.Label(container, text="Name: ", font=h1, fg="white", bg=blue)
    namePrompt.grid(row=0, column=0)

    nameEntry = tkinter.Entry(container, font=h2, width=50)
    nameEntry.grid(row=0, column=1, sticky='ew')

    # Email
    emailPrompt = tkinter.Label(container, text="Email: ", font=h1, fg="white", bg=blue)
    emailPrompt.grid(row=1, column=0)

    emailEntry = tkinter.Entry(container, font=h2)
    emailEntry.grid(row=1, column=1, sticky='ew')

    # Phone
    phonePrompt = tkinter.Label(container, text="Phone: ", font=h1, fg="white", bg=blue)
    phonePrompt.grid(row=2, column=0)

    phoneEntry = tkinter.Entry(container, font=h2)
    phoneEntry.grid(row=2, column=1, sticky='ew')

    # UserLevel
    levelPrompt = tkinter.Label(container, text="Level: ", font=h1, fg="white", bg=blue)
    levelPrompt.grid(row=3, column=0)

    level_selection = StringVar(container)
    level_selection.set("View")
    level_choices = ["View", "Edit"]

    levelSelector = OptionMenu(container, level_selection, *level_choices)
    levelSelector.config(bg=blue, fg="white", padx=5, font=h2)
    levelSelector.grid(row=3, column=1, sticky='ew')

    # Commit Button

    def addUserDB():
        user_name = nameEntry.get()
        user_email = emailEntry.get()
        user_phone = phoneEntry.get()
        user_level = level_selection.get()

        level_dict = {
            "View": 2,
            "Edit": 1
        }

        user_level = int(level_dict[user_level])

        if not check_name(user_name):
            return None
        
        if not check_email(user_email):
            return None

        if len(user_phone) != 11:
                messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                return None

        new_id = sql_select("SELECT UserID FROM Users ORDER BY UserID DESC")[0][0]
        print(new_id)

        system_name = "{}{}".format(user_name.replace(" ", ""), new_id)

        
        confirmation = askyesno(title="Confirmation", message="Are you sure you want to add this user? They will now have access to church records")
        if confirmation:
            try:
                sql_items("INSERT INTO Users (UserName, UserEmail, UserPhone, UserLevel, SystemName, UserPassword) VALUES (%s, %s, %s, %s, %s, %s)", (user_name, user_email, user_phone, user_level, system_name, "ChurchSystem1"))

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was a problem when adding this user. Please try again later")
                return None
            
            messagebox.showinfo("Success", "Successfully added user. \nTheir Username which is used to access the System is: \n{}\nThe password they should use to sign in Initially is ChurchSystem1".format(system_name))
            canvas.yview_moveto(0)
            addUser(frame, canvas)
        

    commitUserButton = tkinter.Button(container, text="Add User", font=h1, fg="white", bg=blue, command=addUserDB)
    commitUserButton.grid(row=4, column=1, sticky='ew')


def editUser(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    userListbox = tkinter.Listbox(container, width=100, font=h2)
    userListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=userListbox.xview)
    userListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=userListbox.yview)
    userListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    def viewEditUser(editFrame):
        # Name
        namePrompt = tkinter.Label(editFrame, text="Name: ", font=h1, fg="white", bg=blue)
        namePrompt.grid(row=0, column=0)

        nameEntry = tkinter.Entry(editFrame, font=h2, width=50)
        nameEntry.grid(row=0, column=1, sticky='ew')

        # Email
        emailPrompt = tkinter.Label(editFrame, text="Email: ", font=h1, fg="white", bg=blue)
        emailPrompt.grid(row=1, column=0)

        emailEntry = tkinter.Entry(editFrame, font=h2)
        emailEntry.grid(row=1, column=1, sticky='ew')

        # Phone
        phonePrompt = tkinter.Label(editFrame, text="Phone: ", font=h1, fg="white", bg=blue)
        phonePrompt.grid(row=2, column=0)

        phoneEntry = tkinter.Entry(editFrame, font=h2)
        phoneEntry.grid(row=2, column=1, sticky='ew')

        # UserLevel
        levelPrompt = tkinter.Label(editFrame, text="Level: ", font=h1, fg="white", bg=blue)
        levelPrompt.grid(row=3, column=0)

        level_selection = StringVar(editFrame)
        level_selection.set("View")
        level_choices = ["View", "Edit"]

        levelSelector = OptionMenu(editFrame, level_selection, *level_choices)
        levelSelector.config(bg=blue, fg="white", padx=5, font=h2)
        levelSelector.grid(row=3, column=1, sticky='ew')

        def editUserDB():
            user_name = nameEntry.get()
            user_email = emailEntry.get()
            user_phone = phoneEntry.get()
            user_level = level_selection.get()

            level_dict = {
                "View": 2,
                "Edit": 1
            }

            user_level = int(level_dict[user_level])

            if not check_name(user_name):
                return None
            
            if not check_email(user_email):
                return None

            if len(user_phone) != 11:
                    messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                    return None

            
            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make changes to this User's details?")
            if confirmation:
                try:
                    sql_items("UPDATE Users SET UserName=%s, UserEmail=%s, UserPhone=%s, UserLevel=%s WHERE UserID=%s", (user_name, user_email, user_phone, user_level, user_id))
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "There was an error updating this User's details. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully changed the Details of User: {}".format(user[5]))
                canvas.yview_moveto(0)
                editUser(frame, canvas)


        commitEditButton = tkinter.Button(editFrame, text="Make Changes", command=editUserDB, font=h1, fg="white", bg=blue)
        commitEditButton.grid(row=4, column=1, sticky='ew', pady=10)

        # Insert Details
        if len(userListbox.get(tkinter.ANCHOR)) == 0:
            return None

        user = user_dict[userListbox.get(tkinter.ANCHOR)]
        user_id = user[0]

        level_dict = {
                "View": 2,
                "Edit": 1
            }

        if user[4] == 1:
            level_selection.set("Edit")
        else:
            level_selection.set("View")

        nameEntry.insert(0, user[1])
        emailEntry.insert(0, user[2])
        phoneEntry.insert(0, user[3])

    editButton = tkinter.Button(container, text="View/Edit User", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditUser(editFrame))
    editButton.grid(row=2, column=0, sticky='w')

    def deleteUserDB():
        if len(userListbox.get(tkinter.ANCHOR)) == 0:
            return None
        
        user = user_dict[userListbox.get(tkinter.ANCHOR)]

        confirmation = askyesno(title="Confirmation", message="Are you sure that you want to delete this User?")
        if confirmation:
            try:
                sql("DELETE FROM Users WHERE UserID={}".format(user[0]))
            except:
                messagebox.showerror("Error", "There was an error deleting this User. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully Deleted User")
            canvas.yview_moveto(0)
            editUser(frame, canvas)


    deleteButton = tkinter.Button(container, text="Delete User", font=h1, bg=blue, fg="white", width=30, command=deleteUserDB)
    deleteButton.grid(row=2, column=0, sticky='e')

    def resetUserPassword():
        if len(userListbox.get(tkinter.ANCHOR)) == 0:
            return None

        member = user_dict[userListbox.get(tkinter.ANCHOR)]

        confirmation = askyesno(title="Confirmation", message="Are you sure you want to reset this User's password to: \nChurchSystem1")
        if confirmation:
            try:
                sql("UPDATE Users SET UserPassword='ChurchSystem1' WHERE UserID={}".format(member[0]))
            except:
                messagebox.showerror("Error", "An error occured when trying to Reset the Password. Please try again later")
                return None
            
            messagebox.showinfo("Success", "Successfully Reset Password of User: {} to \nChurchSystem1".format(member[5]))


    resetPassButton = tkinter.Button(container, text="Reset Password", font=h1, bg=blue, fg="white", width=30, command=resetUserPassword)
    resetPassButton.grid(row=3, column=0, sticky='w')

    user_dict = searchFunctionUser(userListbox, container, 4)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=6,column=0, columnspan=2)

def userOptions(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options

    userAddButton = tkinter.Button(mOptionsFrame, text="Add User", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addUser(restFrame, canvas))
    userAddButton.grid(row=0, column=1, padx=10)

    userEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete User", highlightthickness=0, bd=0, font=h1, bg=blue, fg="white", command=lambda: editUser(restFrame, canvas))
    userEditButton.grid(row=0, column=2, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)