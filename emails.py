from encodings import search_function
from database_init import *
from tkinter import LEFT, font as tkFont
from tkinter import ttk
from PIL import Image, ImageTk
from colors import *
import datetime
from tkinter import *
from checks import *
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import askyesno
from members_class import *
from search_func import adults_list, searchFunction, searchFunctionGroups
import pyperclip

def createGroup(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    groupNamePrompt = tkinter.Label(container, text="Group Name: ", bg=blue, fg="white", font=h1)
    groupNamePrompt.grid(row=0, column=0)

    groupNameEntry = tkinter.Entry(container, font=h2)
    groupNameEntry.grid(row=0, column=1, sticky='ew', pady=(0, 10))

    # Select Members from Here
    temp_container = tkinter.Frame(container, bg=blue, highlightthickness=2)
    temp_container.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)

    selectPrompt = tkinter.Label(temp_container, text="Select Members to add to Group", font=h1, bg=blue, fg="white")
    selectPrompt.grid(row=0, column=0)

    indListbox = tkinter.Listbox(temp_container, width=60, font=h2)
    indListbox.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(temp_container, orient=tkinter.HORIZONTAL, command=indListbox.xview)
    indListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(temp_container, orient=tkinter.VERTICAL, command=indListbox.yview)
    indListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    # searchFunctionEmail(indListbox, temp_container, 3)
    t_adults_list = adults_list
    added_list = []
    # Search Function

    churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
    churches_dict = {}
    for churchid, churchname in churches:
        churches_dict[churchid] = churchname

    def fill_listbox():
        indListbox.delete(0, 'end')
        # mAdults = sql_select("SELECT * FROM MembersAdult")
        # mChilds = sql_select("SELECT * FROM MembersChild")
        for person in t_adults_list:
            indListbox.insert('end', person.value)


    fill_listbox()


    searchFrame = tkinter.Frame(temp_container, bg=blue)
    searchFrame.grid(row=3, column=0, columnspan=3, pady=10)

    container.rowconfigure(0, weight=1)

    searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
    searchLabel.grid(row=0, column=0)

    search_selection = StringVar(searchFrame)
    search_selection.set("MemberID")
    search_choices = ["MemberID", "Full Name", "Occupation", "DOB", "Phone Number", "Email", "Role"]


    searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
    searchSelector.config(bg=blue, fg="white", padx=3)
    searchSelector.grid(row=0, column=1)

    searchEntry = tkinter.Entry(searchFrame, font=h2)
    searchEntry.grid(row=0, column=2, sticky='ew')
    
    def searcher():
        indListbox.delete(0, 'end')
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
                        indListbox.insert('end', "ID: a{}. {} | {}".format(result[0][0], result[0][1], churches_dict[int(result[0][2])]))
                        return None
                    elif search_entry[0] == 'c':
                        try:
                            result = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild WHERE MemberCID={}".format(int(search_entry[1:])))
                            print(result)
                            indListbox.insert('end', "ID: c{}. {} | {}".format(result[0][0], result[0][1], churches_dict[0][int(result[2])]))
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
            "Role": "RoleID"
        }

        # Searching Adult
        result1 = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
        print(result1)
        

        # Outputting both
        if len(result1) != 0:
            for memberid, fullname, churchid in result1:
                for person in t_adults_list:
                    if person.member_id == memberid:
                        indListbox.insert('end', "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

       
    searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
    searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


    resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
    resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

    # Search Function

    def addToShow():
        member = indListbox.get(tkinter.ANCHOR)

        for i in range(len(t_adults_list)):
            print("h")
            if t_adults_list[i].value == member:
                showListbox.insert('end', member)
                added_list.append(t_adults_list[i])
                del t_adults_list[i]
                index = indListbox.get(0, 'end').index(member)
                indListbox.delete(index)


    addButton = tkinter.Button(temp_container, text="Add to Group", font=h1, fg="white", bg=blue, command=addToShow)
    addButton.grid(row=4, column=0, sticky='ew')

    # See selected members Here

    show_container = tkinter.Frame(container, bg=blue)
    show_container.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

    showPrompt = tkinter.Label(show_container, text="Members you Added", font=h1, bg=blue, fg="white")
    showPrompt.grid(row=0, column=0)

    showListbox = tkinter.Listbox(show_container, width=60, font=h2)
    showListbox.grid(row=1, column=0)

    shorizontal_scrollbar = tkinter.Scrollbar(show_container, orient=tkinter.HORIZONTAL, command=showListbox.xview)
    showListbox['xscrollcommand'] = shorizontal_scrollbar.set
    shorizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    svertical_scrollbar = tkinter.Scrollbar(show_container, orient=tkinter.VERTICAL, command=showListbox.yview)
    showListbox['yscrollcommand'] = svertical_scrollbar.set
    svertical_scrollbar.grid(row=1, column=0, sticky='ens')

    def removeShow():
        member = showListbox.get(tkinter.ANCHOR)
        for i in range(len(added_list)):
            if added_list[i].value == member:
                print("found")
                t_adults_list.append(added_list[i])
                del added_list[i]
                indListbox.insert(0, member)
                index = showListbox.get(0, 'end').index(member)
                showListbox.delete(index)
                

    removeButton = tkinter.Button(show_container, text="Remove from List", font=h2, fg="white", bg=blue, command=removeShow)
    removeButton.grid(row=2, column=0, sticky='ew')

    def createGroupDB():

        group_name = groupNameEntry.get()

        all_groups = sql_select("SELECT EGroupName FROM EmailGroups WHERE EGroupName='{}'".format(group_name))

        if len(all_groups) > 0:
            messagebox.showerror("Error", "Please select a unique Group Name. This name is currently in use")
            return None

        if len(group_name) == 0:
            messagebox.showerror("Error", "Please insert a Group Name")
            return None

        group_ids = []
        if len(added_list) == 0:
            messagebox.showerror("Error", "Please add members to this group")
            return None

        for person in added_list:
            group_ids.append(person.member_id)

        members_str = ', '.join(str(v) for v in group_ids)
        
        

        try:
            sql_items("INSERT INTO EmailGroups (EGroupName, EGroupMembers) VALUES (%s, %s)", (group_name, members_str))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "There was an error adding this Group. Please try again later")
            return None
        
        messagebox.showinfo("Success", "Successfully created E-mail Group")
        createGroup(frame)

    createButton = tkinter.Button(show_container, text="Make Group", font=h1, fg="white", bg=blue, command=createGroupDB)
    createButton.grid(row=3, column=0, sticky='ew', pady=10)




def editGroupArea(frame, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    nameFrame = tkinter.Frame(container, bg=blue)
    nameFrame.grid(row=0, column=0)

    # tkinter.Label(container, text="Created Groups", fg="white", bg=blue, font=h1).grid(row=0, column=0)

    indListbox = tkinter.Listbox(container, width=60, font=h2)
    indListbox.grid(row=1, column=0)

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=indListbox.xview)
    indListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=indListbox.yview)
    indListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    groups_dict = searchFunctionGroups(indListbox, container, 4)

    def editGroupDetails():

        group = indListbox.get(tkinter.ANCHOR)

        if len(group) == 0:
            return None

        groupid = group[group.find(":")+1:group.find(" |")]

        members_list = groups_dict[group]

        members_ids_list = members_list.split(", ")
        t_adults_list = adults_list[:]
        members_ids_list_i = [int(x) for x in members_ids_list]
        added_list = []

        removals = []
        for i in range(len(t_adults_list)):
        
            print(t_adults_list[i].fullname)
            if t_adults_list[i].member_id in members_ids_list_i:
                print("match")
                added_list.append(t_adults_list[i])
                # del t_adults_list[i]
                removals.append(i)
                print("removals: ", removals)
        
        # removals = removals.reverse()
        print("removals: ", removals[::-1])
        for number in removals[::-1]:
            del t_adults_list[number]

        print("Len adults_list: ", len(t_adults_list))
        print("len added list: ", len(added_list))


        



        nameFrame = tkinter.Frame(container, bg=blue)
        nameFrame.grid(row=5, column=0, sticky='ew')

        namePrompt = tkinter.Label(nameFrame, font=h1, fg="white", bg=blue, text="Name: ")
        namePrompt.grid(row=0, column=0, sticky='w')

        nameEntry = tkinter.Entry(nameFrame, font=h2)
        nameEntry.grid(row=0, column=1, sticky='ew')

        nameEntry.insert(0, group[group.find("| Group Name: ")+14:])

        nameFrame.columnconfigure(1, weight=1)
        
        tkinter.Label(nameFrame, text="Members you can add", fg="white", bg=blue, font=h1).grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky='ew')

        memListbox = tkinter.Listbox(container, width=60, font=h2)
        memListbox.grid(row=6, column=0)

        mhorizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=memListbox.xview)
        memListbox['xscrollcommand'] = mhorizontal_scrollbar.set
        mhorizontal_scrollbar.grid(row=7, column=0, sticky='nwe')

        mvertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=memListbox.yview)
        memListbox['yscrollcommand'] = mvertical_scrollbar.set
        mvertical_scrollbar.grid(row=6, column=0, sticky='ens')


        # Search Function

        churches = sql_select("SELECT ChurchID, ChurchName FROM Churches")
        churches_dict = {}
        for churchid, churchname in churches:
            churches_dict[churchid] = churchname

        def fill_listbox():
            memListbox.delete(0, 'end')
            # mAdults = sql_select("SELECT * FROM MembersAdult")
            # mChilds = sql_select("SELECT * FROM MembersChild")
            print(len(t_adults_list))
            for person in t_adults_list:
                memListbox.insert('end', person.value)


        fill_listbox()


        searchFrame = tkinter.Frame(container, bg=blue)
        searchFrame.grid(row=8, column=0, columnspan=3, pady=10)

        container.rowconfigure(0, weight=1)

        searchLabel = tkinter.Label(searchFrame, text="Search: ", fg="white", bg=blue, font=h1)
        searchLabel.grid(row=0, column=0)

        search_selection = StringVar(searchFrame)
        search_selection.set("MemberID")
        search_choices = ["MemberID", "Full Name", "Occupation", "DOB", "Phone Number", "Email", "Role"]


        searchSelector = OptionMenu(searchFrame, search_selection, *search_choices)
        searchSelector.config(bg=blue, fg="white", padx=3)
        searchSelector.grid(row=0, column=1)

        searchEntry = tkinter.Entry(searchFrame, font=h2)
        searchEntry.grid(row=0, column=2, sticky='ew')
        
        def searcher():
            memListbox.delete(0, 'end')
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
                            memListbox.insert('end', "ID: a{}. {} | {}".format(result[0][0], result[0][1], churches_dict[int(result[0][2])]))
                            return None
                        elif search_entry[0] == 'c':
                            try:
                                result = sql_select("SELECT MemberCID, FullName, ChurchID FROM MembersChild WHERE MemberCID={}".format(int(search_entry[1:])))
                                print(result)
                                memListbox.insert('end', "ID: c{}. {} | {}".format(result[0][0], result[0][1], churches_dict[0][int(result[2])]))
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
                "Role": "RoleID"
            }

            # Searching Adult
            result1 = sql_select("SELECT MemberAID, FullName, ChurchID FROM MembersAdult WHERE {} LIKE '%{}%'".format(property_dict[search_property], search_entry))
            print(result1)
            

            # Outputting both
            if len(result1) != 0:
                for memberid, fullname, churchid in result1:
                    for person in t_adults_list:
                        if person.member_id == memberid:
                            memListbox.insert('end', "ID: a{}. {} | {}".format(memberid, fullname, churches_dict[int(churchid)]))

        
        searchButton = tkinter.Button(searchFrame, text="Search Member", fg="white", bg=blue, font=h1, command=searcher)
        searchButton.grid(row=1, column=0, columnspan=3, sticky='ew')


        resetButton = tkinter.Button(searchFrame, text="Reset List", fg="white", bg=blue, font=h1, command=fill_listbox)
        resetButton.grid(row=2, column=0, columnspan=3, sticky='ew')

        def addToShow():
            member = memListbox.get(tkinter.ANCHOR)

            for i in range(len(t_adults_list)):
                try:
                    if t_adults_list[i].value == member:
                        showListbox.insert('end', member)
                        added_list.append(t_adults_list[i])
                        del t_adults_list[i]
                        index = memListbox.get(0, 'end').index(member)
                        memListbox.delete(index)
                except:
                    len(added_list)
                    len(t_adults_list)


        addButton = tkinter.Button(container, text="Add to Group", font=h1, fg="white", bg=blue, command=addToShow)
        addButton.grid(row=9, column=0, sticky='ew')

        if userlevel == 2:
            addButton.grid_forget()
        # Search Function

        show_container = tkinter.Frame(container, bg=blue)
        show_container.grid(row=10, column=0, columnspan=2, sticky='ew', pady=10)

        showPrompt = tkinter.Label(show_container, text="Members you Added", font=h1, bg=blue, fg="white")
        showPrompt.grid(row=0, column=0)

        showListbox = tkinter.Listbox(show_container, width=60, font=h2)
        showListbox.grid(row=1, column=0)

        shorizontal_scrollbar = tkinter.Scrollbar(show_container, orient=tkinter.HORIZONTAL, command=showListbox.xview)
        showListbox['xscrollcommand'] = shorizontal_scrollbar.set
        shorizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

        svertical_scrollbar = tkinter.Scrollbar(show_container, orient=tkinter.VERTICAL, command=showListbox.yview)
        showListbox['yscrollcommand'] = svertical_scrollbar.set
        svertical_scrollbar.grid(row=1, column=0, sticky='ens')

        def removeShow():
            member = showListbox.get(tkinter.ANCHOR)
            for i in range(len(added_list)):
                try:
                    if added_list[i].value == member:
                        print("found")
                        t_adults_list.append(added_list[i])
                        del added_list[i]
                        memListbox.insert(0, member)
                        index = showListbox.get(0, 'end').index(member)
                        showListbox.delete(index)
                except:
                    print(len(added_list))
                    print(len(t_adults_list))

        removeButton = tkinter.Button(show_container, text="Remove from List", font=h2, fg="white", bg=blue, command=removeShow)
        removeButton.grid(row=2, column=0, sticky='ew')

        if userlevel == 2:
            removeButton.grid_forget()

        def commitGroupChangesDB():
            confirmation = askyesno(title="Confirmation", message="Are you sure you want to make the given changes?")
            if confirmation:

                group_name = nameEntry.get()

                if len(group_name) == 0:
                    messagebox.showerror("Error", "Please insert a Group Name")
                    return None

                all_groups = sql_select("SELECT EGroupName FROM EmailGroups WHERE EGroupName='{}'".format(group_name))
                
                if len(all_groups) > 0:
                    messagebox.showerror("Error", "Please select another Group name as this name is already in use.")
                    return None
                group_ids = []
                if len(added_list) == 0:
                    messagebox.showerror("Error", "Please add members to this group")
                    return None

                for person in added_list:
                    group_ids.append(person.member_id)

                members_str = ', '.join(str(v) for v in group_ids)

                try:
                    sql_items("UPDATE EmailGroups SET EGroupName=%s, EGroupMembers=%s WHERE EGroupID=%s", (group_name, members_str, groupid))

                except:
                    messagebox.showerror("Error", "There was an error making the given changes. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully made the Changes to the Group")
                editGroupArea(frame)

        commitChangesButton = tkinter.Button(container, text="Make Group Changes", font=h1, bg=blue, fg="white", command=commitGroupChangesDB)
        commitChangesButton.grid(row=20, column=0, sticky='ew', pady=(10, 0))

        if userlevel == 2:
            commitChangesButton.grid_forget()

        # Insert People

        for person in added_list:
            showListbox.insert('end', person.value)
        

    if userlevel == 1 or userlevel == 3:
        editButton = tkinter.Button(container, text="View/Edit Details", font=h1, bg=blue, fg="white", width=20, command=editGroupDetails)
        editButton.grid(row=3, column=0, sticky='w')

    else:
        editButton = tkinter.Button(container, text="View Details", font=h1, bg=blue, fg="white", width=20, command=editGroupDetails)
        editButton.grid(row=3, column=0, sticky='w')

    def deleteGroupDB():

        group = indListbox.get(tkinter.ANCHOR)
        if len(group) == 0:
            return None


        confirmation = askyesno(title="Confirmation", message="Are you sure you want to delete this Email Group?")
        if confirmation:


            groupid = group[group.find(":")+1:group.find(" |")]

            print("Group ID: ", groupid)

            try:
                sql("DELETE FROM EmailGroups WHERE EGroupID={}".format(groupid))
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "There was an error deleting this Group. Please try again later")
                return None

            messagebox.showinfo("Success", "Successfully deleted Group")
            editGroupArea(frame)

    deleteButton = tkinter.Button(container, text="Delete Member", font=h1, bg=blue, fg="white", width=20, command=deleteGroupDB)
    deleteButton.grid(row=3, column=0, sticky='e')


    

    
def sendEmailArea(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = tkinter.Frame(frame, bg=blue)
    container.grid(row=0, column=0, columnspan=12, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)
    
    text="To send Emails, select a group from the listbox below and click the select button. This will copy the email addresses of all of the participants. Now, simply paste this into the recipients section when sending the Email."
    howLabel = tkinter.Label(container, text=text, fg="white", bg=blue, font=h1, wraplength=500)
    howLabel.grid(row=0, column=0)

    indListbox = tkinter.Listbox(container, width=60, font=h2)
    indListbox.grid(row=1, column=0, pady=(10, 0))

    horizontal_scrollbar = tkinter.Scrollbar(container, orient=tkinter.HORIZONTAL, command=indListbox.xview)
    indListbox['xscrollcommand'] = horizontal_scrollbar.set
    horizontal_scrollbar.grid(row=2, column=0, sticky='nwe')

    vertical_scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=indListbox.yview)
    indListbox['yscrollcommand'] = vertical_scrollbar.set
    vertical_scrollbar.grid(row=1, column=0, sticky='ens')

    groups_dict = searchFunctionGroups(indListbox, container, 4)

    def copyEmails():
        group = indListbox.get(tkinter.ANCHOR)

        if len(group) == 0:
            return None
        
        # groupid = group[group.find(":")+1:group.find(" |")]

        members = groups_dict[group]
        members_list = members.split(', ')

        member_emails = sql_select("SELECT Email FROM MembersAdult WHERE MemberAID IN ({})".format(members))

        print(member_emails)
        email_list = []
        for email in member_emails:
            email_list.append(email[0])

        print(email_list)
        pyperclip.copy(', '.join(email_list))

        messagebox.showinfo("What to do Now", "Go to your email (e.g. gmail) and in the recipients section, click paste. Write out your email, and click send. This email will be sent to all members of the selected group.")

    copyEmailsButton = tkinter.Button(container, text="Copy Emails to Clipboard", font=h1, fg="white", bg=blue, command=copyEmails)
    copyEmailsButton.grid(row=5, column=0, sticky='ew')







def mailOptions(frame, userlevel):
    for widget in frame.winfo_children():
        widget.destroy()

    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Top Frame
    mOptionsFrame = tkinter.Frame(frame, height=100, background="#036bfc")
    mOptionsFrame.grid(row=0, column=0, padx=10, pady=10)
    frame.columnconfigure(0, weight=1)

    # Top Frame Options
    if userlevel == 1 or userlevel == 3:
        createMailGroup = tkinter.Button(mOptionsFrame, text="Create Group", highlightthickness=0, bd=0, font=h1, background="#036bfc", fg="white", command=lambda: createGroup(restFrame))
        createMailGroup.grid(row=0, column=1, padx=10)

    if userlevel == 1 or userlevel == 3:
        editMailGroup = tkinter.Button(mOptionsFrame, text="View/Edit/Delete", highlightthickness=0, bd=0, font=h1, background=blue, fg="white", command=lambda: editGroupArea(restFrame, userlevel))
        editMailGroup.grid(row=0, column=2, padx=10)
    else:
        editMailGroup = tkinter.Button(mOptionsFrame, text="View Email Groups", highlightthickness=0, bd=0, font=h1, background=blue, fg="white", command=lambda: editGroupArea(restFrame, userlevel))
        editMailGroup.grid(row=0, column=2, padx=10)


    if userlevel == 1 or userlevel == 3:
        sendMailAreaButton = tkinter.Button(mOptionsFrame, text="Send Email", highlightthickness=0, bd=0, fg="white", bg=blue, font=h1, command=lambda: sendEmailArea(restFrame))
        sendMailAreaButton.grid(row=0, column=3, padx=10)

    restFrame = tkinter.Frame(frame, background=blue, height=400)
    restFrame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

    mOptionsFrame.columnconfigure(0, weight=1)