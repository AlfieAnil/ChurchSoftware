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
from search_func import searchFunctionBaptism


def addBaptism(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    # Child Name 
    childNamePrompt = tkinter.Label(container, text="Child Name: ", fg="white", bg=blue, font=h1)
    childNamePrompt.grid(row=0, column=0)

    childNameEntry = tkinter.Entry(container, font=h2)
    childNameEntry.grid(row=0, column=1, sticky='ew')

    # Status Selection
    status_selection = StringVar(container)
    status_selection.set("Received")
    status_choices = ["Received", "Passed to Clergy Member", "Course Started", "Date Confirmed", "Certificate Issued", "Entered in Register"]

    statusPrompt = tkinter.Label(container, text="Status: ", fg="white", bg=blue, font=h1)
    statusPrompt.grid(row=1, column=0, pady=10)

    statusSelector = OptionMenu(container, status_selection, *status_choices)
    statusSelector.config(bg=blue, fg="white", padx=5, font=h2)
    statusSelector.grid(row=1, column=1, sticky='ew')

    # Church select
    churchPrompt = tkinter.Label(container, text="Church: ", bg=blue, fg="white", font=h1)
    churchPrompt.grid(row=4, column=0, pady=10)

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
    churchSelector.grid(row=4, column=1, sticky='ew')

    # Date of Baptism
    datePrompt = tkinter.Label(container, text="Date of Baptism: ", font=h1, bg=blue, fg="white")
    datePrompt.grid(row=2, column=0, pady=10)

    dateFrame = tkinter.Frame(container, bg=blue)
    dateFrame.grid(row=2, column=1, sticky='ew')

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

    timePrompt = tkinter.Label(container, text="Time of Baptism (HH/MM) :", font=h1, fg="white", bg=blue)
    timePrompt.grid(row=3, column=0)

    timeFrame = tkinter.Frame(container, bg=blue)
    timeFrame.grid(row=3, column=1, sticky='ew')

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
    clergyPrompt.grid(row=5, column=0)

    clergyEntry = tkinter.Entry(container, font=h2)
    clergyEntry.grid(row=5, column=1, sticky='ew')

    # Contact Number
    contactNumberPrompt = tkinter.Label(container, text="Contact Number: ", font=h1, fg="white", bg=blue)
    contactNumberPrompt.grid(row=6, column=0)

    contactNumberEntry = tkinter.Entry(container, font=h2)
    contactNumberEntry.grid(row=6, column=1, sticky='ew')

    # Notes
    notesPrompt = tkinter.Label(container, text="Notes: ", font=h1, fg="white", bg=blue)
    notesPrompt.grid(row=7, column=0)

    notesEntry = tkinter.Text(container, font=h2)
    notesEntry.grid(row=7, column=1, sticky='ew')

    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
    notesEntry['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=7, column=2, sticky='wns')

    # AddButton
    def commitBaptismDB():
        child_name = childNameEntry.get()
        status = status_selection.get()
        church_id = church_selection.get()
        dateBaptism = dateEntry.get()
        # Time
        time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

        if notTBool.get() == 1:
            time = "Undetermined"

        clergy_member = clergyEntry.get()
        contact_number = contactNumberEntry.get()
        notes = notesEntry.get('1.0', 'end')

        if not check_name(child_name):
            return None
        
        if len(clergy_member.split()) < 2:
            messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
            return False

        # Date Check
        if notBool.get() == 1:
            dateBaptism = "Undetermined"
        else:
            date_split = dateBaptism.split('/')

            date_split = [int(x) for x in date_split]

            if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                messagebox.showerror("Error", "Ensure that the date is in the future")
                return None

        if len(contact_number) != 11:
            messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
            return None


        confirmation = askyesno(title="Confirmation", message="Are you sure you want to add this Baptism?")
        if confirmation:
            try:
                sql_items("INSERT INTO Baptism (ChildName, Status, ChurchID, DateOfBaptism, TimeOfBaptism, ClergyID, ContactNumber, Notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (child_name, status, church_dict_glob_id[church_id], dateBaptism, str(time), clergy_member, contact_number, notes))

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error adding the Baptism. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully added Baptism")
            canvas.yview_moveto(0)
            addBaptism(frame, canvas)
        


    commitBaptismButton = tkinter.Button(container, text="Add Baptism", font=h1, fg="white", bg=blue, command=commitBaptismDB)
    commitBaptismButton.grid(row=8, column=1, sticky='ew')



    

def editBaptism(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    bapListbox = tkinter.Listbox(container, width=100, font=h2)
    bapListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=bapListbox.xview)
    bapListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=bapListbox.yview)
    bapListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    def viewEditBaptism(editFrame):
        
        if len(bapListbox.get(tkinter.ANCHOR)) == 0:
            return None

        # Child Name 
        childNamePrompt = tkinter.Label(editFrame, text="Child Name: ", fg="white", bg=blue, font=h1)
        childNamePrompt.grid(row=0, column=0)

        childNameEntry = tkinter.Entry(editFrame, font=h2)
        childNameEntry.grid(row=0, column=1, sticky='ew')

        # Status Selection
        status_selection = StringVar(editFrame)
        status_selection.set("Received")
        status_choices = ["Received", "Passed to Clergy Member", "Course Started", "Date Confirmed", "Certificate Issued", "Entered in Register"]

        statusPrompt = tkinter.Label(editFrame, text="Status: ", fg="white", bg=blue, font=h1)
        statusPrompt.grid(row=1, column=0, pady=10)

        statusSelector = OptionMenu(editFrame, status_selection, *status_choices)
        statusSelector.config(bg=blue, fg="white", padx=5, font=h2)
        statusSelector.grid(row=1, column=1, sticky='ew')

        # Church select
        churchPrompt = tkinter.Label(editFrame, text="Church: ", bg=blue, fg="white", font=h1)
        churchPrompt.grid(row=4, column=0, pady=10)

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
        churchSelector.grid(row=4, column=1, sticky='ew')

        # Date of Baptism
        datePrompt = tkinter.Label(editFrame, text="Date of Baptism: ", font=h1, bg=blue, fg="white")
        datePrompt.grid(row=2, column=0, pady=10)

        dateFrame = tkinter.Frame(editFrame, bg=blue)
        dateFrame.grid(row=2, column=1, sticky='ew')

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

        timePrompt = tkinter.Label(editFrame, text="Time of Baptism (HH/MM) :", font=h1, fg="white", bg=blue)
        timePrompt.grid(row=3, column=0)

        timeFrame = tkinter.Frame(editFrame, bg=blue)
        timeFrame.grid(row=3, column=1, sticky='ew')

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
        clergyPrompt.grid(row=5, column=0)

        clergyEntry = tkinter.Entry(editFrame, font=h2)
        clergyEntry.grid(row=5, column=1, sticky='ew')

        # Contact Number
        contactNumberPrompt = tkinter.Label(editFrame, text="Contact Number: ", font=h1, fg="white", bg=blue)
        contactNumberPrompt.grid(row=6, column=0)

        contactNumberEntry = tkinter.Entry(editFrame, font=h2)
        contactNumberEntry.grid(row=6, column=1, sticky='ew')

        # Notes
        notesPrompt = tkinter.Label(editFrame, text="Notes: ", font=h1, fg="white", bg=blue)
        notesPrompt.grid(row=7, column=0)

        notesEntry = tkinter.Text(editFrame, font=h2)
        notesEntry.grid(row=7, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(editFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
        notesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=7, column=2, sticky='wns')

        def editBaptismDB():
            child_name = childNameEntry.get()
            status = status_selection.get()
            church_id = church_selection.get()
            dateBaptism = dateEntry.get()
            # Time
            time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

            if notTBool.get() == 1:
                time = "Undetermined"

            clergy_member = clergyEntry.get()
            contact_number = contactNumberEntry.get()
            notes = notesEntry.get('1.0', 'end')

            if not check_name(child_name):
                return None
            
            if len(clergy_member.split()) < 2:
                messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
                return False

            # Date Check
            if notBool.get() == 1:
                dateBaptism = "Undetermined"
            else:
                date_split = dateBaptism.split('/')

                date_split = [int(x) for x in date_split]

                if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                    messagebox.showerror("Error", "Ensure that the date is in the future")
                    return None

            if len(contact_number) != 11:
                messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                return None


            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make changes to this Baptism Record?")
            
            if confirmation:
                try:
                    sql_items("UPDATE Baptism SET ChildName=%s, Status=%s, ChurchID=%s, DateOfBaptism=%s, TimeOfBaptism=%s, ClergyID=%s, ContactNumber=%s, Notes=%s WHERE BaptismID=%s", (child_name, status, church_dict_glob_id[church_id], dateBaptism, str(time), clergy_member, contact_number, notes, baptism_id))
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "There was a problem updating this Baptism record. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully updated Baptism record details")
                canvas.yview_moveto(0)
                editBaptism(frame, canvas)
                
        
        confirmBaptismEditsButton = tkinter.Button(editFrame, text="Make Changes", font=h1, bg=blue, fg="white", command=editBaptismDB)
        confirmBaptismEditsButton.grid(row=8, column=1, sticky='ew')

        if userlevel == 2:
            confirmBaptismEditsButton.grid_forget()

        # Insert Details
        bapListbox['state'] = 'disabled'
        selected_baptism = bapListbox.get(tkinter.ANCHOR)
        selected_baptism = baptism_dict[selected_baptism]
        baptism_id = selected_baptism[0]
        print(selected_baptism)

        childNameEntry.insert(0, selected_baptism[1])

        status_selection.set(selected_baptism[2])

        church_selection.set(church_dict_glob[selected_baptism[3]])

        # Date
        if selected_baptism[4] == "Undetermined":
            checkBool.select()
            cal['state'] = 'disabled'
        
        else:
            dateEntry.set(selected_baptism[4])

        # Time
        if selected_baptism[5] == "Undetermined":
            checkTBool.select()
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'

        else:
            hour = selected_baptism[5][0:2]
            minute = selected_baptism[5][3:5]
            hour_select_first_selection.set(hour)
            minute_select_first_selection.set(minute)

        clergyEntry.insert(0, selected_baptism[6])

        contactNumberEntry.insert(0, selected_baptism[7])

        notesEntry.insert('end', selected_baptism[8])

        # Block if level = 2
        if userlevel == 2:
            childNameEntry['state'] = 'disabled'
            statusSelector['state'] = 'disabled'
            statusSelector['bg'] = "white"
            churchSelector['state'] = 'disabled'
            churchSelector['bg'] = "white"
            checkBool['bg'] = "white"
            checkBool['state'] = 'disabled'
            cal['state'] = 'disabled'
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
        editButton = tkinter.Button(container, text="View/Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditBaptism(editFrame))
        editButton.grid(row=2, column=0, sticky='w')

    else:
        editButton = tkinter.Button(container, text="View Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditBaptism(editFrame))
        editButton.grid(row=2, column=0, sticky='w')

    def deleteBaptismDB():
        selected_baptism = bapListbox.get(tkinter.ANCHOR)
        selected_baptism = baptism_dict[selected_baptism][0]

        confirmation = askyesno(title="Confirmation", message="Are you sure you want to delete the selected Baptism Record?")
        if confirmation:
            try:
                sql("DELETE FROM Baptism WHERE BaptismID={}".format(selected_baptism))
            except:
                messagebox.showerror("Error", "An error occured when deleting the baptism. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully deleted Baptism Record")
            canvas.yview_moveto(0)
            editBaptism(frame, canvas) 

    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Baptism", font=h1, bg=blue, fg="white", width=30, command=deleteBaptismDB)
        deleteButton.grid(row=2, column=0, sticky='e')

    baptism_dict = searchFunctionBaptism(bapListbox, container, 3)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=6,column=0, columnspan=2)


def baptismOptions(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options
    if userlevel == 1 or userlevel == 3:
        baptismAddButton = tkinter.Button(mOptionsFrame, text="Add Baptism", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addBaptism(restFrame, canvas))
        baptismAddButton.grid(row=0, column=1, padx=10)

    if userlevel == 1 or userlevel == 3:
            
        baptismEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete Baptisms", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editBaptism(restFrame, canvas, userlevel))
        baptismEditButton.grid(row=0, column=2, padx=10)
    else:
        baptismEditButton = tkinter.Button(mOptionsFrame, text="View Baptisms", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editBaptism(restFrame, canvas, userlevel))
        baptismEditButton.grid(row=0, column=2, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)