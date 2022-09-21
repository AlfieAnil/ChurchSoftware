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
from members_class import *
from search_func import searchFunctionRoles

def roleAdd(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    roleNamePrompt = tkinter.Label(container, text="Role Name: ", bg=blue, fg="white", font=h1)
    roleNamePrompt.grid(row=0, column=0, sticky='w', padx=5)

    roleNameEntry = tkinter.Entry(container, font=h2)
    roleNameEntry.grid(row=0, column=1, stick='ew')

    roleNotesPrompt = tkinter.Label(container, text="Description: ", font=h1, bg=blue, fg="white")
    roleNotesPrompt.grid(row=1, column=0, padx=5)

    roleNotesEntry = tkinter.Text(container, font=h2)
    roleNotesEntry.grid(row=1, column=1, sticky='ew')

    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=roleNotesEntry.yview, bg=blue)
    roleNotesEntry['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=1, column=2, sticky='wns')

    def roleAddDB():
        role_name = roleNameEntry.get()
        role_desc = roleNotesEntry.get('1.0', 'end')

        if len(role_name) == 0:
            messagebox.showerror("Error", "Please enter a Role Name")
            return None

        try:
            sql_items("INSERT INTO Roles (RoleName, RoleDescription) VALUES (%s, %s)", (role_name, role_desc))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "There was a problem adding this Role to the database. Please try again later")
            return None
        
        messagebox.showinfo("Sucess", "Successfully added Role to Database")
        roleAdd(frame)

    roleAddButton = tkinter.Button(container, text="Add Role", fg="white", bg=blue, font=h2, command=roleAddDB)
    roleAddButton.grid(row=3, column=1, sticky='ew')


def editRoles(frame, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    h0 = tkFont.Font(family='Helvetica', size=14, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    selectPrompt = tkinter.Label(container, text="Select Family to Edit/Delete", fg="white", bg=blue, font=h0)
    selectPrompt.grid(row=0, column=0, sticky='ew')

    roleSelect = tkinter.Listbox(container, width=110, height=15, font=h2)
    roleSelect.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=roleSelect.xview)
    roleSelect['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=roleSelect.yview)
    roleSelect['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    def editRoleArea(editFrame):

        if len(roleSelect.get(tkinter.ANCHOR)) == 0:
            return None

        role_id = roleSelect.get(tkinter.ANCHOR)

        role_id = role_id[role_id.find(": ")+1:role_id.find("|")]

        roleNamePrompt = tkinter.Label(editFrame, text="Role Name: ", bg=blue, fg="white", font=h1)
        roleNamePrompt.grid(row=0, column=0, sticky='w', padx=5)

        roleNameEntry = tkinter.Entry(editFrame, font=h2)
        roleNameEntry.grid(row=0, column=1, stick='ew')

        roleNotesPrompt = tkinter.Label(editFrame, text="Description: ", font=h1, bg=blue, fg="white")
        roleNotesPrompt.grid(row=1, column=0, padx=5)

        roleNotesEntry = tkinter.Text(editFrame, font=h2)
        roleNotesEntry.grid(row=1, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(editFrame, orient=tkinter.VERTICAL, command=roleNotesEntry.yview, bg=blue)
        roleNotesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=1, column=2, sticky='wns')

        def makeRoleEdits():
            role_name = roleNameEntry.get()
            role_desc = roleNotesEntry.get('1.0', 'end')

            if len(role_name) == 0:
                messagebox.showerror("Error", "Please insert a role name")
                return None

            try:
                sql_items("UPDATE Roles SET RoleName=%s, RoleDescription=%s WHERE RoleID=%s", (role_name, role_desc, role_id))
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error making changes to this role. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully made changes to this role")
            editRoles(frame)

        confirmEditsButton = tkinter.Button(editFrame, text="Make Changes", fg="white", bg=blue, font=h1, command=makeRoleEdits)
        confirmEditsButton.grid(row=2, column=1, sticky='ew')

        if userlevel == 2:
            confirmEditsButton.grid_forget()

        # Insert details
        role_dets = sql_select("SELECT RoleName, RoleDescription FROM Roles WHERE RoleID={}".format(role_id))

        for rolename, roledescription in role_dets:
            roleNameEntry.insert('end', rolename)
            roleNotesEntry.insert('end', roledescription)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=5, column=0)

    if userlevel == 1 or userlevel == 3:
        editButton = tkinter.Button(container, text="View/Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: editRoleArea(editFrame))
        editButton.grid(row=3, column=0, sticky='w')
    
    else:
        editButton = tkinter.Button(container, text="View Details", font=h1, bg=blue, fg="white", width=30, command=lambda: editRoleArea(editFrame))
        editButton.grid(row=3, column=0, sticky='w')

    def deleteRoleDB():
        role_id = roleSelect.get(tkinter.ANCHOR)

        role_id = role_id[role_id.find(": ")+1:role_id.find("|")]

        confirmation = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete this Role?")
        if confirmation:
            try:
                sql("DELETE FROM Roles WHERE RoleID={}".format(role_id))
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error deleting this role. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully deleted role")
            editRoles(frame)

    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Role", font=h1, bg=blue, fg="white", width=30, command=deleteRoleDB)
        deleteButton.grid(row=3, column=0, sticky='e')

    searchFunctionRoles(roleSelect, container, 4)

    
    


def roleOptionsArea(frame, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options
    if userlevel == 1 or userlevel == 3:
        roleAddButton = tkinter.Button(mOptionsFrame, text="Add Role", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: roleAdd(restFrame))
        roleAddButton.grid(row=0, column=1, padx=10)


        roleEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete Role", highlightthickness=0, bd=0, fg="white", bg=blue, font=h1, command=lambda: editRoles(restFrame, userlevel))
        roleEditButton.grid(row=0, column=2, padx=10)

    else:
        roleEditButton = tkinter.Button(mOptionsFrame, text="View Roles", highlightthickness=0, bd=0, fg="white", bg=blue, font=h1, command=lambda: editRoles(restFrame, userlevel))
        roleEditButton.grid(row=0, column=2, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)
    