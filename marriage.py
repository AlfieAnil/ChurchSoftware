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
from search_func import searchFunctionMarriage


def addMarriage(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    # Groom Bridge Names

    groomNamePrompt = tkinter.Label(container, text="Groom Name: ", fg="white", bg=blue, font=h1)
    groomNamePrompt.grid(row=0, column=0, sticky='w')

    groomNameEntry = tkinter.Entry(container, font=h2)
    groomNameEntry.grid(row=0, column=1, sticky='ew')

    brideNamePrompt = tkinter.Label(container, text="Bride Name: ", fg="white", bg=blue, font=h1)
    brideNamePrompt.grid(row=1, column=0, sticky='w')

    brideNameEntry = tkinter.Entry(container, font=h2)
    brideNameEntry.grid(row=1, column=1, sticky='ew')
    

    # Status Selection
    status_selection = StringVar(container)
    status_selection.set("Received")
    status_choices = ["Request Received", "Interview Attended", "Marriage Course Attended", "Document sent to Registrar"]

    statusPrompt = tkinter.Label(container, text="Status: ", fg="white", bg=blue, font=h1)
    statusPrompt.grid(row=2, column=0, pady=10, sticky='w')

    statusSelector = OptionMenu(container, status_selection, *status_choices)
    statusSelector.config(bg=blue, fg="white", padx=5, font=h2)
    statusSelector.grid(row=2, column=1, sticky='ew')

    # Permission
    permissionPrompt = tkinter.Label(container, text="Permission: ", fg="white", bg=blue, font=h1)
    permissionPrompt.grid(row=3, column=0, sticky='w')

    permission_selection = StringVar(container)
    permission_selection.set("Yes")
    permission_choices = ["Yes", "No", "Requested", "Received", "Not Required"]
    
    permissionSelector = OptionMenu(container, permission_selection, *permission_choices)
    permissionSelector.config(bg=blue, fg="white", padx=5, font=h2)
    permissionSelector.grid(row=3, column=1, sticky='ew')





    # Church select
    churchPrompt = tkinter.Label(container, text="Church: ", bg=blue, fg="white", font=h1)
    churchPrompt.grid(row=6, column=0, pady=10, sticky='w')

    church_selection = StringVar(container)
    church_dictionary = church_dict_glob_id
    church_list = []
    # churches = sql_select("SELECT * FROM Churches")

    for church in church_dictionary:
        church_list.append(church)

    print(church_dictionary)

    church_selection.set(church_list[0])
    church_choices = church_list
    churchSelector = OptionMenu(container, church_selection, *church_choices)
    churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
    churchSelector.grid(row=6, column=1, sticky='ew')

    # Date of Marriage
    datePrompt = tkinter.Label(container, text="Date of Marriage: ", font=h1, bg=blue, fg="white")
    datePrompt.grid(row=4, column=0, pady=10, sticky='w')

    dateFrame = tkinter.Frame(container, bg=blue)
    dateFrame.grid(row=4, column=1, sticky='ew')

    dateEntry = tkinter.StringVar()
    
    def switchDateState():
        if notBool.get() == 1:
            cal['state'] = 'disabled'
        else:
            cal['state'] = 'normal'

    notBool = tkinter.IntVar()
    checkBool = tkinter.Checkbutton(dateFrame, text="Undetermined", font=h2, variable=notBool, onvalue=1, offvalue=0, command=switchDateState)
    checkBool.grid(row=0, column=0, padx=(0, 10))
    checkBool['bg'] = blue

    cal = DateEntry(dateFrame, font=h2, selectmode='day', textvariable=dateEntry, date_pattern='dd/MM/yyyy')
    cal.grid(row=0, column=1, sticky='ew')

    dateFrame.columnconfigure(1, weight=1)

    timePrompt = tkinter.Label(container, text="Time of Marriage (HH/MM) :", font=h1, fg="white", bg=blue)
    timePrompt.grid(row=5, column=0, sticky='w')

    timeFrame = tkinter.Frame(container, bg=blue)
    timeFrame.grid(row=5, column=1, sticky='ew')

    def switchTimeState():
        if notTBool.get() == 1:
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'
        
        else:
            hour_select_first['state'] = 'readonly'
            minute_select_first['state'] = 'readonly'

    notTBool = tkinter.IntVar()
    checkTBool = tkinter.Checkbutton(timeFrame, text="Undetermined", font=h2, variable=notTBool, onvalue=1, offvalue=0, command=switchTimeState)
    checkTBool.grid(row=0, column=0, padx=(0, 10))
    checkTBool['bg'] = blue

    timeContainer = tkinter.Frame(timeFrame, bg=blue)
    timeContainer.grid(row=0, column=1)

    hour_select_first_selection = tkinter.StringVar()
    hour_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable = hour_select_first_selection, from_=00, to=23, format="%02.0f", width=5, font=h2)
    hour_select_first.grid(row=0, column=1)

    colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=2)

    minutes_list = ['00', '15', '30', '45']
    minute_select_first_selection = tkinter.StringVar()
    minute_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_first_selection, values=minutes_list, width=5, font=h2)
    minute_select_first.grid(row=0, column=3)


    # Clergy Selection
    clergyPrompt = tkinter.Label(container, text="Clergy Member: ", font=h1, fg="white", bg=blue)
    clergyPrompt.grid(row=7, column=0, sticky='w')

    clergyEntry = tkinter.Entry(container, font=h2)
    clergyEntry.grid(row=7, column=1, sticky='ew')

    # Contact Number
    contactNumberPrompt = tkinter.Label(container, text="Contact Number: ", font=h1, fg="white", bg=blue)
    contactNumberPrompt.grid(row=8, column=0, sticky='w')

    contactNumberEntry = tkinter.Entry(container, font=h2)
    contactNumberEntry.grid(row=8, column=1, sticky='ew')

    # Notes
    notesPrompt = tkinter.Label(container, text="Notes: ", font=h1, fg="white", bg=blue)
    notesPrompt.grid(row=9, column=0, sticky='w')

    notesEntry = tkinter.Text(container, font=h2)
    notesEntry.grid(row=9, column=1, sticky='ew')

    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
    notesEntry['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=9, column=2, sticky='wns')

    # AddButton
    def commitMarriageDB():
        groom_name = groomNameEntry.get()
        bride_name = brideNameEntry.get()
        permission = permission_selection.get()
        status = status_selection.get()
        church_id = church_selection.get()
        dateMarriage = dateEntry.get()
        # Time
        time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

        if notTBool.get() == 1:
            time = "Undetermined"

        clergy_member = clergyEntry.get()
        contact_number = contactNumberEntry.get()
        notes = notesEntry.get('1.0', 'end')

        if not check_name(groom_name):
            return None

        if not check_name(bride_name):
            return None
        
        if len(clergy_member.split()) < 2:
            messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
            return False

        # Date Check
        if notBool.get() == 1:
            dateMarriage = "Undetermined"
        else:
            date_split = dateMarriage.split('/')

            date_split = [int(x) for x in date_split]

            if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                messagebox.showerror("Error", "Ensure that the date is in the future")
                return None

        if len(contact_number) != 11:
            messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
            return None


        confirmation = askyesno(title="Confirmation", message="Are you sure you want to add this Marriage?")
        if confirmation:
            try:
                sql_items("INSERT INTO Marriage (GroomName, BrideName, Status, Permission, ChurchID, DateOfMarriage, TimeOfMarriage, ClergyID, ContactNumber, Notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (groom_name, bride_name, status, permission, church_dict_glob_id[church_id], dateMarriage, str(time), clergy_member, contact_number, notes))

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error adding the Marriage. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully added Marriage")
            canvas.yview_moveto(0)
            addMarriage(frame, canvas)
        


    commitMarriageButton = tkinter.Button(container, text="Add Marriage", font=h1, fg="white", bg=blue, command=commitMarriageDB)
    commitMarriageButton.grid(row=10, column=1, sticky='ew')


def editMarriage(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    marriageListbox = tkinter.Listbox(container, width=100, font=h2)
    marriageListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=marriageListbox.xview)
    marriageListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=marriageListbox.yview)
    marriageListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    def viewEditMarriage(editFrame):
        if len(marriageListbox.get(tkinter.ANCHOR)) == 0:
            return None

        # Groom Bridge Names

        groomNamePrompt = tkinter.Label(editFrame, text="Groom Name: ", fg="white", bg=blue, font=h1)
        groomNamePrompt.grid(row=0, column=0, sticky='w')

        groomNameEntry = tkinter.Entry(editFrame, font=h2)
        groomNameEntry.grid(row=0, column=1, sticky='ew')

        brideNamePrompt = tkinter.Label(editFrame, text="Bride Name: ", fg="white", bg=blue, font=h1)
        brideNamePrompt.grid(row=1, column=0, sticky='w')

        brideNameEntry = tkinter.Entry(editFrame, font=h2)
        brideNameEntry.grid(row=1, column=1, sticky='ew')
        

        # Status Selection
        status_selection = StringVar(editFrame)
        status_selection.set("Received")
        status_choices = ["Request Received", "Interview Attended", "Marriage Course Attended", "Document sent to Registrar"]

        statusPrompt = tkinter.Label(editFrame, text="Status: ", fg="white", bg=blue, font=h1)
        statusPrompt.grid(row=2, column=0, pady=10, sticky='w')

        statusSelector = OptionMenu(editFrame, status_selection, *status_choices)
        statusSelector.config(bg=blue, fg="white", padx=5, font=h2)
        statusSelector.grid(row=2, column=1, sticky='ew')

        # Permission
        permissionPrompt = tkinter.Label(editFrame, text="Permission: ", fg="white", bg=blue, font=h1)
        permissionPrompt.grid(row=3, column=0, sticky='w')

        permission_selection = StringVar(editFrame)
        permission_selection.set("Yes")
        permission_choices = ["Yes", "No", "Requested", "Received", "Not Required"]
        
        permissionSelector = OptionMenu(editFrame, permission_selection, *permission_choices)
        permissionSelector.config(bg=blue, fg="white", padx=5, font=h2)
        permissionSelector.grid(row=3, column=1, sticky='ew')





        # Church select
        churchPrompt = tkinter.Label(editFrame, text="Church: ", bg=blue, fg="white", font=h1)
        churchPrompt.grid(row=6, column=0, pady=10, sticky='w')

        church_selection = StringVar(editFrame)
        church_dictionary = church_dict_glob_id
        church_list = []
        # churches = sql_select("SELECT * FROM Churches")

        for church in church_dictionary:
            church_list.append(church)

        print(church_dictionary)

        church_selection.set(church_list[0])
        church_choices = church_list
        churchSelector = OptionMenu(editFrame, church_selection, *church_choices)
        churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
        churchSelector.grid(row=6, column=1, sticky='ew')

        # Date of Marriage
        datePrompt = tkinter.Label(editFrame, text="Date of Marriage: ", font=h1, bg=blue, fg="white")
        datePrompt.grid(row=4, column=0, pady=10, sticky='w')

        dateFrame = tkinter.Frame(editFrame, bg=blue)
        dateFrame.grid(row=4, column=1, sticky='ew')

        dateEntry = tkinter.StringVar()
        
        def switchDateState():
            if notBool.get() == 1:
                cal['state'] = 'disabled'
            else:
                cal['state'] = 'normal'

        notBool = tkinter.IntVar()
        checkBool = tkinter.Checkbutton(dateFrame, text="Undetermined", font=h2, variable=notBool, onvalue=1, offvalue=0, command=switchDateState)
        checkBool.grid(row=0, column=0, padx=(0, 10))
        checkBool['bg'] = blue

        cal = DateEntry(dateFrame, font=h2, selectmode='day', textvariable=dateEntry, date_pattern='dd/MM/yyyy')
        cal.grid(row=0, column=1, sticky='ew')

        dateFrame.columnconfigure(1, weight=1)

        timePrompt = tkinter.Label(editFrame, text="Time of Marriage (HH/MM) :", font=h1, fg="white", bg=blue)
        timePrompt.grid(row=5, column=0, sticky='w')

        timeFrame = tkinter.Frame(editFrame, bg=blue)
        timeFrame.grid(row=5, column=1, sticky='ew')

        def switchTimeState():
            if notTBool.get() == 1:
                hour_select_first['state'] = 'disabled'
                minute_select_first['state'] = 'disabled'
            
            else:
                hour_select_first['state'] = 'readonly'
                minute_select_first['state'] = 'readonly'

        notTBool = tkinter.IntVar()
        checkTBool = tkinter.Checkbutton(timeFrame, text="Undetermined", font=h2, variable=notTBool, onvalue=1, offvalue=0, command=switchTimeState)
        checkTBool.grid(row=0, column=0, padx=(0, 10))
        checkTBool['bg'] = blue

        timeContainer = tkinter.Frame(timeFrame, bg=blue)
        timeContainer.grid(row=0, column=1)

        hour_select_first_selection = tkinter.StringVar()
        hour_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable = hour_select_first_selection, from_=00, to=23, format="%02.0f", width=5, font=h2)
        hour_select_first.grid(row=0, column=1)

        colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=2)

        minutes_list = ['00', '15', '30', '45']
        minute_select_first_selection = tkinter.StringVar()
        minute_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_first_selection, values=minutes_list, width=5, font=h2)
        minute_select_first.grid(row=0, column=3)


        # Clergy Selection
        clergyPrompt = tkinter.Label(editFrame, text="Clergy Member: ", font=h1, fg="white", bg=blue)
        clergyPrompt.grid(row=7, column=0, sticky='w')

        clergyEntry = tkinter.Entry(editFrame, font=h2)
        clergyEntry.grid(row=7, column=1, sticky='ew')

        # Contact Number
        contactNumberPrompt = tkinter.Label(editFrame, text="Contact Number: ", font=h1, fg="white", bg=blue)
        contactNumberPrompt.grid(row=8, column=0, sticky='w')

        contactNumberEntry = tkinter.Entry(editFrame, font=h2)
        contactNumberEntry.grid(row=8, column=1, sticky='ew')

        # Notes
        notesPrompt = tkinter.Label(editFrame, text="Notes: ", font=h1, fg="white", bg=blue)
        notesPrompt.grid(row=9, column=0, sticky='w')

        notesEntry = tkinter.Text(editFrame, font=h2)
        notesEntry.grid(row=9, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(editFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
        notesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=9, column=2, sticky='wns')

        def editMarriageDB():
            groom_name = groomNameEntry.get()
            bride_name = brideNameEntry.get()
            permission = permission_selection.get()
            status = status_selection.get()
            church_id = church_selection.get()
            dateMarriage = dateEntry.get()
            # Time
            time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

            if notTBool.get() == 1:
                time = "Undetermined"

            clergy_member = clergyEntry.get()
            contact_number = contactNumberEntry.get()
            notes = notesEntry.get('1.0', 'end')

            if not check_name(groom_name):
                return None

            if not check_name(bride_name):
                return None
            
            if len(clergy_member.split()) < 2:
                messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
                return False

            # Date Check
            if notBool.get() == 1:
                dateMarriage = "Undetermined"
            else:
                date_split = dateMarriage.split('/')

                date_split = [int(x) for x in date_split]

                if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                    messagebox.showerror("Error", "Ensure that the date is in the future")
                    return None

            if len(contact_number) != 11:
                messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                return None


            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make changes this Marriage?")
            if confirmation:
                try:
                     sql_items("UPDATE Marriage SET GroomName=%s, BrideName=%s, Status=%s, Permission=%s, ChurchID=%s, DateOfMarriage=%s, TimeOfMarriage=%s, ClergyID=%s, ContactNumber=%s, Notes=%s WHERE MarriageID=%s", (groom_name, bride_name, status, permission, church_dict_glob_id[church_id], dateMarriage, str(time), clergy_member, contact_number, notes, marriage_id))
                except:
                    messagebox.showerror("Error", "There was an error making changes to this Marriage record. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully made changes to Marriage Record")
                canvas.yview_moveto(0)
                editMarriage(frame, canvas)

        
        confirmMarriageEditsButton = tkinter.Button(editFrame, text="Make Changes", font=h1, bg=blue, fg="white", command=editMarriageDB)
        confirmMarriageEditsButton.grid(row=10, column=1, sticky='ew')

        if userlevel == 2:
            confirmMarriageEditsButton.grid_forget()

        # Insert Details

        marriageListbox['state'] = 'disabled'
        selected_marriage = marriageListbox.get(tkinter.ANCHOR)
        selected_marriage = marriage_dict[selected_marriage]
        marriage_id = selected_marriage[0]

        groomNameEntry.insert(0, selected_marriage[1])
        brideNameEntry.insert(0, selected_marriage[2])

        status_selection.set(selected_marriage[3])
        permission_selection.set(selected_marriage[4])

        church_selection.set(church_dict_glob[selected_marriage[5]])

        # date
        if selected_marriage[6] == "Undetermined":
            checkBool.select()
            cal['state'] = 'disabled'
        
        else:
            dateEntry.set(selected_marriage[6])

        # Time
        if selected_marriage[7] == "Undetermined":
            checkTBool.select()
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'

        else:
            hour = selected_marriage[7][0:2]
            minute = selected_marriage[7][3:5]
            hour_select_first_selection.set(hour)
            minute_select_first_selection.set(minute)

        clergyEntry.insert(0, selected_marriage[8])

        contactNumberEntry.insert(0, selected_marriage[9])

        notesEntry.insert('end', selected_marriage[10])

        # Block if userlevel = 2
        if userlevel == 2:
            groomNameEntry['state'] = 'disabled'
            brideNameEntry['state'] = 'disabled'
            statusSelector['bg'] = "white"
            statusSelector['state'] = 'disabled'
            permissionSelector['bg'] = "white"
            permissionSelector['state'] = 'disabled'
            churchSelector['bg'] = "white"
            churchSelector['state'] = 'disabled'
            cal['state'] = 'disabled'
            checkBool['bg'] = "white"
            checkBool['state'] = 'disabled'
            checkTBool['bg'] = "white"
            checkTBool['state'] = 'disabled'
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'
            clergyEntry['state'] = 'disabled'
            contactNumberEntry['state'] = 'disabled'
            notesEntry['state'] = 'disabled'

            if notBool.get() == 1:
                cal.grid_forget()

        

    if userlevel == 1 or userlevel == 3:
        editButton = tkinter.Button(container, text="View/Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditMarriage(editFrame))
        editButton.grid(row=2, column=0, sticky='w')
    else:
        editButton = tkinter.Button(container, text="View Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditMarriage(editFrame))
        editButton.grid(row=2, column=0, sticky='w')

    def deleteMarriageDB():
        marriage = marriageListbox.get(tkinter.ANCHOR)
        if len(marriage) == 0:
            return None
        
        marriage_id = marriage_dict[marriage][0]

        try:
            sql("DELETE FROM Marriage WHERE MarriageID={}".format(marriage_id))
        except:
            messagebox.showerror("Error", "There was an error deleting this marriage. Please try again later")
            return None
        
        messagebox.showinfo("Success", "Successfully deleted Marriage record from Database")
        editMarriage(frame, canvas)

    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Marriage", font=h1, bg=blue, fg="white", width=30, command=deleteMarriageDB)
        deleteButton.grid(row=2, column=0, sticky='e')

    marriage_dict = searchFunctionMarriage(marriageListbox, container, 3)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=6,column=0, columnspan=2)


def marriageOptions(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options
    if userlevel == 1 or userlevel == 3:
        marriageAddButton = tkinter.Button(mOptionsFrame, text="Add Marriage", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addMarriage(restFrame, canvas))
        marriageAddButton.grid(row=0, column=1, padx=10)

    if userlevel == 1 or userlevel == 3:
        marriageEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete Marriage", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editMarriage(restFrame, canvas, userlevel))
        marriageEditButton.grid(row=0, column=2, padx=10)
    else:
        marriageEditButton = tkinter.Button(mOptionsFrame, text="View Marriages", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editMarriage(restFrame, canvas, userlevel))
        marriageEditButton.grid(row=0, column=2, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)