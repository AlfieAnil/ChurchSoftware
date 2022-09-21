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
from search_func import searchFunction, id_finder, searchFunctionFamily, person_creator_adult, person_creator_child, church_dict_glob_id, church_dict_glob, adults_list, childrens_list, roles_dict_glob, roles_dict_glob_id, family_dict_glob, church_dict_glob_name, person_update_adult, person_update_child



# Creat Family Function
def createFamilyArea(frame):
    for widget in frame.winfo_children():
        widget.destroy()


    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    # Family Name
    familyNamePrompt = tkinter.Label(container, text="Family Name: ", font=h1, bg=blue, fg="white")
    familyNamePrompt.grid(row=0, column=0, padx=5)

    familyNameEntry = tkinter.Entry(container, font=h2)
    familyNameEntry.grid(row=0, column=1, sticky='ew')

    # Family Address
    familyAddressPrompt = tkinter.Label(container, text="Family Address: ", font=h1, bg=blue, fg="white")
    familyAddressPrompt.grid(row=1, column=0, padx=5)

    familyAddressEntry = tkinter.Entry(container, font=h2)
    familyAddressEntry.grid(row=1, column=1, sticky='ew')




    # Family Notes
    familyNotesPrompt = tkinter.Label(container, text="Notes: ", font=h1, bg=blue, fg="white")
    familyNotesPrompt.grid(row=2, column=0, padx=5)

    familyNotesEntry = tkinter.Text(container, font=h2)
    familyNotesEntry.grid(row=2, column=1, sticky='ew')

    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=familyNotesEntry.yview, bg=blue)
    familyNotesEntry['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=2, column=2, sticky='wns')

    def addFamilyDB():

        family_name = familyNameEntry.get()
        family_notes = familyNotesEntry.get('1.0', 'end')
        family_address = familyAddressEntry.get()

        if len(family_name) == 0 or len(family_notes) == 0 or len(family_address) == 0:
            messagebox.showerror("Error", "Missing Fields")
            return None

        print(family_name, family_notes, family_address)

        date_now = datetime.datetime.now().strftime("%d/%m/%Y")
        print(date_now)

        success = True
        try:
            # sql("INSERT INTO Family (FamilyName, Address, Notes, DateCreated) VALUES ('{}', '{}', '{}', '{}')".format(family_name, family_address, family_notes, date_now))
            sql_items("INSERT INTO Family (FamilyName, Address, Notes, DateCreated) VALUES (%s, %s, %s, %s)", (family_name, family_address, family_notes, date_now))
        except:
            success = False
            messagebox.showerror("Error", "There was a problem creating the Family. Check the internet connection and try again later")

        if success:
            messagebox.showinfo("Success", "Successfully Created Family")
            createFamilyArea(frame)


    createFamilyButton = tkinter.Button(container, text="Create Family", bg=blue, fg="white", font=h1, command=addFamilyDB)
    createFamilyButton.grid(row=3, column=1, sticky='ew')
    

def addMember(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    selectFrame = tkinter.Frame(container, bg=blue)
    selectFrame.grid(row=0, column=0, columnspan=2, sticky='ew')

    def adultInfoCollect():

        collectFrame = tkinter.Frame(selectFrame, bg=blue)
        collectFrame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=15)

        # Member Name
        namePrompt = tkinter.Label(collectFrame, text="Full Name: ", font=h1, bg=blue, fg="white")
        namePrompt.grid(row=1, column=0, pady=10)

        nameEntry = tkinter.Entry(collectFrame, font=h2, width=40)
        nameEntry.grid(row=1, column=1, sticky='ew')

        # DOB
        dobPrompt = tkinter.Label(collectFrame, text="DOB: ", font=h1, bg=blue, fg="white")
        dobPrompt.grid(row=2, column=0, pady=10)

        # dobEntry = tkinter.Entry(collectFrame, font=h1, bg=blue, fg="white", width=20, state='disabled')
        # dobEntry.grid(row=2, column=1, sticky='ew')

        dobEntry = tkinter.StringVar()
        cal = DateEntry(collectFrame, font=h2, selectmode='day', textvariable=dobEntry, date_pattern='dd/MM/yyyy')
        cal.grid(row=2, column=1, sticky='ew')

        def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
                calendar_window = tkinter.Tk()

                calendar = Calendar(calendar_window, font="Arial", selectmode='day')
                calendar.grid(row=0, column=0, sticky='ew')

                def return_date():
                    print("Function Date: ", calendar.selection_get())
                    selected_date = calendar.selection_get()
                    date = selected_date.strftime("%d/%m/%Y")

                    dobEntry['state'] = 'normal'
                    dobEntry.delete(0, 'end')

                    dobEntry.insert(0, str(date))
                    dobEntry['state'] = 'disabled'

                    calendar_window.destroy()
                
                tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

        # dob_selector = tkinter.Button(collectFrame, text="Select Date", command=select_dob_calendar)
        # dob_selector.grid(row=2, column=2, sticky='e', padx=5)

        # cal = DateEntry(collectFrame, selectmode='day')
        # cal.grid(row=2, column=2, sticky='e', padx=5)

        # Church select
        churchPrompt = tkinter.Label(collectFrame, text="Church: ", bg=blue, fg="white", font=h1)
        churchPrompt.grid(row=3, column=0, pady=10)

        church_selection = StringVar(collectFrame)
        church_dictionary = church_dict_glob_id
        church_list = []
        churches = sql_select("SELECT * FROM Churches")
        # for id, churchName in churches:
        #     church_dictionary["ID: {} Church Name: {}".format(id, churchName)] = id 
        #     church_list.append("ID: {} Church Name: {}".format(id, churchName))

        for church in church_dictionary:
            church_list.append(church)
        
        print(church_dictionary)

        church_selection.set(church_list[0])
        church_choices = church_list
        churchSelector = OptionMenu(collectFrame, church_selection, *church_choices)
        churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
        churchSelector.grid(row=3, column=1, sticky='ew')

        # Role Insert
        rolePrompt = tkinter.Label(collectFrame, text="Roles", fg="white", bg=blue, font=h1)
        rolePrompt.grid(row=4, column=0, pady=10)

        role_selection = StringVar(collectFrame)
        role_dictionary = {}
        role_id_dictionary = {}
        role_list = []
        roles = sql_select("SELECT * FROM Roles")
        selected_roles = []

        for id, rolename, description in roles:
            role_dictionary["{}, {}".format(rolename, description)] = rolename
            role_list.append("{}, {}".format(rolename, description))
            role_id_dictionary[rolename] = id

        role_selection.set('None')
        role_list.append('None')
        role_choices = role_list
        
        roleSelector = OptionMenu(collectFrame, role_selection, *role_choices)
        roleSelector.config(bg=blue, fg="white", padx=5, font=h2)
        roleSelector.grid(row=4, column=1, sticky='ew')

        def addSelRole():
            new_role = role_selection.get()
            print(new_role)
            print(selected_roles)
            if new_role == "None":
                selected_roles.clear()
                roleShower['text'] = "\n".join(selected_roles)
                return None

            if role_dictionary[new_role] in selected_roles:
                    return None
                 
            selected_roles.append(role_dictionary[new_role])

            roleShower['text'] = "\n".join(selected_roles)


        roleAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Role", command=addSelRole)
        roleAdder.grid(row=4, column=2, sticky='ew')

        roleShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
        roleShower.grid(row=5, column=1, sticky='ew')

        # Occupation
        occupationPrompt = tkinter.Label(collectFrame, text="Occupation", fg="white", bg=blue, font=h1)
        occupationPrompt.grid(row=6, column=0, pady=10)

        occupationEntry = tkinter.Entry(collectFrame, font=h2)
        occupationEntry.grid(row=6, column=1, sticky='ew')

        # Gender
        gender_selection = StringVar(collectFrame)
        gender_selection.set("M")
        gender_choices = ["M", "F"]

        genderPrompt = tkinter.Label(collectFrame, text="Gender: ", fg="white", bg=blue, font=h1)
        genderPrompt.grid(row=7, column=0, pady=10)

        genderSelector = OptionMenu(collectFrame, gender_selection, *gender_choices)
        genderSelector.config(bg=blue, fg="white", padx=5, font=h2)
        genderSelector.grid(row=7, column=1, sticky='ew')

        # Marital Status
        maritalPrompt = tkinter.Label(collectFrame, text="Marital Status: ", bg=blue, fg="white", font=h1)
        maritalPrompt.grid(row=8, column=0, pady=10)

        marital_selection = StringVar(collectFrame)
        marital_selection.set("Single")
        marital_choices = ["Single", "Married", "Divorced"]

        maritalSelector = OptionMenu(collectFrame, marital_selection, *marital_choices)
        maritalSelector.config(bg=blue, fg="white", padx=5, font=h2)
        maritalSelector.grid(row=8, column=1, sticky='ew')

        # Phone Number
        phonePrompt = tkinter.Label(collectFrame, text="Phone Number: ", fg="white", bg=blue, font=h1)
        phonePrompt.grid(row=9, column=0, pady=10)

        phoneEntry = tkinter.Entry(collectFrame, font=h2)
        phoneEntry.grid(row=9, column=1, sticky='ew')

        # Email Address
        emailPrompt = tkinter.Label(collectFrame, text="Email Address: ", fg="white", bg=blue, font=h1)
        emailPrompt.grid(row=10, column=0, pady=10)

        emailEntry = tkinter.Entry(collectFrame, font=h2)
        emailEntry.grid(row=10, column=1, sticky='ew')

        # DBS
        dbsPrompt = tkinter.Label(collectFrame, text="DBS: ", fg="white", bg=blue, font=h1)
        dbsPrompt.grid(row=11, column=0, pady=10)

        dbs_selection = StringVar(collectFrame)
        dbs_selection.set("N")
        dbs_choices = ["Y", "N"]

        dbsSelector = OptionMenu(collectFrame, dbs_selection, *dbs_choices)
        dbsSelector.config(bg=blue, fg="white", padx=5, font=h2)
        dbsSelector.grid(row=11, column=1, sticky='ew')

        

            

        # Family Select
        familyPrompt = tkinter.Label(collectFrame, text="Family: ", bg=blue, fg="white", font=h1)
        familyPrompt.grid(row=12, column=0, pady=10)

        family_dict={}

        def familySelector():
            familyWin = tkinter.Tk()
            familyWin.title("Family Finder")
            # familyWin.geometry('910x340')

            familyListbox = tkinter.Listbox(familyWin, width=100, height=15, font=h2)
            familyListbox.grid(row=0, column=0, sticky='ew')

            horizontal_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.HORIZONTAL, command=familyListbox.xview)
            familyListbox['xscrollcommand'] = horizontal_scrollbar.set
            horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

            vertical_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.VERTICAL, command=familyListbox.yview)
            familyListbox['yscrollcommand'] = vertical_scrollbar.set
            vertical_scrollbar.grid(row=0, column=0, sticky='ens')

            familyWin.geometry("")

            families = sql_select("SELECT * FROM Family")
            familyListbox.insert('end', 'Individual')
            for familyId, familyName, familyNotes, dateCreated, address in families:
                family_dict["Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")] = familyId
                familyListbox.insert('end', "Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated))
                print(family_dict)
            def getFamily():
                if len(familyListbox.get(tkinter.ANCHOR)) == 0:
                    messagebox.showerror("Error", "Please select a family to continue")
                    return None
                
                else:
                    familyButton['text'] = familyListbox.get(tkinter.ANCHOR)
                    familyWin.destroy()

            familySelectButton = tkinter.Button(familyWin, text="Select Family", bg=blue, fg="white", font=h2, command=getFamily)
            familySelectButton.grid(row=2, column=0, sticky='ew')

            familyWin.mainloop()

        familyButton = tkinter.Button(collectFrame, text="Find Family", bg=blue, fg="white", font=h2, command=familySelector)
        familyButton.grid(row=12, column=1, sticky='ew')

        # Religion

        religionPrompt = tkinter.Label(collectFrame, text="Religion: ", bg=blue, fg="white", font=h1)
        religionPrompt.grid(row=13, column=0, sticky='ew')

        religion_selection = StringVar(collectFrame)
        religion_selection.set("Roman Catholic")
        religion_choices = ["Roman Catholic", "Church of England", "Orthodox", "Other Christian (Protestant)", "Non-Christian", "None"]

        religionSelector = OptionMenu(collectFrame, religion_selection, *religion_choices)
        religionSelector.config(bg=blue, fg="white", font=h2)
        religionSelector.grid(row=13, column=1, sticky='ew', pady=5)

        # Additional Notes

        notesPrompt = tkinter.Label(collectFrame, text="Additional Notes", font=h1, bg=blue, fg="white")
        notesPrompt.grid(row=14, column=0)

        notesEntry = tkinter.Text(collectFrame, font=h2)
        notesEntry.grid(row=14, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(collectFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
        notesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=14, column=2, sticky='wns')

        # Add member button
        def addMemberDB():
            member_name = nameEntry.get()
            member_dob = dobEntry.get()
            member_church = church_selection.get()
            member_roles = selected_roles
            member_occupation = occupationEntry.get()
            member_gender = gender_selection.get()
            member_marital = marital_selection.get()
            member_phone = phoneEntry.get()
            member_email = emailEntry.get()
            member_dbs = dbs_selection.get()
            member_religion = religion_selection.get()
            member_family = None
            
            try:
                if 'Individual' in familyButton['text']:
                    member_family = 0
                else:
                    member_family = family_dict[familyButton['text'].replace("\n", "")]
            except:
                messagebox.showerror("Error", "Please click the 'Find Family' Buttton and make a selection from the List")
                return None

            member_notes = notesEntry.get('1.0', 'end')

            print(member_name, member_dob, member_church, member_roles, member_occupation, member_gender, member_marital, member_phone, member_email, member_phone, member_dbs, member_family, member_notes)

            if not check_name(member_name):
                return None
            
            if not check_dob(member_dob):
                return None
            
            if len(member_occupation) == 0:
                messagebox.showerror("Error", "Please fill in the Occupation Field")
                return None

            if len(member_phone) != 11:
                messagebox.showerror("Error", "Please enter a valid phone number")
                return None
            
            if not check_email(member_email):
                return None

            if member_family == "Find Family":
                messagebox.showerror("Error", "Please press the 'Find Family' Button and select from the list")
                return None

            selected_roles_ids = []

            for role in selected_roles:
                selected_roles_ids.append(role_id_dictionary[role])

            commit_question = askyesno(title="Confirmation", message="Are you sure you want to add this Member to the Database?")
            if commit_question:
                try:
                    sql_items("INSERT INTO MembersAdult (FullName, DOB, ChurchID, RoleID, Occupation, Gender, MaritalStatus, PhoneNum, Email, DBS, FamilyID, AdditionalNotes, Religion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (member_name, member_dob, int(church_dictionary[member_church]), ', '.join(str(v) for v in selected_roles_ids), member_occupation, member_gender, member_marital, str(member_phone), member_email, member_dbs, member_family, member_notes, member_religion))
                except:
                    messagebox.showerror("Error", "There was a problem adding this member to the database. Check your connection and try again later")
                    return None

                messagebox.showinfo("Success", "Successfully added {} to the Database".format(member_name))

                try:
                    member_aid = sql_select("SELECT MemberAID FROM MembersAdult ORDER BY MemberAID DESC")
                    person_creator_adult(member_aid[0][0], member_name, member_dob, church_dict_glob_id[member_church], ', '.join(str(v) for v in selected_roles_ids), member_occupation, member_gender, member_marital, member_phone, member_email, member_dbs, member_family, member_notes, member_religion)

                except:
                    messagebox.showerror("Error", "Unfortunately you will have to restart the application to ensure the validity of data in the database. Sorry for the Inconvenience")
                    return None
                
                adultInfoCollect()

            

                



        addMemberButton = tkinter.Button(collectFrame, text="Add Member", fg="white", bg=blue, font=h1, command=addMemberDB)
        addMemberButton.grid(row=15, column=1, sticky='ew')
        

                
        



    adultButton = tkinter.Button(selectFrame, text="Adult", bg=blue, width=25, font=h1, fg="white", command=adultInfoCollect)
    adultButton.grid(row=0, column=0)

    def childInfoCollect():

        for widget in selectFrame.winfo_children():
            widget.destroy()

        adultButton = tkinter.Button(selectFrame, text="Adult", bg=blue, width=25, font=h1, fg="white", command=adultInfoCollect)
        adultButton.grid(row=0, column=0)

        childButton = tkinter.Button(selectFrame, text="Child", bg=blue, width=25, font=h1, fg="white", command=childInfoCollect)
        childButton.grid(row=0, column=1)

        collectFrame = tkinter.Frame(selectFrame, bg=blue)
        collectFrame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=15)

        # Member Name
        namePrompt = tkinter.Label(collectFrame, text="Full Name: ", font=h1, bg=blue, fg="white")
        namePrompt.grid(row=1, column=0, pady=10)

        nameEntry = tkinter.Entry(collectFrame, font=h2, width=40)
        nameEntry.grid(row=1, column=1, sticky='ew')

        # DOB
        dobPrompt = tkinter.Label(collectFrame, text="DOB: ", font=h1, bg=blue, fg="white")
        dobPrompt.grid(row=2, column=0, pady=10)

        dobEntry = tkinter.StringVar()
        cal = DateEntry(collectFrame, font=h2, selectmode='day', textvariable=dobEntry, date_pattern='dd/MM/yyyy')
        cal.grid(row=2, column=1, sticky='ew')

        def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
                calendar_window = tkinter.Tk()

                calendar = Calendar(calendar_window, font="Arial", selectmode='day')
                calendar.grid(row=0, column=0, sticky='ew')

                def return_date():
                    print("Function Date: ", calendar.selection_get())
                    selected_date = calendar.selection_get()
                    date = selected_date.strftime("%d/%m/%Y")

                    dobEntry['state'] = 'normal'
                    dobEntry.delete(0, 'end')

                    dobEntry.insert(0, str(date))
                    dobEntry['state'] = 'disabled'

                    calendar_window.destroy()
                
                tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

        # dob_selector = tkinter.Button(collectFrame, text="Select Date", command=select_dob_calendar)
        # dob_selector.grid(row=2, column=2, sticky='e', padx=5)

        # Gender
        gender_selection = StringVar(collectFrame)
        gender_selection.set("M")
        gender_choices = ["M", "F"]

        genderPrompt = tkinter.Label(collectFrame, text="Gender: ", fg="white", bg=blue, font=h1)
        genderPrompt.grid(row=3, column=0, pady=10)

        genderSelector = OptionMenu(collectFrame, gender_selection, *gender_choices)
        genderSelector.config(bg=blue, fg="white", padx=5, font=h2)
        genderSelector.grid(row=3, column=1, sticky='ew')

        # Church select
        churchPrompt = tkinter.Label(collectFrame, text="Church: ", bg=blue, fg="white", font=h1)
        churchPrompt.grid(row=4, column=0, pady=10)

        church_selection = StringVar(collectFrame)
        church_dictionary = church_dict_glob_id
        church_list = []
        churches = sql_select("SELECT * FROM Churches")

        for church in church_dictionary:
            church_list.append(church)

        print(church_dictionary)

        church_selection.set(church_list[0])
        church_choices = church_list
        churchSelector = OptionMenu(collectFrame, church_selection, *church_choices)
        churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
        churchSelector.grid(row=4, column=1, sticky='ew')

        # Role Insert
        rolePrompt = tkinter.Label(collectFrame, text="Roles:", fg="white", bg=blue, font=h1)
        rolePrompt.grid(row=5, column=0, pady=10)

        role_selection = StringVar(collectFrame)
        role_dictionary = {}
        role_id_dictionary = {}
        role_list = []
        roles = sql_select("SELECT * FROM Roles")
        selected_roles = []

        for id, rolename, description in roles:
            role_dictionary["{}, {}".format(rolename, description)] = rolename
            role_list.append("{}, {}".format(rolename, description))
            role_id_dictionary[rolename] = id

        role_selection.set('None')
        role_list.append('None')
        role_choices = role_list
        
        roleSelector = OptionMenu(collectFrame, role_selection, *role_choices)
        roleSelector.config(bg=blue, fg="white", padx=5, font=h2)
        roleSelector.grid(row=5, column=1, sticky='ew')

        def addSelRole():
            new_role = role_selection.get()
            print(new_role)
            print(selected_roles)
            if new_role == "None":
                selected_roles.clear()
                roleShower['text'] = "\n".join(selected_roles)
                return None

            if role_dictionary[new_role] in selected_roles:
                    return None
                 
            selected_roles.append(role_dictionary[new_role])

            roleShower['text'] = "\n".join(selected_roles)


        roleAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Role", command=addSelRole)
        roleAdder.grid(row=5, column=2, sticky='ew')

        roleShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
        roleShower.grid(row=6, column=1, sticky='ew')


        # School prompt
        schoolPrompt = tkinter.Label(collectFrame, bg=blue, text="School (if applicable):", fg="white", font=h1)
        schoolPrompt.grid(row=7, column=0)

        schoolEntry = tkinter.Entry(collectFrame, font=h2)
        schoolEntry.grid(row=7, column=1, sticky='ew')

        # Sacraments Received
        sacramentPrompt = tkinter.Label(collectFrame, text="Sacraments", fg="white", bg=blue, font=h1)
        sacramentPrompt.grid(row=8, column=0, pady=10)

        sacrament_selection = StringVar(collectFrame)
        sacrament_dictionary = {}
        sacrament_choices = ['None', 'Baptism', 'Reconciliation', 'Holy Communion', 'Confirmation']
        selected_sacraments = []

        sacrament_selection.set('None')
        
        sacramentSelector = OptionMenu(collectFrame, sacrament_selection, *sacrament_choices)
        sacramentSelector.config(bg=blue, fg="white", padx=5, font=h2)
        sacramentSelector.grid(row=8, column=1, sticky='ew')

        def addSelSacrament():
            new_sacrament = sacrament_selection.get()
            if new_sacrament == "None":
                selected_sacraments.clear()
                sacramentShower['text'] = "\n".join(selected_roles)
                return None

            if new_sacrament in selected_sacraments:
                return None
                 
            selected_sacraments.append(new_sacrament)

            sacramentShower['text'] = "\n".join(selected_sacraments)


        sacramentAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Sacrament", command=addSelSacrament)
        sacramentAdder.grid(row=8, column=2, sticky='ew')

        sacramentShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
        sacramentShower.grid(row=9, column=1, sticky='ew', pady=10)

        # Church of Baptism
        cBaptismPrompt = tkinter.Label(collectFrame, text="Church of Baptism: ", bg=blue, fg="white", font=h1)
        cBaptismPrompt.grid(row=10, column=0)

        cBaptismEntry = tkinter.Entry(collectFrame, font=h2)
        cBaptismEntry.grid(row=10, column=1, sticky='ew')

        # Family Select
        familyPrompt = tkinter.Label(collectFrame, text="Family: ", bg=blue, fg="white", font=h1)
        familyPrompt.grid(row=11, column=0, pady=10)

        family_dict={}

        def familySelector():
            familyWin = tkinter.Tk()
            familyWin.title("Family Finder")
            # familyWin.geometry('910x340')

            familyListbox = tkinter.Listbox(familyWin, width=100, height=15, font=h2)
            familyListbox.grid(row=0, column=0, sticky='ew')

            horizontal_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.HORIZONTAL, command=familyListbox.xview)
            familyListbox['xscrollcommand'] = horizontal_scrollbar.set
            horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

            vertical_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.VERTICAL, command=familyListbox.yview)
            familyListbox['yscrollcommand'] = vertical_scrollbar.set
            vertical_scrollbar.grid(row=0, column=0, sticky='ens')


            
            families = sql_select("SELECT * FROM Family")
            familyListbox.insert('end', 'Individual')
            for familyId, familyName, familyNotes, dateCreated, address in families:
                family_dict["Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")] = familyId
                familyListbox.insert('end', "Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated))
                print(family_dict)
            def getFamily():
                if len(familyListbox.get(tkinter.ANCHOR)) == 0:
                    messagebox.showerror("Error", "Please select a family to continue")
                    return None
                
                else:
                    familyButton['text'] = familyListbox.get(tkinter.ANCHOR)
                    familyWin.destroy()

            familySelectButton = tkinter.Button(familyWin, text="Select Family", bg=blue, fg="white", font=h2, command=getFamily)
            familySelectButton.grid(row=2, column=0, sticky='ew')

            familyWin.mainloop()

        familyButton = tkinter.Button(collectFrame, text="Find Family", bg=blue, fg="white", font=h2, command=familySelector)
        familyButton.grid(row=11, column=1, sticky='ew')

        # Religion

        religionPrompt = tkinter.Label(collectFrame, text="Religion: ", bg=blue, fg="white", font=h1)
        religionPrompt.grid(row=12, column=0, sticky='ew')

        religion_selection = StringVar(collectFrame)
        religion_selection.set("Roman Catholic")
        religion_choices = ["Roman Catholic", "Church of England", "Orthodox", "Other Christian (Protestant)", "Non-Christian", "None"]

        religionSelector = OptionMenu(collectFrame, religion_selection, *religion_choices)
        religionSelector.config(bg=blue, fg="white", font=h2)
        religionSelector.grid(row=12, column=1, sticky='ew', pady=5)

        # Additional Notes

        notesPrompt = tkinter.Label(collectFrame, text="Additional Notes:", font=h1, bg=blue, fg="white")
        notesPrompt.grid(row=13, column=0)

        notesEntry = tkinter.Text(collectFrame, font=h2)
        notesEntry.grid(row=13, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(collectFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
        notesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=13, column=2, sticky='wns')

        # Add Child Button

        def addChildMember():
            member_name = nameEntry.get()
            member_dob = dobEntry.get()
            member_church = church_selection.get()
            member_school = schoolEntry.get()
            member_gender = gender_selection.get()
            member_sacraments = selected_sacraments
            if len(selected_sacraments) == 0:
                member_sacraments.append("None")
            member_baptism_church = cBaptismEntry.get()
            member_family = None
            member_notes = notesEntry.get('1.0', 'end')
            member_religion = religion_selection.get()

            print(member_name, member_dob, member_church, member_school, member_sacraments, member_baptism_church, member_family, member_notes)
            
            try:
                if 'Individual' in familyButton['text']:
                    member_family = 0
                else:
                    member_family = family_dict[familyButton['text'].replace("\n", "")]
            except:
                messagebox.showerror("Error", "Please click the 'Find Family' Buttton and make a selection from the List")
                return None
            
            selected_roles_ids = []

            for role in selected_roles:
                selected_roles_ids.append(role_id_dictionary[role])

            if len(member_dob) == 0:
                messagebox.showerror("Error", "Please enter the Date of Birth")
                return None
            
            if not check_name(member_name):
                return None
            
            if not check_dob_child(member_dob):
                return None

            
            commit_question = askyesno(title="Confirmation", message="Are you sure you want to add this Member to the Database?")
            if commit_question:
                success = True
                try:
                    sql_items("INSERT INTO MembersChild (FullName, DOB, School, SacramentsReceived, ChurchOfBaptism, RoleID, FamilyID, Notes, ChurchID, Gender, Religion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (member_name, member_dob, member_school, ', '.join(selected_sacraments), member_baptism_church, ', '.join(str(v) for v in selected_roles_ids), member_family, member_notes, int(church_dictionary[member_church]), member_gender, member_religion))
                except Exception as e:
                    print(e)
                    success = False
                    messagebox.showerror("Error", "Failed to add child to Database")
                    return None

                if success:
                    messagebox.showinfo("Success", "Successfully added child to Database")

                    try:
                        member_cid = sql_select("SELECT MemberCID FROM MembersChild ORDER BY MemberCID DESC")
                        person_creator_child(member_cid[0][0], member_name, member_dob, member_school, member_sacraments, member_baptism_church, ', '.join(str(v) for v in selected_roles_ids), member_family, member_notes, int(church_dictionary[member_church]), member_gender, member_religion)

                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Unfortunately you will have to restart the application to ensure the validity of data in the database. Sorry for the Inconvenience")
                        return None

                    childInfoCollect()



        addChildButton = tkinter.Button(collectFrame, text="Add Child Member", fg="white", bg=blue, font=h1, command=addChildMember)
        addChildButton.grid(row=14, column=1, sticky='ew')




    childButton = tkinter.Button(selectFrame, text="Child", bg=blue, width=25, font=h1, fg="white", command=childInfoCollect)
    childButton.grid(row=0, column=1)


# Edit Members
def editMember(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    h0 = tkFont.Font(family='Helvetica', size=14, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    selectPrompt = tkinter.Label(container, text="Select Member to Edit/Delete", fg="white", bg=blue, font=h0)
    selectPrompt.grid(row=0, column=0, sticky='ew')

    memberSelect = tkinter.Listbox(container, width=110, height=15, font=h2)
    memberSelect.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=memberSelect.xview)
    memberSelect['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=memberSelect.yview)
    memberSelect['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    def editMemberDetails(editFrame):
        memberEdit = memberSelect.get(tkinter.ANCHOR)
        print("Member to edit: ", memberEdit)

        def editDetailFrame(member_id, category, full_name, collectFrame):
            if category == 'a':
                # Member Name
                namePrompt = tkinter.Label(collectFrame, text="Full Name: ", font=h1, bg=blue, fg="white")
                namePrompt.grid(row=1, column=0, pady=10)

                nameEntry = tkinter.Entry(collectFrame, font=h2, width=40)
                nameEntry.grid(row=1, column=1, sticky='ew')

                # DOB
                dobPrompt = tkinter.Label(collectFrame, text="DOB: ", font=h1, bg=blue, fg="white")
                dobPrompt.grid(row=2, column=0, pady=10)

                dobEntry = tkinter.StringVar()
                cal = DateEntry(collectFrame, font=h2, selectmode='day', textvariable=dobEntry, date_pattern='dd/MM/yyyy')
                cal.grid(row=2, column=1, sticky='ew')

                def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
                        calendar_window = tkinter.Tk()

                        calendar = Calendar(calendar_window, font="Arial", selectmode='day')
                        
                        calendar.grid(row=0, column=0, sticky='ew')

                        def return_date():
                            print("Function Date: ", calendar.selection_get())
                            selected_date = calendar.selection_get()
                            date = selected_date.strftime("%d/%m/%Y")

                            dobEntry.delete(0, 'end')

                            dobEntry.insert(0, str(date))

                            calendar_window.destroy()
                        
                        tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

                # dob_selector = tkinter.Button(collectFrame, text="Select Date", command=select_dob_calendar)
                # dob_selector.grid(row=2, column=2, sticky='e', padx=5)

                # Church select
                churchPrompt = tkinter.Label(collectFrame, text="Church: ", bg=blue, fg="white", font=h1)
                churchPrompt.grid(row=3, column=0, pady=10)

                church_selection = StringVar(collectFrame)
                church_dictionary = church_dict_glob_id
                church_list = []
                for church in church_dictionary:
                    church_list.append(church)
                
                print(church_dictionary)

                church_selection.set(church_list[0])
                church_choices = church_list
                churchSelector = OptionMenu(collectFrame, church_selection, *church_choices)
                churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
                churchSelector.grid(row=3, column=1, sticky='ew')

                # Role Insert
                rolePrompt = tkinter.Label(collectFrame, text="Roles", fg="white", bg=blue, font=h1)
                rolePrompt.grid(row=4, column=0, pady=10)

                role_selection = StringVar(collectFrame)
                role_dictionary = roles_dict_glob
                role_id_dictionary = roles_dict_glob_id
                role_list = []
                # roles = sql_select("SELECT * FROM Roles")
                selected_roles = []

                # for id, rolename, description in roles:
                #     role_dictionary["{}, {}".format(rolename, description)] = rolename
                #     role_list.append("{}, {}".format(rolename, description))
                #     role_id_dictionary[rolename] = id

                for role in roles_dict_glob:
                    role_list.append(role)

                role_selection.set('None')
                role_list.append('None')
                role_choices = role_list
                
                roleSelector = OptionMenu(collectFrame, role_selection, *role_choices)
                roleSelector.config(bg=blue, fg="white", padx=5, font=h2)
                roleSelector.grid(row=4, column=1, sticky='ew')

                def addSelRole():
                    new_role = role_selection.get()
                    print(new_role)
                    print(selected_roles)
                    if new_role == "None":
                        selected_roles.clear()
                        roleShower['text'] = "\n".join(selected_roles)
                        return None

                    if role_dictionary[new_role] in selected_roles:
                            return None
                        
                    selected_roles.append(role_dictionary[new_role])

                    roleShower['text'] = "\n".join(selected_roles)


                roleAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Role", command=addSelRole)
                roleAdder.grid(row=4, column=2, sticky='ew')

                roleShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
                roleShower.grid(row=5, column=1, sticky='ew')

                # Occupation
                occupationPrompt = tkinter.Label(collectFrame, text="Occupation", fg="white", bg=blue, font=h1)
                occupationPrompt.grid(row=6, column=0, pady=10)

                occupationEntry = tkinter.Entry(collectFrame, font=h2)
                occupationEntry.grid(row=6, column=1, sticky='ew')

                # Gender
                gender_selection = StringVar(collectFrame)
                gender_selection.set("M")
                gender_choices = ["M", "F"]

                genderPrompt = tkinter.Label(collectFrame, text="Gender: ", fg="white", bg=blue, font=h1)
                genderPrompt.grid(row=7, column=0, pady=10)

                genderSelector = OptionMenu(collectFrame, gender_selection, *gender_choices)
                genderSelector.config(bg=blue, fg="white", padx=5, font=h2)
                genderSelector.grid(row=7, column=1, sticky='ew')

                # Marital Status
                maritalPrompt = tkinter.Label(collectFrame, text="Marital Status: ", bg=blue, fg="white", font=h1)
                maritalPrompt.grid(row=8, column=0, pady=10)

                marital_selection = StringVar(collectFrame)
                marital_selection.set("Single")
                marital_choices = ["Single", "Married", "Divorced"]

                maritalSelector = OptionMenu(collectFrame, marital_selection, *marital_choices)
                maritalSelector.config(bg=blue, fg="white", padx=5, font=h2)
                maritalSelector.grid(row=8, column=1, sticky='ew')

                # Phone Number
                phonePrompt = tkinter.Label(collectFrame, text="Phone Number: ", fg="white", bg=blue, font=h1)
                phonePrompt.grid(row=9, column=0, pady=10)

                phoneEntry = tkinter.Entry(collectFrame, font=h2)
                phoneEntry.grid(row=9, column=1, sticky='ew')

                # Email Address
                emailPrompt = tkinter.Label(collectFrame, text="Email Address: ", fg="white", bg=blue, font=h1)
                emailPrompt.grid(row=10, column=0, pady=10)

                emailEntry = tkinter.Entry(collectFrame, font=h2)
                emailEntry.grid(row=10, column=1, sticky='ew')

                # DBS
                dbsPrompt = tkinter.Label(collectFrame, text="DBS: ", fg="white", bg=blue, font=h1)
                dbsPrompt.grid(row=11, column=0, pady=10)

                dbs_selection = StringVar(collectFrame)
                dbs_selection.set("N")
                dbs_choices = ["Y", "N"]

                dbsSelector = OptionMenu(collectFrame, dbs_selection, *dbs_choices)
                dbsSelector.config(bg=blue, fg="white", padx=5, font=h2)
                dbsSelector.grid(row=11, column=1, sticky='ew')

                

                    

                # Family Select
                familyPrompt = tkinter.Label(collectFrame, text="Family: ", bg=blue, fg="white", font=h1)
                familyPrompt.grid(row=12, column=0, pady=10)

                family_dict=family_dict_glob

                def familySelector():
                    familyWin = tkinter.Tk()
                    familyWin.title("Family Finder")
                    # familyWin.geometry('910x340')

                    familyListbox = tkinter.Listbox(familyWin, width=100, height=15, font=h2)
                    familyListbox.grid(row=0, column=0, sticky='ew')

                    horizontal_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.HORIZONTAL, command=familyListbox.xview)
                    familyListbox['xscrollcommand'] = horizontal_scrollbar.set
                    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

                    vertical_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.VERTICAL, command=familyListbox.yview)
                    familyListbox['yscrollcommand'] = vertical_scrollbar.set
                    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

                    familyWin.geometry("")
                    # families = sql_select("SELECT * FROM Family")
                    familyListbox.insert('end', 'Individual')
                    
                    # for familyId, familyName, familyNotes, dateCreated, address in families:
                    #     family_dict["Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")] = familyId
                    #     familyListbox.insert('end', "Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated))
                    #     print(family_dict)
                    
                    for family in family_dict:
                        familyListbox.insert('end', family)

                    def getFamily():
                        if len(familyListbox.get(tkinter.ANCHOR)) == 0:
                            messagebox.showerror("Error", "Please select a family to continue")
                            return None
                        
                        else:
                            familyButton['text'] = familyListbox.get(tkinter.ANCHOR)
                            familyWin.destroy()

                    familySelectButton = tkinter.Button(familyWin, text="Select Family", bg=blue, fg="white", font=h2, command=getFamily)
                    familySelectButton.grid(row=2, column=0, sticky='ew')

                    familyWin.mainloop()

                familyButton = tkinter.Button(collectFrame, text="Find Family", bg=blue, fg="white", font=h2, command=familySelector)
                familyButton.grid(row=12, column=1, sticky='ew')

                # Religion

                religionPrompt = tkinter.Label(collectFrame, text="Religion: ", bg=blue, fg="white", font=h1)
                religionPrompt.grid(row=13, column=0, sticky='ew')

                religion_selection = StringVar(collectFrame)
                religion_selection.set("Roman Catholic")
                religion_choices = ["Roman Catholic", "Church of England", "Orthodox", "Other Christian (Protestant)", "Non-Christian", "None"]

                religionSelector = OptionMenu(collectFrame, religion_selection, *religion_choices)
                religionSelector.config(bg=blue, fg="white", font=h2)
                religionSelector.grid(row=13, column=1, sticky='ew', pady=5)

                # Additional Notes

                notesPrompt = tkinter.Label(collectFrame, text="Additional Notes", font=h1, bg=blue, fg="white")
                notesPrompt.grid(row=14, column=0)

                notesEntry = tkinter.Text(collectFrame, font=h2)
                notesEntry.grid(row=14, column=1, sticky='ew')

                scrollbar = tkinter.Scrollbar(collectFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
                notesEntry['yscrollcommand'] = scrollbar.set
                scrollbar.grid(row=14, column=2, sticky='wns')

                # Edit Details Button
                def makeChanges():
                    member_name = nameEntry.get()
                    member_dob = dobEntry.get()
                    member_church = church_selection.get()
                    member_roles = selected_roles
                    member_occupation = occupationEntry.get()
                    member_gender = gender_selection.get()
                    member_marital = marital_selection.get()
                    member_phone = phoneEntry.get()
                    member_email = emailEntry.get()
                    member_dbs = dbs_selection.get()
                    member_family = None
                    member_religion = religion_selection.get()
                    
                    try:
                        if 'Individual' in familyButton['text']:
                            member_family = 0
                        else:
                            member_family = family_dict[familyButton['text'].replace("\n", "")]
                    except:
                        messagebox.showerror("Error", "Please click the 'Find Family' Buttton and make a selection from the List")
                        return None

                    member_notes = notesEntry.get('1.0', 'end')

                    print(member_name, member_dob, member_church, member_roles, member_occupation, member_gender, member_marital, member_phone, member_email, member_phone, member_dbs, member_family, member_notes)

                    if not check_name(member_name):
                        return None
                    
                    if not check_dob(member_dob):
                        return None
                    
                    if len(member_occupation) == 0:
                        messagebox.showerror("Error", "Please fill in the Occupation Field")
                        return None

                    if len(member_phone) != 11:
                        messagebox.showerror("Error", "Please enter a valid phone number")
                        return None
                    
                    if not check_email(member_email):
                        return None

                    if member_family == "Find Family":
                        messagebox.showerror("Error", "Please press the 'Find Family' Button and select from the list")
                        return None

                    selected_roles_ids = []

                    for role in selected_roles:
                        selected_roles_ids.append(role_id_dictionary[role])

                    commit_question = askyesno(title="Confirmation", message="Are you sure you want to make changes to this Member's details?")
                    if commit_question:
                        try:
                            sql_items("UPDATE MembersAdult SET FullName=%s, DOB=%s, ChurchID=%s, RoleID=%s, Occupation=%s, Gender=%s, MaritalStatus=%s, PhoneNum=%s, Email=%s, DBS=%s, FamilyID=%s, AdditionalNotes=%s, Religion=%s WHERE MemberAID=%s", (member_name, member_dob, int(church_dictionary[member_church]), ', '.join(str(v) for v in selected_roles_ids), member_occupation, member_gender, member_marital, str(member_phone), member_email, member_dbs, member_family, member_notes, member_religion, member_id))
                        except:
                            messagebox.showerror("Error", "There was a problem making changes to this member's details. Check your connection and try again later")
                            return None

                        messagebox.showinfo("Success", "Successfully made changes to the details of {}".format(member_name))
                        person_update_adult(member_id, member_name, member_dob, int(church_dictionary[member_church]), ', '.join(str(v) for v in selected_roles_ids), member_occupation, member_gender, member_marital, str(member_phone), member_email, member_dbs, member_family, member_notes, member_religion)
                        

                    
                    

                makeChangeButton = tkinter.Button(collectFrame, text="Make Changes", bg=blue, fg="white", command=makeChanges)
                makeChangeButton.grid(row=15, column=1, sticky='ew')
                

                # insert details
                for memberid, fullname, dob, church_id, roleid, occupation, gender, maritalstatus, phonenumber, email, dbs, familyid, additionalnotes, religion in sql_select("SELECT * FROM MembersAdult WHERE MemberAID={}".format(member_id)):
                    nameEntry.insert(0, fullname)
                    
                    # dobEntry.config(state='normal')
                    dobEntry.set(dob)
                    # dobEntry.config(state='disabled')

                    religion_selection.set(religion)

                    for churchvalue, churchid in church_dictionary.items():
                        if churchid == church_id:
                            church_selection.set(churchvalue)

                    if len(roleid) != 0:
                        roles_temp = roleid.split(', ')
                        print("RoleID ", roleid)
                        print("RolesTemp: ", roles_temp)
                        for temp_role_id in roles_temp:
                            try:
                                role_name = sql_select("SELECT RoleName FROM Roles WHERE RoleID={}".format(int(temp_role_id)))[0][0]
                                selected_roles.append(role_name)
                            except:
                                print("none")
                            

                    print(selected_roles)
                    roleShower['text'] = "\n".join(selected_roles) 

                    occupationEntry.insert(0, occupation)

                    gender_selection.set(gender)

                    marital_selection.set(maritalstatus)

                    phoneEntry.insert(0, phonenumber)

                    emailEntry.insert(0, email)

                    dbs_selection.set(dbs)

                    if familyid == 0:
                        familyButton['text'] = "Individual"
                    else:
                        for family in family_dict_glob:
                            if family_dict_glob[family] == familyid:
                                familyButton['text'] = family

                        


                    notesEntry.insert("1.0", additionalnotes)


            if category == 'c':
                # Member Name
                namePrompt = tkinter.Label(collectFrame, text="Full Name: ", font=h1, bg=blue, fg="white")
                namePrompt.grid(row=1, column=0, pady=10)

                nameEntry = tkinter.Entry(collectFrame, font=h2, width=40)
                nameEntry.grid(row=1, column=1, sticky='ew')

                # DOB
                dobPrompt = tkinter.Label(collectFrame, text="DOB: ", font=h1, bg=blue, fg="white")
                dobPrompt.grid(row=2, column=0, pady=10)

                dobEntry = tkinter.StringVar()
                cal = DateEntry(collectFrame, font=h2, selectmode='day', textvariable=dobEntry, date_pattern='dd/MM/yyyy')
                cal.grid(row=2, column=1, sticky='ew')

                def select_dob_calendar(): # opens window to allow the user to select a date from a calendar
                        calendar_window = tkinter.Tk()

                        calendar = Calendar(calendar_window, font="Arial", selectmode='day')
                        calendar.grid(row=0, column=0, sticky='ew')

                        def return_date():
                            print("Function Date: ", calendar.selection_get())
                            selected_date = calendar.selection_get()
                            date = selected_date.strftime("%d/%m/%Y")

                            dobEntry['state'] = 'normal'
                            dobEntry.delete(0, 'end')

                            dobEntry.insert(0, str(date))
                            dobEntry['state'] = 'disabled'

                            calendar_window.destroy()
                        
                        tkinter.Button(calendar_window, text="Select Date", command=return_date).grid(row=1, column=0)

                # dob_selector = tkinter.Button(collectFrame, text="Select Date", command=select_dob_calendar)
                # dob_selector.grid(row=2, column=2, sticky='e', padx=5)

                # Gender
                gender_selection = StringVar(collectFrame)
                gender_selection.set("M")
                gender_choices = ["M", "F"]

                genderPrompt = tkinter.Label(collectFrame, text="Gender: ", fg="white", bg=blue, font=h1)
                genderPrompt.grid(row=3, column=0, pady=10)

                genderSelector = OptionMenu(collectFrame, gender_selection, *gender_choices)
                genderSelector.config(bg=blue, fg="white", padx=5, font=h2)
                genderSelector.grid(row=3, column=1, sticky='ew')

                # Church select
                churchPrompt = tkinter.Label(collectFrame, text="Church: ", bg=blue, fg="white", font=h1)
                churchPrompt.grid(row=4, column=0, pady=10)

                church_selection = StringVar(collectFrame)
                church_dictionary = church_dict_glob_id
                church_list = []

                for church in church_dictionary:
                    church_list.append(church)


                print(church_dictionary)

                church_selection.set(church_list[0])
                church_choices = church_list
                churchSelector = OptionMenu(collectFrame, church_selection, *church_choices)
                churchSelector.config(bg=blue, fg="white", padx=5, font=h2)
                churchSelector.grid(row=4, column=1, sticky='ew')

                # Role Insert
                rolePrompt = tkinter.Label(collectFrame, text="Roles:", fg="white", bg=blue, font=h1)
                rolePrompt.grid(row=5, column=0, pady=10)

                role_selection = StringVar(collectFrame)
                role_dictionary = roles_dict_glob
                role_id_dictionary = roles_dict_glob_id
                role_list = []
                # roles = sql_select("SELECT * FROM Roles")
                selected_roles = []

                # for id, rolename, description in roles:
                #     role_dictionary["{}, {}".format(rolename, description)] = rolename
                #     role_list.append("{}, {}".format(rolename, description))
                #     role_id_dictionary[rolename] = id

                for role in roles_dict_glob:
                    role_list.append(role)

                role_selection.set('None')
                role_list.append('None')
                role_choices = role_list
                
                roleSelector = OptionMenu(collectFrame, role_selection, *role_choices)
                roleSelector.config(bg=blue, fg="white", padx=5, font=h2)
                roleSelector.grid(row=5, column=1, sticky='ew')

                def addSelRole():
                    new_role = role_selection.get()
                    print(new_role)
                    print(selected_roles)
                    if new_role == "None":
                        selected_roles.clear()
                        roleShower['text'] = "\n".join(selected_roles)
                        return None

                    if role_dictionary[new_role] in selected_roles:
                            return None
                        
                    selected_roles.append(role_dictionary[new_role])

                    roleShower['text'] = "\n".join(selected_roles)


                roleAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Role", command=addSelRole)
                roleAdder.grid(row=5, column=2, sticky='ew')

                roleShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
                roleShower.grid(row=6, column=1, sticky='ew')


                # School prompt
                schoolPrompt = tkinter.Label(collectFrame, bg=blue, text="School (if applicable):", fg="white", font=h1)
                schoolPrompt.grid(row=7, column=0)

                schoolEntry = tkinter.Entry(collectFrame, font=h2)
                schoolEntry.grid(row=7, column=1, sticky='ew')

                # Sacraments Received
                sacramentPrompt = tkinter.Label(collectFrame, text="Sacraments", fg="white", bg=blue, font=h1)
                sacramentPrompt.grid(row=8, column=0, pady=10)

                sacrament_selection = StringVar(collectFrame)
                sacrament_dictionary = {}
                sacrament_choices = ['None', 'Baptism', 'Reconciliation', 'Holy Communion', 'Confirmation']
                selected_sacraments = []

                sacrament_selection.set('None')
                
                sacramentSelector = OptionMenu(collectFrame, sacrament_selection, *sacrament_choices)
                sacramentSelector.config(bg=blue, fg="white", padx=5, font=h2)
                sacramentSelector.grid(row=8, column=1, sticky='ew')

                def addSelSacrament():
                    new_sacrament = sacrament_selection.get()
                    if new_sacrament == "None":
                        selected_sacraments.clear()
                        sacramentShower['text'] = "\n".join(selected_roles)
                        return None

                    if new_sacrament in selected_sacraments:
                        return None
                        
                    selected_sacraments.append(new_sacrament)

                    sacramentShower['text'] = "\n".join(selected_sacraments)


                sacramentAdder = tkinter.Button(collectFrame, bg=blue, fg="white", text="Add Sacrament", command=addSelSacrament)
                sacramentAdder.grid(row=8, column=2, sticky='ew')

                sacramentShower = tkinter.Label(collectFrame, text="", bg=blue, fg="white", font=h2)
                sacramentShower.grid(row=9, column=1, sticky='ew', pady=10)

                # Church of Baptism
                cBaptismPrompt = tkinter.Label(collectFrame, text="Church of Baptism: ", bg=blue, fg="white", font=h1)
                cBaptismPrompt.grid(row=10, column=0)

                cBaptismEntry = tkinter.Entry(collectFrame, font=h2)
                cBaptismEntry.grid(row=10, column=1, sticky='ew')

                # Family Select
                familyPrompt = tkinter.Label(collectFrame, text="Family: ", bg=blue, fg="white", font=h1)
                familyPrompt.grid(row=11, column=0, pady=10)

                family_dict=family_dict_glob

                def familySelector():
                    familyWin = tkinter.Tk()
                    familyWin.title("Family Finder")
                    # familyWin.geometry('910x340')

                    familyListbox = tkinter.Listbox(familyWin, width=100, height=15, font=h2)
                    familyListbox.grid(row=0, column=0, sticky='ew')

                    horizontal_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.HORIZONTAL, command=familyListbox.xview)
                    familyListbox['xscrollcommand'] = horizontal_scrollbar.set
                    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

                    vertical_scrollbar = tkinter.Scrollbar(familyWin, orient=tkinter.VERTICAL, command=familyListbox.yview)
                    familyListbox['yscrollcommand'] = vertical_scrollbar.set
                    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

                    familyWin.geometry("")

                    # families = sql_select("SELECT * FROM Family")
                    familyListbox.insert('end', 'Individual')
                    # for familyId, familyName, familyNotes, dateCreated, address in families:
                    #     family_dict["Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")] = familyId
                    #     familyListbox.insert('end', "Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated))
                    #     print(family_dict)

                    for family in family_dict:
                        familyListbox.insert('end', family)

                    def getFamily():
                        if len(familyListbox.get(tkinter.ANCHOR)) == 0:
                            messagebox.showerror("Error", "Please select a family to continue")
                            return None
                        
                        else:
                            familyButton['text'] = familyListbox.get(tkinter.ANCHOR)
                            familyWin.destroy()

                    familySelectButton = tkinter.Button(familyWin, text="Select Family", bg=blue, fg="white", font=h2, command=getFamily)
                    familySelectButton.grid(row=2, column=0, sticky='ew')

                    familyWin.mainloop()

                familyButton = tkinter.Button(collectFrame, text="Find Family", bg=blue, fg="white", font=h2, command=familySelector)
                familyButton.grid(row=11, column=1, sticky='ew')
                # Religion

                religionPrompt = tkinter.Label(collectFrame, text="Religion: ", bg=blue, fg="white", font=h1)
                religionPrompt.grid(row=12, column=0, sticky='ew')

                religion_selection = StringVar(collectFrame)
                religion_selection.set("Roman Catholic")
                religion_choices = ["Roman Catholic", "Church of England", "Orthodox", "Other Christian (Protestant)", "Non-Christian", "None"]

                religionSelector = OptionMenu(collectFrame, religion_selection, *religion_choices)
                religionSelector.config(bg=blue, fg="white", font=h2)
                religionSelector.grid(row=12, column=1, sticky='ew', pady=5)

                # Additional Notes

                notesPrompt = tkinter.Label(collectFrame, text="Additional Notes:", font=h1, bg=blue, fg="white")
                notesPrompt.grid(row=13, column=0)

                notesEntry = tkinter.Text(collectFrame, font=h2)
                notesEntry.grid(row=13, column=1, sticky='ew')

                scrollbar = tkinter.Scrollbar(collectFrame, orient=tkinter.VERTICAL, command=notesEntry.yview, bg=blue)
                notesEntry['yscrollcommand'] = scrollbar.set
                scrollbar.grid(row=13, column=2, sticky='wns')

                # Edit Details Button
                def makeChanges():
                    member_name = nameEntry.get()
                    member_dob = dobEntry.get()
                    member_church = church_selection.get()
                    member_school = schoolEntry.get()
                    member_sacraments = selected_sacraments
                    if len(selected_sacraments) == 0:
                        member_sacraments.append("None")
                    
                    member_baptism_church = cBaptismEntry.get()
                    member_roles = selected_roles
                    member_gender = gender_selection.get()
                    member_family = None
                    member_religion = religion_selection.get()

                    try:
                        if 'Individual' in familyButton['text']:
                            member_family = 0
                        else:
                            member_family = family_dict[familyButton['text'].replace("\n", "")]
                    except:
                        messagebox.showerror("Error", "Please click the 'Find Family' Buttton and make a selection from the List")
                        return None

                    member_notes = notesEntry.get('1.0', 'end')

                    if not check_name(member_name):
                        return None
                    
                    if not check_dob_child(member_dob):
                        return None
                    

                    if member_family == "Find Family":
                        messagebox.showerror("Error", "Please press the 'Find Family' Button and select from the list")
                        return None

                    selected_roles_ids = []

                    for role in selected_roles:
                        selected_roles_ids.append(role_id_dictionary[role])

                    commit_question = askyesno(title="Confirmation", message="Are you sure you want to make changes to this Member's details?")
                    if commit_question:
                        try:
                            # int(church_dictionary[member_church]), ', '.join(str(v) for v in selected_roles_ids)
                            # sql("UDPATE MembersChild SET FullName='{}', DOB='{}', School='{}', SacramentsReceived='{}', ChurchOfBaptism='{}', RoleID='{}', FamilyID={}, Notes='{}', ChurchID={}, Gender='{}'".format(member_name, member_dob, member_school, member_sacraments, member_baptism_church, ', '.join(str(v) for v in selected_roles_ids), member_family, member_notes, member_church, member_gender))
                            sql_items("UPDATE MembersChild SET FullName=%s, DOB=%s, School=%s, SacramentsReceived=%s, ChurchOfBaptism=%s, RoleID=%s, FamilyID=%s, Notes=%s, ChurchID=%s, Gender=%s, Religion=%s WHERE MemberCID=%s", (member_name, member_dob, member_school, ', '.join(selected_sacraments), member_baptism_church, ', '.join(str(v) for v in selected_roles_ids), member_family, member_notes, int(church_dictionary[member_church]), member_gender, member_religion, member_id))
                            
                        except:
                            messagebox.showerror("Error", "There was a problem making changes to this member's details. Check your connection and try again later")
                            return None

                        messagebox.showinfo("Success", "Successfully made changes to the details of {}".format(member_name))
                        person_update_child(member_id, member_name, member_dob, member_school, ', '.join(selected_sacraments), member_baptism_church, ', '.join(str(v) for v in selected_roles_ids), member_family, member_notes, int(church_dictionary[member_church]), member_gender)
                    
                    

                makeChangeButton = tkinter.Button(collectFrame, text="Make Changes", bg=blue, font=h1, fg="white", command=makeChanges)
                makeChangeButton.grid(row=14, column=1, sticky='ew')


                # insert details
                for memberid, fullname, dob, school, sacramentsreceived, churchofbaptism, roleid, familyid, notes, church_id, gender, religion in sql_select("SELECT * FROM MembersChild WHERE MemberCID={}".format(member_id)):
                    nameEntry.insert(0, fullname)  
                    gender_selection.set(gender)
                    
                    religion_selection.set(religion)
                    # dobEntry.config(state='normal')
                    dobEntry.set(dob)
                    # dobEntry.config(state='disabled')

                    for churchvalue, churchid in church_dictionary.items():
                        if churchid == church_id:
                            church_selection.set(churchvalue)

                    if len(roleid) != 0:
                        roles_temp = roleid.split(', ')
                        print("RoleID ", roleid)
                        print("RolesTemp: ", roles_temp)
                        for temp_role_id in roles_temp:
                            selected_roles.append(sql_select("SELECT RoleName FROM Roles WHERE RoleID={}".format(int(temp_role_id)))[0][0])

                    print(selected_roles)
                    roleShower['text'] = "\n".join(selected_roles)

                    schoolEntry.insert(0, school)

                    if "None" not in sacramentsreceived:
                        selected_sacraments = sacramentsreceived.split(', ')
                        sacramentShower['text'] = "\n".join(selected_sacraments)

                    cBaptismEntry.insert(0, churchofbaptism)

                    if familyid == 0:
                        familyButton['text'] = "Individual"
                    else:
                        # families = sql_select("SELECT * FROM Family WHERE FamilyID={}".format(familyid))
                        # for familyId, familyName, familyNotes, dateCreated, address in families:
                        #     familyButton['text'] = "Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")

                        for family in family_dict_glob:
                            if family_dict_glob[family] == familyid:
                                familyButton['text'] = family

                    notesEntry.insert(0, notes)


                    
                    


                    




        if memberEdit[4] == 'a':
            for person in adults_list:
                print("COMPARE")
                print("ID: a{}. {} | {}".format(person.member_id, person.fullname, church_dict_glob[person.churchid]))
                print(memberEdit)
                if "ID: a{}. {} | {}".format(person.member_id, person.fullname, church_dict_glob_name[person.churchid]) == memberEdit:
                    memberSelect.configure(state='disabled')
                    editDetailFrame(person.member_id, 'a', person.fullname, editFrame)
                    return None
        else:
            for person in childrens_list:
                print("ID: c{}. {} | {}".format(person.member_id, person.fullname, church_dict_glob_name[person.churchid]))
                print(memberEdit)

                if "ID: c{}. {} | {}".format(person.member_id, person.fullname, church_dict_glob_name[person.churchid]) == memberEdit:
                    memberSelect.configure(state='disabled')
                    editDetailFrame(person.member_id, 'c', person.fullname, editFrame)
                    return None


    editButton = tkinter.Button(container, text="Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: editMemberDetails(editFrame))
    editButton.grid(row=3, column=0, sticky='w')

    def deleteButton():
        memberDel = memberSelect.get(tkinter.ANCHOR)
        adult_members = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult")
        child_members = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild")
        memberDelID = None
        def deleter(memid, category, fullname):
            try:
                if category == 'a':
                    sql("DELETE FROM MembersAdult WHERE MemberAID={}".format(memid))
                else:
                    sql("DELETE FROM MembersChild WHERE MemberCID={}".format(memid))
            except:
                messagebox.showerror("Error", "There was an error when trying to delete the selected Member")
                return None
            
            for i in range(len(adults_list)):
                if adults_list[i].member_id == memid:
                    del adults_list[i]

                    messagebox.showinfo("Success", "{} was successfully removed".format(fullname))
                    editMember(frame)
                    return None

            for i in range(len(childrens_list)):
                if childrens_list[i].member_id == memid:
                    del childrens_list[i]

                    messagebox.showinfo("Success", "{} was successfully removed".format(fullname))
                    editMember(frame)
                    return None

        churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
        churches_dict = {}
        for churchid, churchname in churches:
            churches_dict[churchid] = churchname

        for memberid, fullname, churchid in adult_members:
            if "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[churchid]) == memberDel:
                deleter(memberid, 'a', fullname)
                return None
            
        for memberid, fullname, churchid in child_members:
            if "ID: c{}. {} | {}".format(memberid, fullname, churches_dict[churchid]) == memberDel:
                print(churches_dict[churchid])
                deleter(memberid, 'c', fullname)
                return None


    deleteButton = tkinter.Button(container, text="Delete Member", font=h1, bg=blue, fg="white", width=30, command=deleteButton)
    deleteButton.grid(row=3, column=0, sticky='e')
    
    searchFunction(memberSelect, container, 4)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=5, column=0)

def viewIndividualArea(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    h0 = tkFont.Font(family='Helvetica', size=14, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    indListbox = tkinter.Listbox(container, width=60, font=h2)
    indListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=indListbox.xview)
    indListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=indListbox.yview)
    indListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    searchFunction(indListbox, container, 2)

    def getFamilyName(famid):
        if famid == 0:
            return "Individual"
        fam_details = sql_select("SELECT FamilyName, Address FROM Family WHERE FamilyID={}".format(famid))

        return ', '.join(fam_details[0])

    def getChurchName(churchid):
        church_name = sql_select("SELECT ChurchName FROM Churches WHERE ChurchID={}".format(churchid))

        return church_name[0][0]

    def getRoles(roleids):
        if len(roleids) == 0:
            return ""
        roles = roleids.split(', ')

        roles_list = []

        for role in roles:
            try:
                new_role = sql_select("SELECT RoleName FROM Roles WHERE RoleID={}".format(role))

                roles_list.append(new_role[0][0])
            except:
                print('')

        return ', '.join(roles_list)


    def viewIndividualFromDB():
        member = indListbox.get(tkinter.ANCHOR)

        member_id = id_finder(member)

        outputframe = tkinter.Frame(container, background="#036bfc", highlightthickness=2)
        outputframe.grid(row=6, column=0, pady=50, sticky='ew')

        member_detbox = tkinter.Listbox(outputframe, font=h2)
        member_detbox.grid(row=0, column=0, sticky='ew')

        outputframe.columnconfigure(0, weight=1)

        horizontal_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.HORIZONTAL, command=member_detbox.xview)
        member_detbox['xscrollcommand'] = horizontal_scrollbar.set
        horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

        vertical_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.VERTICAL, command=member_detbox.yview)
        member_detbox['yscrollcommand'] = vertical_scrollbar.set
        vertical_scrollbar.grid(row=0, column=0, sticky='ens')

        

        if member_id[1] == 'a':
            member_details = sql_select("SELECT FullName, DOB, ChurchID, RoleID, Occupation, Gender, MaritalStatus, PhoneNum, Email, DBS, FamilyID, AdditionalNotes, Religion FROM MembersAdult WHERE MemberAID={}".format(member_id[0]))
            member_details = member_details[0]

            # name_text = tkinter.Label(outputframe, text="MemberID: a{}".format(member_id[0]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=0, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "MemberID: a{}".format(member_id[0]))

            # name_text = tkinter.Label(outputframe, text="Name: {}".format(member_details[0]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=1, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Name: {}".format(member_details[0]))

            # name_text = tkinter.Label(outputframe, text="DOB: {}".format(member_details[1]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=2, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "DOB: {}".format(member_details[1]))

            # name_text = tkinter.Label(outputframe, text="Church: {}".format(getChurchName(member_details[2])), bg=blue, fg="white", font=h1)
            # name_text.grid(row=3, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Church: {}".format(getChurchName(member_details[2])))

            # name_text = tkinter.Label(outputframe, text="Roles: {}".format(getRoles(member_details[3])), bg=blue, fg="white", font=h1, wraplength=500)
            # name_text.grid(row=4, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Roles: {}".format(getRoles(member_details[3])))

            # name_text = tkinter.Label(outputframe, text="Occupation: {}".format(member_details[4]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=5, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Occupation: {}".format(member_details[4]))

            # name_text = tkinter.Label(outputframe, text="Gender: {}".format(member_details[5]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=6, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Gender: {}".format(member_details[5]))

            # name_text = tkinter.Label(outputframe, text="Marital Status: {}".format(member_details[6]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=7, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Marital Status: {}".format(member_details[6]))

            # name_text = tkinter.Label(outputframe, text="Phone Number: {}".format(member_details[7]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=8, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Phone Number: {}".format(member_details[7]))

            # name_text = tkinter.Label(outputframe, text="Email: {}".format(member_details[8]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=9, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Email: {}".format(member_details[8]))

            # name_text = tkinter.Label(outputframe, text="DBS: {}".format(member_details[9]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=10, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "DBS: {}".format(member_details[9]))

            # name_text = tkinter.Label(outputframe, text="Family ID: {}".format(getFamilyName(member_details[10])), bg=blue, fg="white", font=h1)
            # name_text.grid(row=11, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Family ID: {}".format(getFamilyName(member_details[10])))

            # name_text = tkinter.Label(outputframe, text="Additional Notes: {}".format(member_details[11]), bg=blue, fg="white", font=h1)
            # name_text.grid(row=12, column=0, padx=10, sticky='w', pady=5)

            member_detbox.insert('end', "Religion: {}".format(member_details[12]))

            member_detbox.insert('end', "Additional Notes: {}".format(member_details[11]))

            

        elif member_id[1] == 'c':
            member_details = sql_select("SELECT FullName, DOB, School, SacramentsReceived, ChurchOfBaptism, RoleID, FamilyID, Notes, ChurchID, Gender, Religion FROM MembersChild WHERE MemberCID={}".format(member_id[0]))
            member_details = member_details[0]

            member_detbox.insert('end', "MemberID: c{}".format(member_id[0]))

            member_detbox.insert('end', "Name: {}".format(member_details[0]))

            member_detbox.insert('end',"DOB: {}".format(member_details[1]))

            member_detbox.insert('end', "Gender: {}".format(member_details[9]))

            member_detbox.insert('end',"Church: {}".format(getChurchName(member_details[8])))

            member_detbox.insert('end', "Family ID: {}".format(getFamilyName(member_details[6])))

            member_detbox.insert('end', "School: {}".format(member_details[2]))

            member_detbox.insert('end', "Sacraments Received: {}".format(member_details[3]))

            member_detbox.insert('end', "Church Of Baptism: {}".format(member_details[4]))

            member_detbox.insert('end', "Roles: {}".format(getRoles(member_details[5])))

            member_detbox.insert('end', "Religion: {}".format(member_details[10]))

            member_detbox.insert('end', "Notes: {}".format(member_details[7]))

            

            


    viewButton = tkinter.Button(container, text="View Individual", bg=blue, fg="white", font=h2, command=viewIndividualFromDB)
    viewButton.grid(row=5, column=0, sticky='ew')



def viewFamilyArea(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    h0 = tkFont.Font(family='Helvetica', size=14, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    indListbox = tkinter.Listbox(container, width=100, font=h2)
    indListbox.grid(row=0, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=indListbox.xview)
    indListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=indListbox.yview)
    indListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=0, column=0, sticky='ens')

    searchFunctionFamily(indListbox, container, 2)

    def showFamilyMembers():
        selected_family = indListbox.get(tkinter.ANCHOR)

        for widget in temp_container.winfo_children():
            temp_container.destroy()
        
        results = sql_select("SELECT * FROM Family")

        def showWholeFamily(_familyid):

            # Show Adults
            adults_family = sql_select("SELECT * FROM MembersAdult WHERE FamilyID={}".format(_familyid))

            def getFamilyName(famid):
                if famid == 0:
                    return "Individual"
                fam_details = sql_select("SELECT FamilyName, Address FROM Family WHERE FamilyID={}".format(famid))

                return ', '.join(fam_details[0])
            
            def getChurchName(churchid):
                church_name = sql_select("SELECT ChurchName FROM Churches WHERE ChurchID={}".format(churchid))

                return church_name[0][0]

            def getRoles(roleids):
                if len(roleids) == 0:
                    return ""
                roles = roleids.split(', ')

                roles_list = []

                for role in roles:
                    try:
                        new_role = sql_select("SELECT RoleName FROM Roles WHERE RoleID={}".format(role))

                        roles_list.append(new_role[0][0])
                    except:
                        print("")

                return ', '.join(roles_list)    

            i = 8

            tkinter.Label(temp_container, text="Adults", font=h1, fg="white", bg=blue).grid(row=7, column=0, sticky='ew')

            listboxes = []
            scrollbars = []

            for memberid, fullname, dob, churchid, roleid, occupation, gender, maritalstatus, phonenumber, email, dbs, familyid, notes, religion in adults_family:
                
                # outputframe = tkinter.Frame(temp_container, background="#036bfc", highlightthickness=2, width=150)
                # outputframe.grid(row=i, column=0, pady=10, sticky='ew')

                outputframe = tkinter.Frame(temp_container, background="#036bfc", width=150, highlightthickness=2)
                outputframe.grid(row=i, column=0, pady=10, sticky='ew')

                member_detbox = tkinter.Listbox(outputframe, font=h2, width=100)
                member_detbox.grid(row=0, column=0, sticky='ew')

                outputframe.columnconfigure(0, weight=1)

                horizontal_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.HORIZONTAL, command=member_detbox.xview)
                member_detbox['xscrollcommand'] = horizontal_scrollbar.set
                horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

                vertical_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.VERTICAL, command=member_detbox.yview)
                member_detbox['yscrollcommand'] = vertical_scrollbar.set
                vertical_scrollbar.grid(row=0, column=0, sticky='ens')

                member_detbox.insert('end', "MemberID: a{}".format(memberid))

                member_detbox.insert('end', "Name: {}".format(fullname))

                member_detbox.insert('end', "DOB: {}".format(dob))

                member_detbox.insert('end', "Church: {}".format(getChurchName(churchid)))

                member_detbox.insert('end', "Roles: {}".format(getRoles(roleid)))

                member_detbox.insert('end', "Occupation: {}".format(occupation))

                member_detbox.insert('end', "Gender: {}".format(gender))

                member_detbox.insert('end', "Marital Status: {}".format(maritalstatus))

                member_detbox.insert('end', "Phone Number: {}".format(phonenumber))

                member_detbox.insert('end',"Email: {}".format(email))

                member_detbox.insert('end', "DBS: {}".format(dbs))

                member_detbox.insert('end', "Family ID: {}".format(getFamilyName(familyid)))

                member_detbox.insert('end', "Religion: {}".format(religion))

                member_detbox.insert('end',"Additional Notes: {}".format(notes))

                i += 1
            

            # Show Children

            tkinter.Label(temp_container, text="Children", font=h1, fg="white", bg=blue).grid(row=i, column=0, sticky='ew')

            i += 1

            children_family = sql_select("SELECT * FROM MembersChild WHERE FamilyID={}".format(_familyid))

            for memberid, fullname, dob, school, sacramentsreceived, churchofbaptism, roleid, familyid, notes, churchid, gender, religion in children_family:
                
                outputframe = tkinter.Frame(temp_container, background="#036bfc", width=150, highlightthickness=2)
                outputframe.grid(row=i, column=0, pady=10, sticky='ew')

                member_detbox = tkinter.Listbox(outputframe, font=h2, width=100)
                member_detbox.grid(row=0, column=0, sticky='ew')

                outputframe.columnconfigure(0, weight=1)

                horizontal_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.HORIZONTAL, command=member_detbox.xview)
                member_detbox['xscrollcommand'] = horizontal_scrollbar.set
                horizontal_scrollbar.grid(row=1, column=0, sticky='nwe')

                vertical_scrollbar = tkinter.Scrollbar(outputframe, orient=tkinter.VERTICAL, command=member_detbox.yview)
                member_detbox['yscrollcommand'] = vertical_scrollbar.set
                vertical_scrollbar.grid(row=0, column=0, sticky='ens')
                
                member_detbox.insert('end', "MemberID: c{}".format(memberid))

                member_detbox.insert('end', "Name: {}".format(fullname))

                member_detbox.insert('end', "DOB: {}".format(dob))

                member_detbox.insert('end', "Gender: {}".format(gender))
                
                member_detbox.insert('end', "Church: {}".format(getChurchName(churchid)))

                member_detbox.insert('end', "Family ID: {}".format(getFamilyName(familyid)))

                member_detbox.insert('end', "School: {}".format(school))

                member_detbox.insert('end', "Sacraments Received: {}".format(sacramentsreceived))

                member_detbox.insert('end', "Church Of Baptism: {}".format(churchofbaptism))

                member_detbox.insert('end', "Roles: {}".format(getRoles(roleid)))

                member_detbox.insert('end', "Religion: {}".format(religion))

                member_detbox.insert('end', "Notes: {}".format(notes))

                i += 1



        for familyid, familyname, notes, datecreated, address in results:
            if selected_family == "FamilyID: {}, Family Name: {}, Address: {}, Date Created: {}, Notes: {}".format(familyid, familyname, address, datecreated, notes):
                indListbox['state'] = 'disabled'
                showWholeFamily(familyid)
        
        
        

    familyViewButton = tkinter.Button(container, text="View Family", font=h2, bg=blue, fg="white", command=showFamilyMembers)
    familyViewButton.grid(row=6, column=0, sticky='ew')

    temp_container = tkinter.Frame(container, bg=blue)
    temp_container.grid(row=7, column=0, sticky='ew')



def editFamilyDetailsArea(frame):
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

    familySelect = tkinter.Listbox(container, width=110, height=15, font=h2)
    familySelect.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=familySelect.xview)
    familySelect['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=familySelect.yview)
    familySelect['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    def editFamilyDetails(editFrame):

        if len(familySelect.get(tkinter.ANCHOR)) == 0:
            return None
        
        member_id = familySelect.get(tkinter.ANCHOR)

        member_id = member_id[member_id.find(':')+1:member_id.find(',')]

        print("Member ID: ", member_id)

        familySelect['state'] = 'disabled'


        # Family Name
        familyNamePrompt = tkinter.Label(editFrame, text="Family Name: ", font=h1, bg=blue, fg="white")
        familyNamePrompt.grid(row=0, column=0, padx=5)

        familyNameEntry = tkinter.Entry(editFrame, font=h2)
        familyNameEntry.grid(row=0, column=1, sticky='ew')

        # Family Address
        familyAddressPrompt = tkinter.Label(editFrame, text="Family Address: ", font=h1, bg=blue, fg="white")
        familyAddressPrompt.grid(row=1, column=0, padx=5)

        familyAddressEntry = tkinter.Entry(editFrame, font=h2)
        familyAddressEntry.grid(row=1, column=1, sticky='ew')




        # Family Notes
        familyNotesPrompt = tkinter.Label(editFrame, text="Notes: ", font=h1, bg=blue, fg="white")
        familyNotesPrompt.grid(row=2, column=0, padx=5)

        familyNotesEntry = tkinter.Text(editFrame, font=h2)
        familyNotesEntry.grid(row=2, column=1, sticky='ew')

        scrollbar = tkinter.Scrollbar(editFrame, orient=tkinter.VERTICAL, command=familyNotesEntry.yview, bg=blue)
        familyNotesEntry['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=2, column=2, sticky='wns')

        def makeFamilyChanges():
            family_name = familyNameEntry.get()
            family_address = familyAddressEntry.get()
            family_notes = familyNotesEntry.get('1.0', 'end')

            if len(family_name) == 0:
                messagebox.showerror("Error", "Please enter a family name")
                return None
            
            if len(family_address) == 0:
                messagebox.showerror("Error", "Please enter a family address")
                return None

            commit_question = askyesno(title="Confirmation", message="Are you sure you want to make changes to this family?")
            if commit_question:
                try:
                    sql_items("UPDATE Family SET FamilyName=%s, Notes=%s, Address=%s WHERE FamilyID=%s", (family_name, family_notes, family_address, member_id))
                except:
                    messagebox.showerror("Error", "There was an error when trying to make changes to the Family Details. Please try again later")
                    return None
                
                messagebox.showinfo("Success", "Successfully made changes to the family")
                editFamilyDetailsArea(frame)

        editCommitButton = tkinter.Button(editFrame, text="Make Changes", fg="white", bg=blue, font=h1, command=makeFamilyChanges)
        editCommitButton.grid(row=3, column=1, sticky='ew')

        family_dets = sql_select("SELECT * FROM Family WHERE FamilyID={}".format(member_id))

        for familyid, familyname, notes, datecreated, address in family_dets:
            familyNameEntry.insert('end', familyname)
            familyAddressEntry.insert('end', address)
            familyNotesEntry.insert('end', notes)

    editButton = tkinter.Button(container, text="Edit Details", font=h1, bg=blue, fg="white", width=30, command=lambda: editFamilyDetails(editFrame))
    editButton.grid(row=3, column=0, sticky='w')

    def deleteFamilyDB():
        if len(familySelect.get(tkinter.ANCHOR)) == 0:
            return None
        
        family_id = familySelect.get(tkinter.ANCHOR)

        family_id = family_id[family_id.find(':')+1:family_id.find(',')]

        commit_question = askyesno(title="Confirmation", message="Are you sure you want to Delete this family and all of its members?")
        if commit_question:
            try:
                sql("DELETE FROM MembersAdult WHERE FamilyID={}".format(family_id))
                sql("DELETE FROM MembersChild WHERE FamilyID={}".format(family_id))
                sql("DELETE FROM Family WHERE FamilyID={}".format(family_id))
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error when trying to delete this family. Please try again later")
                return None
            
            for i in range(len(adults_list)):
                print(adults_list[i].name)
                print(adults_list[i].familyid)
                if adults_list[i].familyid == int(family_id):
                    del adults_list[i]

            for i in range(len(childrens_list)):
                print(childrens_list[i].name)
                print(childrens_list[i].familyid)
                if childrens_list[i].familyid == int(family_id):
                    del childrens_list[i]

            
            messagebox.showinfo("Success", "Successfully deleted Family and all of its members")
            editFamilyDetailsArea(frame)
                

    deleteButton = tkinter.Button(container, text="Delete Family", font=h1, bg=blue, fg="white", width=30, command=deleteFamilyDB)
    deleteButton.grid(row=3, column=0, sticky='e')

    searchFunctionFamily(familySelect, container, 4)

    editFrame = tkinter.Frame(container, bg=blue)
    editFrame.grid(row=5, column=0)

def memberOptions(frame, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options

    if userlevel == 1 or userlevel == 3:
        memberAddButton = tkinter.Button(mOptionsFrame, text="Add", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: addMember(restFrame))
        memberAddButton.grid(row=0, column=1, padx=10)
    
        memberEditButton = tkinter.Button(mOptionsFrame, text="Edit or Delete", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: editMember(restFrame))
        memberEditButton.grid(row=0, column=2, padx=10)

        FamilyAddButton = tkinter.Button(mOptionsFrame, text="Create Family", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: createFamilyArea(restFrame))
        FamilyAddButton.grid(row=0, column=4, padx=10)

        familyEditButton = tkinter.Button(mOptionsFrame, text="Edit / Delete Family", highlightthickness=0, bd=0, font=h1, fg="white", bg=blue, command=lambda: editFamilyDetailsArea(restFrame))
        familyEditButton.grid(row=0, column=5)

    viewIndividualButton = tkinter.Button(mOptionsFrame, text="View Individual", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: viewIndividualArea(restFrame))
    viewIndividualButton.grid(row=0, column=6, padx=10)
    
    viewFamilyButton = tkinter.Button(mOptionsFrame, text="View Family", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: viewFamilyArea(restFrame))
    viewFamilyButton.grid(row=0, column=7, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)
