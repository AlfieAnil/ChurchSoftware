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
from members_class import *



adults_list = []
t_adults_list = []
childrens_list = []
church_dict_glob = {}
church_dict_glob_id = {}
church_dict_glob_name = {}
roles_dict_glob = {}
roles_dict_glob_id = {}
family_dict_glob = {}

def t_list_assigner(n):
    global t_adults_list
    t_adults_list = n


def getMemberID(memberID):
    if memberID[4] == 'a':
        for person in adults_list:
            if person.value == memberID:
                return person.member_id

    else:
        for person in childrens_list:
            if person.value == memberID:
                return person.member_id


def person_update_adult(member_id, name, dob, churchid, roleids, occupation, gender, maritalstatus, phonenum, email, dbs, familyid, notes, religion):
    for person in adults_list:
        if person.member_id == member_id:
            person.fullname = name
            person.dob = dob
            person.churchid = churchid
            person.roleids = roleids
            person.occupation = occupation
            person.gender = gender
            person.maritalstatus = maritalstatus
            person.phonenum = phonenum
            person.email = email
            person.dbs = dbs
            person.familyid = familyid
            person.religion = religion
            person.notes = notes
            person.value = "ID: a{}. {} | {}".format(member_id, name, church_dict_glob_name[int(churchid)])
    

def person_update_child(member_id, fullname, dob, school, sacramentsreceived, churchofbaptism, roleids, familyid, notes, churchid, gender, religion):
    for person in childrens_list:
        if person.member_id == member_id:
            person.fullname = fullname
            person.dob = dob
            person.gender = gender
            person.school = school
            person.sacramentsreceived = sacramentsreceived
            person.churchbaptism = churchofbaptism
            person.roleid = roleids
            person.familyid = familyid
            person.notes = notes
            person.churchid = churchid
            person.religion = religion
            person.value = "ID: c{}. {} | {}".format(member_id, fullname, church_dict_glob_name[int(churchid)])

def person_creator_adult(member_id, name, dob, churchid, roleids, occupation, gender, maritalstatus, phonenum, email, dbs, familyid, notes, religion):
    person = Person()
    person.member_id = member_id
    person.fullname = name
    person.dob = dob
    person.churchid = churchid
    person.roleids = roleids
    person.occupation = occupation
    person.gender = gender
    person.maritalstatus = maritalstatus
    person.phonenum = phonenum
    person.email = email
    person.dbs = dbs
    person.familyid = familyid
    person.notes = notes
    person.religion = religion
    person.value = "ID: a{}. {} | {}".format(member_id, name, church_dict_glob_name[int(churchid)])
    adults_list.append(person)

def person_creator_child(member_id, fullname, dob, school, sacramentsreceived, churchofbaptism, roleids, familyid, notes, churchid, gender, religion):
    person = Person()
    person.member_id = member_id
    person.fullname = fullname
    person.dob = dob
    person.gender = gender
    person.school = school
    person.sacramentsreceived = sacramentsreceived
    person.churchbaptism = churchofbaptism
    person.roleid = roleids
    person.familyid = familyid
    person.notes = notes
    person.churchid = churchid
    person.religion = religion
    person.value = "ID: c{}. {} | {}".format(member_id, fullname, church_dict_glob_name[int(churchid)])
    childrens_list.append(person)

def id_finder(memberEdit):

    # adult_members = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult")
    # child_members = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild")

    # churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
    # churches_dict = {}
    # for churchid, churchname in churches:
    #     churches_dict[churchid] = churchname



    if memberEdit[4] == 'a':
            for person in adults_list:
                print("COMPARE")
                # print("ID: a{}. {} | {}".format(memberid, fullname, churches_dict[churchid]))
                print(person.value)
                print(memberEdit)
                if person.value == memberEdit:
                    return [person.member_id, 'a']
    else:
        for person in childrens_list:
            if person.value == memberEdit:
                return [person.member_id, 'c']




def searchFunctionFamily(memberSelect, container, given_row):
        h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
        h2 = tkFont.Font(family='Helvetica', size=12)

        def fill_listbox():
            family_dets = sql_select("SELECT * FROM Family")

            for familyid, familyname, notes, datecreated, address in family_dets:
                text = "FamilyID: {}, Family Name: {}, Address: {}, Date Created: {}, Notes: {}".format(familyid, familyname, address, datecreated, notes)
                memberSelect.insert('end', text)

        fill_listbox()


        searchFrame = tkinter.Frame(container, bg=blue)
        searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

        container.rowconfigure(0, weight=1)

        searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
        searchLabel.grid(row=0, column=0)

        search_selection = StringVar(searchFrame)
        search_selection.set("FamilyID")
        search_choices = ["FamilyID", "Family Name"]


        searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
        searchSelector.config(bg=blue, fg="white", padx=3)
        searchSelector.grid(row=0, column=1)

        searchEntry = tkinter.Entry(searchFrame, font=h2)
        searchEntry.grid(row=0, column=2, sticky='ew')
        
        def searcher():
            memberSelect.delete(0, 'end')
            search_property = search_selection.get()
            search_entry = searchEntry.get()
            print(search_entry)
            if search_property == "FamilyID":
                try:
                    int(search_entry)
                    result = sql_select("SELECT * FROM Family WHERE FamilyID={}".format(int(search_entry)))
                    result = result[0]
                    memberSelect.insert('end', "FamilyID: {}, Family Name: {}, Address: {}, Date Created: {}, Notes: {}".format(result[0], result[1], result[4], result[3], result[2]))

                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "Please enter a valid id")
                    return None

            # Searching Adult
            result1 = sql_select("SELECT * FROM Family WHERE FamilyName LIKE '%{}%'".format(search_entry))
            print(result1)

            # Outputting both
            if len(result1) != 0:
                for familyid, familyname, notes, datecreated, address in result1:
                    memberSelect.insert('end', "FamilyID: {}, Family Name: {}, Address: {}, Date Created: {}, Notes: {}".format(familyid, familyname, address, datecreated, notes))

        searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
        searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


        resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
        resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')


def searchFunctionRoles(memberSelect, container, given_row):
        h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
        h2 = tkFont.Font(family='Helvetica', size=12)

        def fill_listbox():
            role_dets = sql_select("SELECT * FROM Roles")

            for roleid, rolename, roledescription in role_dets:
                text = "RoleID: {} | Role Name: {} | Description: {}".format(roleid, rolename, roledescription)
                memberSelect.insert('end', text)

        fill_listbox()


        searchFrame = tkinter.Frame(container, bg=blue)
        searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

        container.rowconfigure(0, weight=1)

        searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
        searchLabel.grid(row=0, column=0)

        search_selection = StringVar(searchFrame)
        search_selection.set("Role Name")
        search_choices = ["Role Name"]


        searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
        searchSelector.config(bg=blue, fg="white", padx=3)
        searchSelector.grid(row=0, column=1)

        searchEntry = tkinter.Entry(searchFrame, font=h2)
        searchEntry.grid(row=0, column=2, sticky='ew')
        
        def searcher():
            memberSelect.delete(0, 'end')
            search_property = search_selection.get()
            search_entry = searchEntry.get()
            print(search_entry)

            # Searching Adult
            result1 = sql_select("SELECT * FROM Roles WHERE RoleName LIKE '%{}%'".format(search_entry))
            print(result1)

            # Outputting both
            if len(result1) != 0:
                for roleid, rolename, roledescription in result1:
                    memberSelect.insert('end', "RoleID: {} | Role Name: {} | Description: {}".format(roleid, rolename, roledescription))

        searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
        searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


        resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
        resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')


# memberSelect = Listbox, container = frame
def searchFunction(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
    churches_dict = {}
    for churchid, churchname in churches:
        churches_dict[churchid] = churchname

    def fill_listbox():
        memberSelect.delete(0, 'end')

        for person in adults_list:
            print("new person")
            memberSelect.insert('end', person.value)

        for person in childrens_list:
            memberSelect.insert('end', person.value)


    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("MemberID")
    search_choices = ["MemberID", "Full Name", "Occupation", "DOB", "Phone Number", "Email", "RoleID"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
        if search_property == "MemberID":
            try:
                int(search_entry[1:])
            except:
                messagebox.showerror("Error", "Please enter a valid id")
            if search_entry[0] == 'a':
                print('here')
                # result = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE MemberAID={}".format(int(search_entry[1:])))
                for person in adults_list:
                    if person.member_id == int(search_entry[1:]):
                        memberSelect.insert('end', person.value)

                        return None

            elif search_entry[0] == 'c':
                try:
                    # result = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild WHERE MemberCID={}".format(int(search_entry[1:])))
                    for person in childrens_list:
                        if person.member_id == int(search_entry[1:]):

                            memberSelect.insert('end', person.value)
                            return None
                except:
                    messagebox.showerror("Error", "There was an issue executing the command")
                    return None

        property_dict = {
            "Full Name": "FullName",
            "Occupation": "Occupation",
            "DOB": "DOB",
            "Phone Number": "PhoneNum",
            "Email": "Email",
            "Role": "RoleID"
        }

        # Searching Adult
        result1 = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        # Searching Child
        result2 = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result2)

        # Outputting both
        if len(result1) != 0:
            for memberid, fullname, churchid in result1:
                memberSelect.insert('end', "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

        if len(result2) != 0:
            for memberid, fullname, churchid in result2:
                memberSelect.insert('end', "ID: c{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')


def searchFunctionAdults(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    
    churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
    churches_dict = {}
    for churchid, churchname in churches:
        churches_dict[churchid] = churchname

    def fill_listbox():
        memberSelect.delete(0, 'end')
        # mAdults = sql_select("SELECT * FROM MembersAdult")
        # mChilds = sql_select("SELECT * FROM MembersChild")
        for person in adults_list:
            memberSelect.insert('end', person.value)


    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("MemberID")
    search_choices = ["MemberID", "Full Name", "Occupation", "DOB", "Phone Number", "Email", "RoleID"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
        if search_property == "MemberID":
            try:
                int(search_entry[1:])
            except:
                messagebox.showerror("Error", "Please enter a valid id")
            if search_entry[0] == 'a':
                print('here')
                result = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE MemberAID={}".format(int(search_entry[1:])))
                memberSelect.insert('end', "ID: a{}. {} | {}".format(result[0][0], result[0][1], churches_dict[int(result[0][2])]))
                return None
            
            return None

        property_dict = {
            "Full Name": "FullName",
            "Occupation": "Occupation",
            "DOB": "DOB",
            "Phone Number": "PhoneNum",
            "Email": "Email",
            "RoleID": "RoleID"
        }

        # Searching Adult
        result1 = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        # Searching Child

        # Outputting both
        if len(result1) != 0:
            for memberid, fullname, churchid in result1:
                memberSelect.insert('end', "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

        
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')



def searchFunctionBooking(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    bookings_dict = {}
    bookings_dict_id = {}

    def fill_listbox():
        memberSelect.delete(0, 'end')
        
        recordedBookings = sql_select("SELECT * FROM ChurchBookings ORDER BY BookingID DESC")

        for bookingid, churchid, date, time, memberid, description in recordedBookings:
            m_name = "Error"
            for person in adults_list:
                if person.member_id == memberid:
                    m_name = "a{}. {}".format(person.member_id, person.fullname)
            text = "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(bookingid, church_dict_glob_name[churchid], date, time, m_name, description)

            bookings_dict[bookingid] = text
            bookings_dict_id[text] = bookingid

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("BookingID")
    search_choices = ["BookingID", "Church Name", "Date (DD/MM/YYYY)", "Member Name", "Description"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
        if search_property == "BookingID":
            try:
                int(search_entry)
            except:
                messagebox.showerror("Error", "Please enter a valid id")
            
            try:
                result = sql_select("SELECT * FROM ChurchBookings WHERE BookingID={}".format(int(search_entry)))
                print(result)
                m_name = "Error"
                for person in adults_list:
                    if person.member_id == int(result[0][4]):
                        m_name = "a{}. {}".format(person.member_id, person.fullname)
                memberSelect.insert('end', "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(result[0][0], church_dict_glob_name[result[0][1]], result[0][2], result[0][3], m_name, result[0][5]))
                return None
            except:
                messagebox.showerror("Error", "There was an issue executing the command")
                return None

        if search_property == "Member Name":
            person_ids = []

            for person in adults_list:
                if str(search_entry).upper() in (person.fullname).upper():
                    person_ids.append(person.member_id)

            print("person ids: ", person_ids)
            if len(person_ids) == 0:
                return None

            for person in person_ids:
                result = sql_select("SELECT * FROM ChurchBookings WHERE MemberAID={}".format(int(person)))

                for booking in result:
                    print("Booking: ", booking)
                    m_name = "Error"
                    for person in adults_list:
                        print("ID: {} | Name: {}".format(person.member_id, person.fullname))
                        if person.member_id == int(booking[4]):
                            m_name = "a{}. {}".format(person.member_id, person.fullname)
                            print("M-name: ", m_name)
                
                    text = "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(booking[0], church_dict_glob_name[booking[1]], booking[2], booking[3], m_name, booking[5]) 
                    memberSelect.insert('end', text)
            
            return None



        if search_property == "Church Name":
            church_ids = []
            for item in church_dict_glob_name:
                print("Search Entry: ", search_entry)
                print("name: ", church_dict_glob_name[item])
                if str(search_entry).upper() in church_dict_glob_name[item].upper():
                    print("Contains")
                    church_ids.append(item)

            if len(church_ids) == 0:
                return None
            
            print("church ids: ", church_ids)
            for churchid in church_ids:
                result = sql_select("SELECT * FROM ChurchBookings WHERE ChurchID={}".format(int(churchid)))
                print(result)

                for booking in result:
                    print("Booking: ", booking)
                    m_name = "Error"
                    for person in adults_list:
                        print("ID: {} | Name: {}".format(person.member_id, person.fullname))
                        if person.member_id == int(booking[4]):
                            m_name = "a{}. {}".format(person.member_id, person.fullname)
                            print("M-name: ", m_name)
                
                    text = "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(booking[0], church_dict_glob_name[booking[1]], booking[2], booking[3], m_name, booking[5]) 
                    memberSelect.insert('end', text)
                # m_name = "Error"
                # for person in adults_list:
                #     if person.member_id == int(result[0][4]):
                #         m_name = person.fullname
                
                # text = "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(result[0][0], church_dict_glob_name[result[0][1]], result[0][2], result[0][3], m_name, result[0][5])

                # memberSelect.insert('end', text)

            return None
                

        property_dict = {
            "Description": "Description",
            "Date (DD/MM/YYYY)": "Date",
            "Church Name": "ChurchID"
        }

        # Searching Bookings
        result1 = sql_select("SELECT * FROM ChurchBookings WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)

        # Outputting
        if len(result1) != 0:
            for bookingid, churchid, date, time, memberaid, description in result1:
                
                m_name = "Error"
                for person in adults_list:
                    print("ID: {} | Name: {}".format(person.member_id, person.fullname))
                    if person.member_id == int(bookingid):
                        m_name = "a{}. {}".format(person.member_id, person.fullname)
                        print("M-name: ", m_name)
            
                text = "Booking ID: {} | Church: {} | Date: {} | Time: {} | Member: {} | Description: {}".format(bookingid, church_dict_glob_name[churchid], date, time, m_name, description) 
                memberSelect.insert('end', text)
        
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')



# Search For Groups (so dynamically removing from listbox and list)
def searchFunctionEmail(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    
    churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
    churches_dict = {}
    for churchid, churchname in churches:
        churches_dict[churchid] = churchname

    def fill_listbox():
        memberSelect.delete(0, 'end')
        # mAdults = sql_select("SELECT * FROM MembersAdult")
        # mChilds = sql_select("SELECT * FROM MembersChild")
        for person in t_adults_list:
            memberSelect.insert('end', person.value)


    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("MemberID")
    search_choices = ["MemberID", "Full Name", "Occupation", "DOB", "Phone Number", "Email", "RoleID"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
        if search_property == "MemberID":
            try:
                int(search_entry[1:])
            except:
                messagebox.showerror("Error", "Please enter a valid id")
            
            for person in t_adults_list:
                if person.member_id == int(search_entry[1:]):
                    if search_entry[0] == 'a':
                        print('here')
                        result = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE MemberAID={}".format(int(search_entry[1:])))
                        memberSelect.insert('end', "ID: a{}. {} | {}".format(result[0][0], result[0][1], churches_dict[int(result[0][2])]))
                        return None
                    elif search_entry[0] == 'c':
                        try:
                            result = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild WHERE MemberCID={}".format(int(search_entry[1:])))
                            print(result)
                            memberSelect.insert('end', "ID: c{}. {} | {}".format(result[0][0], result[0][1], churches_dict[0][int(result[2])]))
                            return None
                        except:
                            messagebox.showerror("Error", "There was an issue executing the command")
                            return None
            
            return None

        property_dict = {
            "Full Name": "FullName",
            "Occupation": "Occupation",
            "DOB": "DOB",
            "Phone Number": "PhoneNum",
            "Email": "Email",
            "RoleID": "RoleID"
        }

        # Searching Adult
        result1 = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for memberid, fullname, churchid in result1:
                for person in t_adults_list:
                    if person.member_id == memberid:
                        memberSelect.insert('end', "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

       
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')


def searchFunctionGroups(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    
    groups = sql_select("SELECT EGroupID, EGroupName, EGroupMembers FROM EmailGroups")
    groups_dict = {}
    for groupid, groupname, groupmembers in groups:
        groups_dict["ID: {} | Group Name: {}".format(groupid, groupname)] = groupmembers

    def fill_listbox():
        memberSelect.delete(0, 'end')
        # mAdults = sql_select("SELECT * FROM MembersAdult")
        # mChilds = sql_select("SELECT * FROM MembersChild")
        for group in groups_dict:
            memberSelect.insert('end', group)


    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Group Name")
    search_choices = ["Group Name"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)

        # Searching Groups
        for item in groups_dict:
            if searchEntry.get().upper() in item.upper():
                memberSelect.insert('end', item)
       
    searchButton = tkinter.Button(searchFrame, text="Search Groups", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return groups_dict


def searchFunctionBaptism(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    baptism_inf_dict = {}
    
    def fill_listbox():
        memberSelect.delete(0, 'end')

        baptisms = sql_select("SELECT * FROM Baptism ORDER BY BaptismID DESC")

        for baptismid, childname, status, churchid, dateofbaptism, timeofbaptism, clergyid, contactnumber, notes in baptisms:
            text = "Baptism ID: {} | Child Name: {} | Clergy Member: {} | Status: {} | Date of Baptism: {} | Contact Number: {}".format(baptismid, childname, clergyid, status, dateofbaptism, contactnumber)
            baptism_inf_dict[text] = [baptismid, childname, status, churchid, dateofbaptism, timeofbaptism, clergyid, contactnumber, notes]

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Child Name")
    search_choices = ["Child Name", "Status", "Date of Baptism", "Contact Number"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
       
        property_dict = {
            "Child Name": "ChildName",
            "Status": "Status",
            "Date of Baptism": "DateOfBaptism",
            "Contact Number": "ContactNumber"
        }

        # Searching Baptism
        result1 = sql_select("SELECT BaptismID, ChildName, Status, ClergyID, DateOfBaptism, ContactNumber FROM Baptism WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for baptismid, childname, status, clergyid, dateofbaptism, contactnumber in result1:
                memberSelect.insert('end', "Baptism ID: {} | Child Name: {} | Clergy Member: {} | Status: {} | Date of Baptism: {} | Contact Number: {}".format(baptismid, childname, clergyid, status, dateofbaptism, contactnumber))

       
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return baptism_inf_dict


def searchFunctionFuneral(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    funeral_inf_dict = {}
    
    def fill_listbox():
        memberSelect.delete(0, 'end')

        funerals = sql_select("SELECT * FROM Funeral ORDER BY FuneralID DESC")

        for funeralid, decname, status, churchid, dateoffuneral, timeoffuneral, clergyid, contactnumber, notes in funerals:
            text = "Funeral ID: {} | Name of Deceased: {} | Clergy Member: {} | Status: {} | Date of Funeral: {} | Contact Number: {}".format(funeralid, decname, clergyid, status, dateoffuneral, contactnumber)
            funeral_inf_dict[text] = [funeralid, decname, status, churchid, dateoffuneral, timeoffuneral, clergyid, contactnumber, notes]

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Name of Deceased")
    search_choices = ["Name of Deceased", "Status", "Date of Funeral", "Contact Number"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
       
        property_dict = {
            "Name of Deceased": "DeceasedName",
            "Status": "Status",
            "Date of Funeral": "DateOfFuneral",
            "Contact Number": "ContactNumber"
        }

        # Searching Baptism
        result1 = sql_select("SELECT FuneralID, DeceasedName, Status, ClergyID, DateOfFuneral, ContactNumber FROM Funeral WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for funeralid, decname, status, clergyid, dateoffuneral, contactnumber in result1:
                memberSelect.insert('end', "Funeral ID: {} | Name of Deceased: {} | Clergy Member: {} | Status: {} | Date of Funeral: {} | Contact Number: {}".format(funeralid, decname, clergyid, status, dateoffuneral, contactnumber))

       
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return funeral_inf_dict


def searchFunctionHC(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    hc_inf_dict = {}
    
    def fill_listbox():
        memberSelect.delete(0, 'end')

        holyCommunions = sql_select("SELECT * FROM HolyCommunion ORDER BY HCID DESC")

        for hcid, comname, status, churchid, dateofhc, timeofhc, clergyid, contactnumber, notes in holyCommunions:
            text = "Communion ID: {} | Name of Communicant: {} | Clergy Member: {} | Status: {} | Date of Holy Communion: {} | Contact Number: {}".format(hcid, comname, clergyid, status, dateofhc, contactnumber)
            hc_inf_dict[text] = [hcid, comname, status, churchid, dateofhc, timeofhc, clergyid, contactnumber, notes]

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Name of Communicant")
    search_choices = ["Name of Communicant", "Status", "Date of Holy Communion", "Contact Number"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
       
        property_dict = {
            "Name of Communicant": "CommunicantName",
            "Status": "Status",
            "Date of Holy Communion": "DateOfHC",
            "Contact Number": "ContactNumber"
        }

        # Searching Baptism
        result1 = sql_select("SELECT HCID, CommunicantName, Status, ClergyID, DateOfHC, ContactNumber FROM HolyCommunion WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for hcid, comname, status, clergyid, dateofhc, contactnumber in result1:
                memberSelect.insert('end', "Communion ID: {} | Name of Communicant: {} | Clergy Member: {} | Status: {} | Date of Holy Communion: {} | Contact Number: {}".format(hcid, comname, clergyid, status, dateofhc, contactnumber))

       
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return hc_inf_dict


def searchFunctionMarriage(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    marriage_inf_dict = {}
    
    def fill_listbox():
        memberSelect.delete(0, 'end')

        marriages = sql_select("SELECT * FROM Marriage ORDER BY MarriageID DESC")

        for marriageid, groomname, bridename, status, permission, churchid, dateofmarriage, timeofmarriage, clergyid, contactnumber, notes in marriages:
            text = "Marriage ID: {} | Name of Groom: {} | Name of Bride: {} | Clergy Member: {} | Status: {} | Date of Marriage: {} | Contact Number: {}".format(marriageid, groomname, bridename, clergyid, status, dateofmarriage, contactnumber)
            marriage_inf_dict[text] = [marriageid, groomname, bridename, status, permission, churchid, dateofmarriage, timeofmarriage, clergyid, contactnumber, notes]

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Name of Groom")
    search_choices = ["Name of Groom", "Name of Bride", "Date of Marriage", "Contact Number"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
       
        property_dict = {
            "Name of Groom": "GroomName",
            "Name of Bride": "BrideName",
            "Status": "Status",
            "Date of Marriage": "DateOfMarriage",
            "Contact Number": "ContactNumber"
        }

        # Searching Baptism
        result1 = sql_select("SELECT MarriageID, GroomName, BrideName, Status, ClergyID, DateOfMarriage, ContactNumber FROM Marriage WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for marriageid, groomname, bridename, status, clergyid, dateofmarriage, contactnumber in result1:
                memberSelect.insert('end', "Marriage ID: {} | Name of Groom: {} | Name of Bride: {} | Clergy Member: {} | Status: {} | Date of Marriage: {} | Contact Number: {}".format(marriageid, groomname, bridename, clergyid, status, dateofmarriage, contactnumber))

       
    searchButton = tkinter.Button(searchFrame, text="Search Marriage", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return marriage_inf_dict



def searchFunctionUser(memberSelect, container, given_row):
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    user_inf_dict = {}
    
    def fill_listbox():
        memberSelect.delete(0, 'end')

        users = sql_select("SELECT * FROM Users ORDER BY UserID DESC")
        

        for userid, username, useremail, userphone, userlevel, systemname, systempass in users:
            if userlevel == 1:
                userlevel = "Edit"
            else:
                userlevel = "View"
            text = "User ID: {} | Name: {} | Email: {} | Phone: {} | Username: {} | Access Level: {}".format(userid, username, useremail, userphone, systemname, userlevel)
            user_inf_dict[text] = [userid, username, useremail, userphone, userlevel, systemname]

            memberSelect.insert('end', text)

    fill_listbox()


    searchFrame = tkinter.Frame(container, bg=blue)
    searchFrame.grid(row=given_row, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("Name")
    search_choices = ["Name", "Email", "Phone", "Username", "Level"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        memberSelect.delete(0, 'end')
        search_property = search_selection.get()
        search_entry = searchEntry.get()
        print(search_entry)
       
        property_dict = {
            "Name": "UserName",
            "Email": "UserEmail",
            "Phone": "UserPhone",
            "Level": "UserLevel",
            "Username": "SystemName"
        }

        # Searching Baptism
        result1 = sql_select("SELECT * FROM Users WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for userid, username, useremail, userphone, userlevel, systemname, systempass in result1:
                if userlevel == 1:
                    userlevel = "Edit"
                else:
                    userlevel = "View"
                memberSelect.insert('end', "User ID: {} | Name: {} | Email: {} | Phone: {} | Username: {} | Access Level: {}".format(userid, username, useremail, userphone, systemname, userlevel))

       
    searchButton = tkinter.Button(searchFrame, text="Search User", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    return user_inf_dict