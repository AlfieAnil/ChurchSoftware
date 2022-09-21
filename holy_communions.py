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
from search_func import searchFunctionHC


def addHC(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    # Child Name 
    comNamePrompt = tkinter.Label(container, text="Communicant Name: ", fg="white", bg=blue, font=h1)
    comNamePrompt.grid(row=0, column=0)

    comNameEntry = tkinter.Entry(container, font=h2)
    comNameEntry.grid(row=0, column=1, sticky='ew')

    # Status Selection
    status_selection = StringVar(container)
    status_selection.set("Application Receieved")
    status_choices = ["Application Received", "Baptism Confirmed", "Completed Course", "Certificate Issued"]

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

    # Date of Holy Communion
    datePrompt = tkinter.Label(container, text="Date of Holy Communion: ", font=h1, bg=blue, fg="white")
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

    timePrompt = tkinter.Label(container, text="Time of Holy Communion (HH/MM) :", font=h1, fg="white", bg=blue)
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
    def commitHolyCommunionDB():
        communicant_name = comNameEntry.get()
        status = status_selection.get()
        church_id = church_selection.get()
        dateHC = dateEntry.get()
        # Time
        time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

        if notTBool.get() == 1:
            time = "Undetermined"

        clergy_member = clergyEntry.get()
        contact_number = contactNumberEntry.get()
        notes = notesEntry.get('1.0', 'end')

        if not check_name(communicant_name):
            return None
        
        if len(clergy_member.split()) < 2:
            messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
            return False

        # Date Check
        if notBool.get() == 1:
            dateHC = "Undetermined"
        else:
            date_split = dateHC.split('/')

            date_split = [int(x) for x in date_split]

            if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                messagebox.showerror("Error", "Ensure that the date is in the future")
                return None

        if len(contact_number) != 11:
            messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
            return None


        confirmation = askyesno(title="Confirmation", message="Are you sure you want to add this Holy Communion?")
        if confirmation:
            try:
                sql_items("INSERT INTO HolyCommunion (CommunicantName, Status, ChurchID, DateOfHC, TimeOfHC, ClergyID, ContactNumber, Notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (communicant_name, status, church_dict_glob_id[church_id], dateHC, str(time), clergy_member, contact_number, notes))

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error adding the Holy Communion. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully added Holy Communion")
            canvas.yview_moveto(0)
            addHC(frame, canvas)
        


    commitHCButton = tkinter.Button(container, text="Add Holy Communion", font=h1, fg="white", bg=blue, command=commitHolyCommunionDB)
    commitHCButton.grid(row=8, column=1, sticky='ew')




def editHC(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    hcListbox = tkinter.Listbox(container, width=100, font=h2)
    hcListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=hcListbox.xview)
    hcListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=hcListbox.yview)
    hcListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    def viewEditHC(editFrame):
        
        if len(hcListbox.get(tkinter.ANCHOR)) == 0:
            return None

        # Child Name 
        comNamePrompt = tkinter.Label(editFrame, text="Child Name: ", fg="white", bg=blue, font=h1)
        comNamePrompt.grid(row=0, column=0)

        comNameEntry = tkinter.Entry(editFrame, font=h2)
        comNameEntry.grid(row=0, column=1, sticky='ew')

        # Status Selection
        status_selection = StringVar(editFrame)
        status_selection.set("Application Received")
        status_choices = ["Application Received", "Baptism Confirmed", "Completed Course", "Certificate Issued"]

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

        # Date of HC
        datePrompt = tkinter.Label(editFrame, text="Date of Holy Communion: ", font=h1, bg=blue, fg="white")
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

        timePrompt = tkinter.Label(editFrame, text="Time of Holy Communion (HH/MM) :", font=h1, fg="white", bg=blue)
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

        def editHCDB():
            com_name = comNameEntry.get()
            status = status_selection.get()
            church_id = church_selection.get()
            dateHC = dateEntry.get()
            # Time
            time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

            if notTBool.get() == 1:
                time = "Undetermined"

            clergy_member = clergyEntry.get()
            contact_number = contactNumberEntry.get()
            notes = notesEntry.get('1.0', 'end')

            if not check_name(com_name):
                return None
            
            if len(clergy_member.split()) < 2:
                messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
                return False

            # Date Check
            if notBool.get() == 1:
                dateHC = "Undetermined"
            else:
                date_split = dateHC.split('/')

                date_split = [int(x) for x in date_split]

                if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                    messagebox.showerror("Error", "Ensure that the date is in the future")
                    return None

            if len(contact_number) != 11:
                messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                return None


            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make changes to this Holy Communion Record?")
            
            if confirmation:
                try:
                    sql_items("UPDATE HolyCommunion SET CommunicantName=%s, Status=%s, ChurchID=%s, DateOfHC=%s, TimeOfHC=%s, ClergyID=%s, ContactNumber=%s, Notes=%s WHERE HCID=%s", (com_name, status, church_dict_glob_id[church_id], dateHC, str(time), clergy_member, contact_number, notes, hc_id))
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "There was a problem updating this Holy Communion record. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully updated Holy Communion record details")
                canvas.yview_moveto(0)
                editHC(frame, canvas)
                
        
        confirmHCEditsButton = tkinter.Button(editFrame, text="Make Changes", font=h1, bg=blue, fg="white", command=editHCDB)
        confirmHCEditsButton.grid(row=8, column=1, sticky='ew')

        if userlevel == 2:
            confirmHCEditsButton.grid_forget()

        # Insert Details
        hcListbox['state'] = 'disabled'
        selected_hc = hcListbox.get(tkinter.ANCHOR)
        selected_hc = hc_dict[selected_hc]
        hc_id = selected_hc[0]
        print(selected_hc)

        comNameEntry.insert(0, selected_hc[1])

        status_selection.set(selected_hc[2])

        church_selection.set(church_dict_glob[selected_hc[3]])

        # Date
        if selected_hc[4] == "Undetermined":
            checkBool.select()
            cal['state'] = 'disabled'
        
        else:
            dateEntry.set(selected_hc[4])

        # Time
        if selected_hc[5] == "Undetermined":
            checkTBool.select()
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'

        else:
            hour = selected_hc[5][0:2]
            minute = selected_hc[5][3:5]
            hour_select_first_selection.set(hour)
            minute_select_first_selection.set(minute)

        clergyEntry.insert(0, selected_hc[6])

        contactNumberEntry.insert(0, selected_hc[7])

        notesEntry.insert('end', selected_hc[8])

        # block if userlevel = 2
        if userlevel == 2:
            comNameEntry['state'] = 'disabled'
            statusSelector['state'] = 'disabled'
            statusSelector['bg'] = "white"
            churchSelector['state'] = 'disabled'
            churchSelector['bg'] = "white"
            checkBool['bg'] = "white"
            checkBool['state'] = 'disabled'    
            cal['state'] = 'disabled'
            checkTBool['state'] = 'disabled'
            checkTBool['bg'] = "white"
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'
            clergyEntry['state'] = 'disabled'
            contactNumberEntry['state'] = 'disabled'
            notesEntry['state'] = 'disabled'

            if notBool.get() == 1:
                cal.grid_forget()

        
            
        
            

    if userlevel == 1 or userlevel == 3:
        editButton = tkinter.Button(container, text="View/Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditHC(editFrame))
        editButton.grid(row=2, column=0, sticky='w')
    else:
        editButton = tkinter.Button(container, text="View Details", font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditHC(editFrame))
        editButton.grid(row=2, column=0, sticky='w')

    def deleteHCDB():
        selected_hc = hcListbox.get(tkinter.ANCHOR)
        selected_hc = hc_dict[selected_hc][0]

        confirmation = askyesno(title="Confirmation", message="Are you sure you want to delete the selected Holy Communion Record?")
        if confirmation:
            try:
                sql("DELETE FROM HolyCommunion WHERE HCID={}".format(selected_hc))
            except:
                messagebox.showerror("Error", "An error occured when deleting the Holy Communion Record. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully deleted Holy Communion Record")
            canvas.yview_moveto(0)
            editHC(frame, canvas) 

    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Holy Communion", font=h1, bg=blue, fg="white", width=30, command=deleteHCDB)
        deleteButton.grid(row=2, column=0, sticky='e')

    hc_dict = searchFunctionHC(hcListbox, container, 3)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=6,column=0, columnspan=2)





def hcOptions(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options

    if userlevel == 1 or userlevel == 3:
        hcAddButton = tkinter.Button(mOptionsFrame, text="Add Hoy Communion", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addHC(restFrame, canvas))
        hcAddButton.grid(row=0, column=1, padx=10)

    if userlevel == 1 or userlevel == 3:
        hcEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete Holy Communion", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editHC(restFrame, canvas, userlevel))
        hcEditButton.grid(row=0, column=2, padx=10)

    else:
        hcEditButton = tkinter.Button(mOptionsFrame, text="View Holy Communion", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editHC(restFrame, canvas, userlevel))
        hcEditButton.grid(row=0, column=2, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)