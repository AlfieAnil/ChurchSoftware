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
from search_func import searchFunctionFuneral
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import askyesno
from members_class import *


def addFuneral(frame, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    # Child Name 
    decNamePrompt = tkinter.Label(container, text="Name of Deceased: ", fg="white", bg=blue, font=h1)
    decNamePrompt.grid(row=0, column=0)

    decNameEntry = tkinter.Entry(container, font=h2)
    decNameEntry.grid(row=0, column=1, sticky='ew')

    # Status Selection
    status_selection = StringVar(container)
    status_selection.set("Received")
    status_choices = ["Received", "Passed to Clergy Member", "Date Confirmed", "Certificate Issued", "Entered in Register"]

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

    # Date of Funeral
    datePrompt = tkinter.Label(container, text="Date of Funeral: ", font=h1, bg=blue, fg="white")
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

    timePrompt = tkinter.Label(container, text="Time of Funeral (HH/MM) :", font=h1, fg="white", bg=blue)
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
    def commitFuneralDB():
        dec_name = decNameEntry.get()
        status = status_selection.get()
        church_id = church_selection.get()
        dateFuneral = dateEntry.get()
        # Time
        time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

        if notTBool.get() == 1:
            time = "Undetermined"

        clergy_member = clergyEntry.get()
        contact_number = contactNumberEntry.get()
        notes = notesEntry.get('1.0', 'end')

        if not check_name(dec_name):
            return None
        
        if len(clergy_member.split()) < 2:
            messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
            return False

        # Date Check
        if notBool.get() == 1:
            dateFuneral = "Undetermined"
        else:
            date_split = dateFuneral.split('/')

            date_split = [int(x) for x in date_split]

            if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                messagebox.showerror("Error", "Ensure that the date is in the future")
                return None

        if len(contact_number) != 11:
            messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
            return None


        confirmation = askyesno(title="Confirmation", message="Are you sure you want to add this Funeral?")
        if confirmation:
            try:
                sql_items("INSERT INTO Funeral (DeceasedName, Status, ChurchID, DateOfFuneral, TimeOfFuneral, ClergyID, ContactNumber, Notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (dec_name, status, church_dict_glob_id[church_id], dateFuneral, str(time), clergy_member, contact_number, notes))

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error adding the Funeral. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully added Funeral")
            canvas.yview_moveto(0)
            addFuneral(frame, canvas)
        


    commitFuneralButton = tkinter.Button(container, text="Add Funeral", font=h1, fg="white", bg=blue, command=commitFuneralDB)
    commitFuneralButton.grid(row=8, column=1, sticky='ew')



def editFuneral(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    funListbox = tkinter.Listbox(container, width=100, font=h2)
    funListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=funListbox.xview)
    funListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=funListbox.yview)
    funListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    def viewEditFuneral(editFrame):
        
        if len(funListbox.get(tkinter.ANCHOR)) == 0:
            return None

        # Child Name 
        decNamePrompt = tkinter.Label(editFrame, text="Funeral Name: ", fg="white", bg=blue, font=h1)
        decNamePrompt.grid(row=0, column=0)

        decNameEntry = tkinter.Entry(editFrame, font=h2)
        decNameEntry.grid(row=0, column=1, sticky='ew')

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

        # Date of funeral
        datePrompt = tkinter.Label(editFrame, text="Date of Funeral: ", font=h1, bg=blue, fg="white")
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

        timePrompt = tkinter.Label(editFrame, text="Time of Funeral (HH/MM) :", font=h1, fg="white", bg=blue)
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

        def editFuneralDB():
            dec_name = decNameEntry.get()
            status = status_selection.get()
            church_id = church_selection.get()
            dateFuneral = dateEntry.get()
            # Time
            time = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))

            if notTBool.get() == 1:
                time = "Undetermined"

            clergy_member = clergyEntry.get()
            contact_number = contactNumberEntry.get()
            notes = notesEntry.get('1.0', 'end')

            if not check_name(dec_name):
                return None
            
            if len(clergy_member.split()) < 2:
                messagebox.showerror("Error", "Please enter the Full Name of the Clergy Member (with title, e.g. Fr/Dcn)")
                return False

            # Date Check
            if notBool.get() == 1:
                dateFuneral = "Undetermined"
            else:
                date_split = dateFuneral.split('/')

                date_split = [int(x) for x in date_split]

                if not(datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                    messagebox.showerror("Error", "Ensure that the date is in the future")
                    return None

            if len(contact_number) != 11:
                messagebox.showerror("Error", "Please insert a valid phone number (11 Digits)")
                return None


            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make changes to this Funeral Record?")
            
            if confirmation:
                try:
                    sql_items("UPDATE Funeral SET DeceasedName=%s, Status=%s, ChurchID=%s, DateOfFuneral=%s, TimeOfFuneral=%s, ClergyID=%s, ContactNumber=%s, Notes=%s WHERE FuneralID=%s", (dec_name, status, church_dict_glob_id[church_id], dateFuneral, str(time), clergy_member, contact_number, notes, funeral_id))
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "There was a problem updating this Funeral record. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully updated Funeral record details")
                canvas.yview_moveto(0)
                editFuneral(frame, canvas)
                
        confirmFuneralEditsButton = tkinter.Button(editFrame, text="Make Changes", font=h1, bg=blue, fg="white", command=editFuneralDB)
        confirmFuneralEditsButton.grid(row=8, column=1, sticky='ew')

        if userlevel == 2:
            confirmFuneralEditsButton.grid_forget()

        # Insert Details
        funListbox['state'] = 'disabled'
        selected_funeral = funListbox.get(tkinter.ANCHOR)
        selected_funeral = funeral_dict[selected_funeral]
        funeral_id = selected_funeral[0]
        print(selected_funeral)

        decNameEntry.insert(0, selected_funeral[1])

        status_selection.set(selected_funeral[2])

        church_selection.set(church_dict_glob[selected_funeral[3]])

        # Date
        if selected_funeral[4] == "Undetermined":
            checkBool.select()
            cal['state'] = 'disabled'
        
        else:
            funeral_date = selected_funeral[4]
            print("Selected Funeral: ", selected_funeral[4])
            dateEntry.set(funeral_date)

        # Time
        if selected_funeral[5] == "Undetermined":
            checkTBool.select()
            hour_select_first['state'] = 'disabled'
            minute_select_first['state'] = 'disabled'

        else:
            hour = selected_funeral[5][0:2]
            minute = selected_funeral[5][3:5]
            hour_select_first_selection.set(hour)
            minute_select_first_selection.set(minute)

        clergyEntry.insert(0, selected_funeral[6])

        contactNumberEntry.insert(0, selected_funeral[7])

        notesEntry.insert('end', selected_funeral[8])

        # Block if userlevel = 2
        if userlevel == 2:
            decNameEntry['state'] = 'disabled'
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
            
            
        
            

    funeral_text = "View Details"
    if userlevel == 1 or userlevel == 3:
        funeral_text = "View/Edit Details"
    editButton = tkinter.Button(container, text=funeral_text, font=h1, bg=blue, fg="white", width=30, command=lambda: viewEditFuneral(editFrame))
    editButton.grid(row=2, column=0, sticky='w')

    def deleteFuneralDB():
        selected_funeral = funListbox.get(tkinter.ANCHOR)
        selected_funeral = funeral_dict[selected_funeral][0]

        confirmation = askyesno(title="Confirmation", message="Are you sure you want to delete the selected Funeral Record?")
        if confirmation:
            try:
                sql("DELETE FROM Funeral WHERE FuneralID={}".format(selected_funeral))
            except:
                messagebox.showerror("Error", "An error occured when deleting the funeral. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully deleted Funeral Record")
            canvas.yview_moveto(0)
            editFuneral(frame, canvas) 

    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Funeral", font=h1, bg=blue, fg="white", width=30, command=deleteFuneralDB)
        deleteButton.grid(row=2, column=0, sticky='e')

    funeral_dict = searchFunctionFuneral(funListbox, container, 3)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=6,column=0, columnspan=2)



def funeralOptions(frame, canvas, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options

    if userlevel == 1 or userlevel == 3:
        funeralAddButton = tkinter.Button(mOptionsFrame, text="Add Funeral", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addFuneral(restFrame, canvas))
        funeralAddButton.grid(row=0, column=1, padx=10)

    t_text = "View Funeral"
    if userlevel == 1 or userlevel == 3:
        t_text = "View/Edit/Delete Funeral"
    funeralEditButton = tkinter.Button(mOptionsFrame, text=t_text, highlightthickness=0, bd=0, font=h1, bg=blue, fg="white", command=lambda: editFuneral(restFrame, canvas, userlevel))
    funeralEditButton.grid(row=0, column=2, padx=10)
        

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)