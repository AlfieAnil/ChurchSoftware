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
from tkcalendar import Calendar
from tkinter.messagebox import askyesno
from search_func import adults_list, childrens_list, church_dict_glob, church_dict_glob_id, roles_dict_glob, roles_dict_glob_id, family_dict_glob, church_dict_glob_name, searchFunctionAdults, searchFunctionBooking

def getMemberID(memberID):
    if memberID[4] == 'a':
        for person in adults_list:
            if person.value == memberID:
                return person.member_id

    else:
        for person in childrens_list:
            if person.value == memberID:
                return person.member_id

def addBooking(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    # Church select
    churchPrompt = tkinter.Label(container, text="Church: ", bg=blue, fg="white", font=h1)
    churchPrompt.grid(row=0, column=0, pady=10)

    church_selection = StringVar(container)
    church_dictionary = {}
    church_list = []
    churches = sql_select("SELECT * FROM Churches")
    for id, churchName in churches:
        church_dictionary["ID: {} Church Name: {}".format(id, churchName)] = id 
        church_list.append("ID: {} Church Name: {}".format(id, churchName))
    
    print(church_dictionary)

    church_selection.set(church_list[0])
    church_choices = church_list
    churchSelector = OptionMenu(container, church_selection, *church_choices)
    churchSelector.config(bg=blue, fg="white", padx=5)
    churchSelector.grid(row=0, column=1, sticky='ew')

    # Date

    datePrompt = tkinter.Label(container, text="Date: ", font=h1, bg=blue, fg="white")
    datePrompt.grid(row=1, column=0, pady=10)

    # dateEntry = tkinter.Entry(container, font=h1, bg=blue, fg="white", width=20, state='disabled')
    # dateEntry.grid(row=1, column=1, sticky='ew')
    dateEntry = tkinter.StringVar()
    cal = DateEntry(container, font=h2, selectmode='day', textvariable=dateEntry, date_pattern='dd/MM/yyyy')
    cal.grid(row=1, column=1, sticky='ew')

    def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
            calendar_window = tkinter.Tk()

            calendar = Calendar(calendar_window, font="Arial", selectmode='day')
            calendar.grid(row=0, column=0, sticky='ew')

            def return_date():
                print("Function Date: ", calendar.selection_get())
                selected_date = calendar.selection_get()
                date = selected_date.strftime("%d/%m/%Y")

                dateEntry['state'] = 'normal'
                dateEntry.delete(0, 'end')

                dateEntry.insert(0, str(date))
                dateEntry['state'] = 'disabled'

                calendar_window.destroy()
            
            tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

    # date_selector = tkinter.Button(container, text="Select Date", command=select_dob_calendar)
    # date_selector.grid(row=1, column=2, sticky='e', padx=5)

    # Time

    timePrompt = tkinter.Label(container, text="Time: ", font=h1, bg=blue, fg="white")
    timePrompt.grid(row=2, column=0)

    timeContainer = tkinter.Frame(container, bg=blue)
    timeContainer.grid(row=2, column=1)

    hour_select_first_selection = tkinter.StringVar()
    hour_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable = hour_select_first_selection, from_=00, to=23, width=5, font=h2, format="%02.0f").grid(row=0, column=1)

    colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=2)

    minutes_list = ['00', '15', '30', '45']
    minute_select_first_selection = tkinter.StringVar()
    minute_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_first_selection, values=minutes_list, width=5, font=h2).grid(row=0, column=3)

    tkinter.Label(timeContainer, text=" to ", bg=blue, fg="white", font=h2).grid(row=0,column=4, padx=10)

    hour_select_second_selection = tkinter.StringVar()
    hour_select_second = tkinter.Spinbox(timeContainer, state='readonly', textvariable=hour_select_second_selection, from_=00, to=23, width=5, font=h2, format="%02.0f").grid(row=0, column=5)

    colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=6)

    minutes_list = ['00', '15', '30', '45']
    minute_select_second_selection = tkinter.StringVar()
    minute_select_second = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_second_selection, values=minutes_list, width=5, font=h2).grid(row=0, column=7)

    # Member Select

    memberPrompt = tkinter.Label(container, text="Member: ", font=h1, bg=blue, fg="white")
    memberPrompt.grid(row=3, column=0)

    def selectMember():
        memberFinder = tkinter.Tk()
        memberFinder.geometry('910x400')
        memberFinder.title("Member Finder")
        memberFinder['background'] = blue

        indListbox = tkinter.Listbox(memberFinder, width=100, height=50, font=h2)
        indListbox.grid(row=0, column=0, sticky='ew')

        horizontal_scrollbar = tkinter.Scrollbar(memberFinder, orient=tkinter.HORIZONTAL, command=indListbox.xview)
        indListbox['xscrollcommand'] = horizontal_scrollbar.set
        horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

        vertical_scrollbar = tkinter.Scrollbar(memberFinder, orient=tkinter.VERTICAL, command=indListbox.yview)
        indListbox['yscrollcommand'] = vertical_scrollbar.set
        vertical_scrollbar.grid(row=0, column=0, sticky='ens')

        searchFunctionAdults(indListbox, memberFinder, 2)

        def showMemberButton():

            if len(indListbox.get(tkinter.ANCHOR)) == 0:
                return None
            memberButton['text'] = indListbox.get(tkinter.ANCHOR)

            memberFinder.destroy()

        selectButton = tkinter.Button(memberFinder, text="Select Member", font=h1, fg="white", bg=blue, command=showMemberButton)
        selectButton.grid(row=5, column=0, columnspan=2, sticky='ew')

        memberFinder.mainloop()

    memberButton = tkinter.Button(container, text="Find Member", font=h2, bg=blue, fg="white", command=selectMember)
    memberButton.grid(row=3, column=1, sticky='ew')

    # Description
    descriptionPrompt = tkinter.Label(container, text="Description: ", font=h1, fg="white", bg=blue)
    descriptionPrompt.grid(row=4, column=0)

    descEntry = tkinter.Text(container, font=h2)
    descEntry.grid(row=4, column=1, sticky='ew')

    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=descEntry.yview, bg=blue)
    descEntry['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=4, column=2, sticky='wns')

    def addBookingDB():
        booking_church_id = church_dictionary[church_selection.get()]
        date = dateEntry.get()
        description = descEntry.get('1.0', 'end')

        if len(date) == 0:
            messagebox.showerror("Error", "Please Enter a valid date")
            return None
        
        date_split = date.split('/')

        date_split = [int(x) for x in date_split]

        if not (datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
            messagebox.showerror("Error", "Ensure that the date is in the Future")
            return None

        # print(hour_select_first_selection.get())
        if not ((0 <= int(hour_select_first_selection.get()) < 24) and (0 <= int(minute_select_first_selection.get()) < 60) and (0 <= int(hour_select_second_selection.get()) < 24) and (0 <= int(minute_select_second_selection.get()) < 60)):
            messagebox.showerror("Error", "Please ensure that you have entered valid dates")
            return None

        time_from_str = "{}:{}".format(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))
        time_to_str = "{}:{}".format(int(hour_select_second_selection.get()), int(minute_select_second_selection.get()))

        time_from = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))
        time_to = datetime.time(int(hour_select_second_selection.get()), int(minute_select_second_selection.get()))

        if time_from > time_to:
            messagebox.showerror("Error", "Please ensure that the end time is greater than the start time")
            return None

        if len(description) == 1:
            messagebox.showerror("Error", "Please ensure that you have included a description")
            return None

        time = "{} - {}".format(time_from, time_to)
        
        if memberButton['text'] == "Find Member":
            messagebox.showerror("Error", "Please select a Member by Clicking on the 'Find Member' Button")
            return None

        member_aid_c = getMemberID(memberButton['text'])

        overlap_check = sql_select("SELECT MemberAID, Time FROM ChurchBookings WHERE Date='{}' AND ChurchID={}".format(date, booking_church_id))
        text = "There are already some bookings made for this day at the following times? Are you sure you want to continue with the booking?"
        
        if len(overlap_check) != 0:
            
            
            overlaps = False
            for temp_memberaid, temp_time in overlap_check:
                text += "\n{}".format(temp_time)
                overlaps = True

            if overlaps:
                overlap_question = askyesno(title="Confirmation", message=text)
                if not overlap_question:
                    return None
                



        commit_question = askyesno(title="Confirmation", message="Are you sure you want to add this Booking?")
        
        if commit_question:
            try:
                sql("INSERT INTO ChurchBookings (ChurchID, Date, Time, MemberAID, Description) VALUES ({}, '{}', '{}', {}, '{}')".format(booking_church_id, date, time, member_aid_c, description))
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Failed to add Booking to Database. Please try again later")
                return None
            
            messagebox.showinfo("Success", "Successfully inserted booking into Database")

            addBooking(frame)




    addBookingButton = tkinter.Button(container, text="Add Booking", fg="white", font=h2, bg=blue, command=addBookingDB)
    addBookingButton.grid(row=5,column=1, sticky='ew')



def editBooking(frame, userlevel, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    h0 = tkFont.Font(family='Helvetica', size=14, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    selectPrompt = tkinter.Label(container, text="Select Booking", fg="white", bg=blue, font=h0)
    selectPrompt.grid(row=0, column=0, sticky='ew')

    memberSelect = tkinter.Listbox(container, width=110, height=15, font=h2)
    memberSelect.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=memberSelect.xview)
    memberSelect['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=memberSelect.yview)
    memberSelect['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    def editBookingDetails(editFrame):
        bookingEdit = memberSelect.get(tkinter.ANCHOR)

        def editDetailFrameBookings(container, bookingid):
            # Church select
            churchPrompt = tkinter.Label(container, text="Church: ", bg=blue, fg="white", font=h1)
            churchPrompt.grid(row=0, column=0, pady=10)

            church_selection = StringVar(container)
            church_dictionary = {}
            church_list = []
            churches = sql_select("SELECT * FROM Churches")
            for id, churchName in churches:
                church_dictionary["ID: {} Church Name: {}".format(id, churchName)] = id 
                church_list.append("ID: {} Church Name: {}".format(id, churchName))
            
            print(church_dictionary)

            church_selection.set(church_list[0])
            church_choices = church_list
            churchSelector = OptionMenu(container, church_selection, *church_choices)
            churchSelector.config(bg=blue, fg="white", padx=5)
            churchSelector.grid(row=0, column=1, sticky='ew')

            # Date

            datePrompt = tkinter.Label(container, text="Date: ", font=h1, bg=blue, fg="white")
            datePrompt.grid(row=1, column=0, pady=10)

            dateEntry = tkinter.StringVar()
            cal = DateEntry(container, font=h2, selectmode='day', textvariable=dateEntry, date_pattern='dd/MM/yyyy')
            cal.grid(row=1, column=1, sticky='ew')

            def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
                    calendar_window = tkinter.Tk()

                    calendar = Calendar(calendar_window, font="Arial", selectmode='day')
                    calendar.grid(row=0, column=0, sticky='ew')

                    def return_date():
                        print("Function Date: ", calendar.selection_get())
                        selected_date = calendar.selection_get()
                        date = selected_date.strftime("%d/%m/%Y")

                        dateEntry['state'] = 'normal'
                        dateEntry.delete(0, 'end')

                        dateEntry.insert(0, str(date))
                        dateEntry['state'] = 'disabled'

                        calendar_window.destroy()
                    
                    tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

            # date_selector = tkinter.Button(container, text="Select Date", command=select_dob_calendar)
            # date_selector.grid(row=1, column=2, sticky='e', padx=5)

            # Time

            timePrompt = tkinter.Label(container, text="Time: ", font=h1, bg=blue, fg="white")
            timePrompt.grid(row=2, column=0)

            timeContainer = tkinter.Frame(container, bg=blue)
            timeContainer.grid(row=2, column=1)

            hour_select_first_selection = tkinter.StringVar()
            hour_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable = hour_select_first_selection, from_=00, to=23, format="%02.0f", width=5, font=h2)
            hour_select_first.grid(row=0, column=1)

            colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=2)

            minutes_list = ['00', '15', '30', '45']
            minute_select_first_selection = tkinter.StringVar()
            minute_select_first = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_first_selection, values=minutes_list, width=5, font=h2)
            minute_select_first.grid(row=0, column=3)

            tkinter.Label(timeContainer, text=" to ", bg=blue, fg="white", font=h2).grid(row=0,column=4, padx=10)

            hour_select_second_selection = tkinter.StringVar()
            hour_select_second = tkinter.Spinbox(timeContainer, state='readonly', textvariable=hour_select_second_selection, from_=00, to=23, format="%02.0f", width=5, font=h2)
            hour_select_second.grid(row=0, column=5)

            colonLabel = tkinter.Label(timeContainer, text=":", fg="white", bg=blue, font=h2).grid(row=0, column=6)

            minutes_list = ['00', '15', '30', '45']
            minute_select_second_selection = tkinter.StringVar()
            minute_select_second = tkinter.Spinbox(timeContainer, state='readonly', textvariable=minute_select_second_selection, values=minutes_list, width=5, font=h2)
            minute_select_second.grid(row=0, column=7)

            # Member Select

            memberPrompt = tkinter.Label(container, text="Member: ", font=h1, bg=blue, fg="white")
            memberPrompt.grid(row=3, column=0)

            def selectMember():
                memberFinder = tkinter.Tk()
                memberFinder.geometry('910x400')
                memberFinder.title("Member Finder")
                memberFinder['background'] = blue

                indListbox = tkinter.Listbox(memberFinder, width=100, height=50, font=h2)
                indListbox.grid(row=0, column=0, sticky='ew')

                horizontal_scrollbar = tkinter.Scrollbar(memberFinder, orient=tkinter.HORIZONTAL, command=indListbox.xview)
                indListbox['xscrollcommand'] = horizontal_scrollbar.set
                horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

                vertical_scrollbar = tkinter.Scrollbar(memberFinder, orient=tkinter.VERTICAL, command=indListbox.yview)
                indListbox['yscrollcommand'] = vertical_scrollbar.set
                vertical_scrollbar.grid(row=0, column=0, sticky='ens')

                searchFunctionAdults(indListbox, memberFinder, 2)

                def showMemberButton():

                    if len(indListbox.get(tkinter.ANCHOR)) == 0:
                        return None
                    memberButton['text'] = indListbox.get(tkinter.ANCHOR)

                    memberFinder.destroy()

                selectButton = tkinter.Button(memberFinder, text="Select Member", fg="white", bg=blue, command=showMemberButton)
                selectButton.grid(row=5, column=0, columnspan=2, sticky='ew')

                memberFinder.mainloop()

            memberButton = tkinter.Button(container, text="Find Member", font=h2, bg=blue, fg="white", command=selectMember)
            memberButton.grid(row=3, column=1, sticky='ew')

            # Description
            descriptionPrompt = tkinter.Label(container, text="Description: ", font=h1, fg="white", bg=blue)
            descriptionPrompt.grid(row=4, column=0)

            descEntry = tkinter.Text(container, font=h2)
            descEntry.grid(row=4, column=1, sticky='ew')

            scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=descEntry.yview, bg=blue)
            descEntry['yscrollcommand'] = scrollbar.set
            scrollbar.grid(row=4, column=2, sticky='wns')

            def updateBookingDetails():
                
                booking_church_id = church_dictionary[church_selection.get()]
                date = dateEntry.get()
                description = descEntry.get('1.0', 'end')

                if len(date) == 0:
                    messagebox.showerror("Error", "Please Enter a valid date")
                    return None
                
                date_split = date.split('/')

                date_split = [int(x) for x in date_split]

                if not (datetime.datetime(date_split[2], date_split[1], date_split[0]) > datetime.datetime.now()):
                    messagebox.showerror("Error", "Ensure that the date is in the Future")
                    return None

                # print(hour_select_first_selection.get())
                if not ((0 <= int(hour_select_first_selection.get()) < 24) and (0 <= int(minute_select_first_selection.get()) < 60) and (0 <= int(hour_select_second_selection.get()) < 24) and (0 <= int(minute_select_second_selection.get()) < 60)):
                    messagebox.showerror("Error", "Please ensure that you have entered valid dates")
                    return None

                time_from_str = "{}:{}".format(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))
                time_to_str = "{}:{}".format(int(hour_select_second_selection.get()), int(minute_select_second_selection.get()))

                time_from = datetime.time(int(hour_select_first_selection.get()), int(minute_select_first_selection.get()))
                time_to = datetime.time(int(hour_select_second_selection.get()), int(minute_select_second_selection.get()))

                if time_from > time_to:
                    messagebox.showerror("Error", "Please ensure that the end time is greater than the start time")
                    return None

                if len(description) == 1:
                    messagebox.showerror("Error", "Please ensure that you have included a description")
                    return None

                time = "{} - {}".format(time_from, time_to)
                
                if memberButton['text'] == "Find Member":
                    messagebox.showerror("Error", "Please select a Member by Clicking on the 'Find Member' Button")
                    return None

                member_aid_c = getMemberID(memberButton['text'])

                overlap_check = sql_select("SELECT MemberAID, Time FROM ChurchBookings WHERE Date='{}' AND ChurchID={}".format(date, booking_church_id))
                text = "There are already some bookings made for this day at the following times? Are you sure you want to continue with the booking?"
                
                if len(overlap_check) != 0:
                    
                    
                    overlaps = False
                    for temp_memberaid, temp_time in overlap_check:
                        text += "\n{}".format(temp_time)
                        overlaps = True

                    if overlaps:
                        overlap_question = askyesno(title="Confirmation", message=text)
                        if not overlap_question:
                            return None

                commit_question = askyesno(title="Confirmation", message="Are you sure you want to make these changes?")
                
                if commit_question:
                    try:
                        sql("UPDATE ChurchBookings SET ChurchID={}, Date='{}', Time='{}', MemberAID={}, Description='{}' WHERE BookingID={}".format(booking_church_id, date, time, member_aid_c, description, bookingid))
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Failed to udpate the Booking. Please try again later")
                        return None
                    
                    messagebox.showinfo("Success", "Successfully updated booking details to Database")
                    canvas.yview_moveto(0)
                    editBooking(frame, userlevel, canvas)


            if userlevel == 1 or userlevel == 3:
                confirmButton = tkinter.Button(container, text="Confirm Changes", fg="white", bg=blue, font=h1, command=updateBookingDetails)
                confirmButton.grid(row=5, column=1, sticky='ew')

            # Insert Details
            temp_details = sql_select("SELECT * FROM ChurchBookings WHERE BookingID={}".format(int(bookingid)))

            for booking_id, churchid, date, time, memberid, description in temp_details:
                church_selection.set(church_dict_glob[churchid])

                # dateEntry['state'] = 'normal'
                dateEntry.set(date)
                # dateEntry['state'] = 'disabled'

                times = time.split(' - ')

                time_from = times[0][0:5]
                time_to = times[1][0:5]

                hour_select_first_selection.set(time_from[0:2])
                minute_select_first_selection.set(time_from[3:])

                hour_select_second_selection.set(time_to[0:2])
                minute_select_second_selection.set(time_to[3:])

                for person in adults_list:
                    if person.member_id == memberid:
                        memberButton['text'] = person.value

                descEntry.insert('end', description)

            # Block if userlevel = 2
            if userlevel == 2:
                churchSelector['state'] = 'disabled'
                churchSelector['bg'] = "white"
                cal['state'] = 'disabled'
                hour_select_first['state'] = 'disabled'
                minute_select_first['state'] = 'disabled'
                hour_select_second['state'] =  'disabled'
                minute_select_second['state'] = 'disabled'
                memberButton['state'] = 'disabled'
                memberButton['bg'] = "white"
                descEntry['state'] = 'disabled'



        booking_id = bookingEdit[bookingEdit.find('ID: ')+4:bookingEdit.find(' |')]
        print(booking_id)
        memberSelect['state'] = 'disabled'
        editDetailFrameBookings(editFrame, booking_id)
        


    if userlevel == 1 or userlevel == 3:
        editButton = tkinter.Button(container, text="View/Edit Bookings", font=h1, bg=blue, fg="white", width=30, command=lambda: editBookingDetails(editFrame))
        editButton.grid(row=3, column=0, sticky='w')
    
    if userlevel == 2:
        editButton = tkinter.Button(container, text="View Bookings", font=h1, bg=blue, fg="white", width=30, command=lambda: editBookingDetails(editFrame))
        editButton.grid(row=3, column=0, sticky='w')

    def deleteSelectedBooking():
        def deleteBookingDB(delBookingID):
            commit_question = askyesno(title="Confirmation", message="Are you sure you want to add this Booking to the Database?")
        
            if commit_question:
                
            
            
                try:
                    sql("DELETE FROM ChurchBookings WHERE BookingID={}".format(delBookingID))
                except:
                    success = False
                    messagebox.showerror("Error", "There was an error deleting the given Booking. Please try again later")
                    return None
                
                messagebox.showinfo("Success", "Successfully deleted the given booking")
                editBooking(frame, userlevel, canvas)


        booking_selected = memberSelect.get(tkinter.ANCHOR)
        if len(booking_selected) == 0:
            messagebox.showerror("Error", "Please select a booking to continue")
            return None
        
        booking_id = booking_selected[booking_selected.find('ID: ')+4:booking_selected.find(' |')]
        deleteBookingDB(booking_id)
    
    if userlevel == 1 or userlevel == 3:
        deleteButton = tkinter.Button(container, text="Delete Booking", font=h1, bg=blue, fg="white", width=30, command=deleteSelectedBooking)
        deleteButton.grid(row=3, column=0, sticky='e')
    
    searchFunctionBooking(memberSelect, container, 4)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=5, column=0)


def bookingOptions(frame, userlevel, canvas):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options
    if userlevel == 1 or userlevel == 3:
        bookingAddButton = tkinter.Button(mOptionsFrame, text="Add Booking", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addBooking(restFrame))
        bookingAddButton.grid(row=0, column=1, padx=10)

    if userlevel == 1 or userlevel == 3:
        bookingEditButton = tkinter.Button(mOptionsFrame, text="View/Edit/Delete Bookings", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editBooking(restFrame, userlevel, canvas))
        bookingEditButton.grid(row=0, column=2, padx=10)

    else:
        bookingEditButton = tkinter.Button(mOptionsFrame, text="View Bookings", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editBooking(restFrame, userlevel, canvas))
        bookingEditButton.grid(row=0, column=2, padx=10)


    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)