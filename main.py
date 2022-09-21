from database_init import *
from tkinter import LEFT, font as tkFont
from tkinter import ttk
from members import *
from roles import *
from church_bookings import *
from emails import *
from baptism import *
from marriage import *
from holy_communions import *
from funerals import *
from PIL import Image, ImageTk
import PIL.Image
from users import *
from search_func import adults_list, childrens_list, church_dict_glob, church_dict_glob_id, roles_dict_glob, roles_dict_glob_id, family_dict_glob, church_dict_glob_name
version = 0
def image_converter(path):
    image = PIL.Image.open(path)
    image = image.resize((20, 20), PIL.Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

def get_all_families():
    families = sql_select("SELECT * FROM Family")
    for familyId, familyName, familyNotes, dateCreated, address in families:
        family_dict_glob["Family Name: {}, Address: {}, Notes: {}, Date Created: {}".format(familyName, address, familyNotes, dateCreated).replace("\n", "")] = familyId
        print(family_dict_glob)

def get_all_roles():
    roles = sql_select("SELECT * FROM Roles")

    for id, rolename, description in roles:
        roles_dict_glob["{}, {}".format(rolename, description)] = rolename
        roles_dict_glob_id[rolename] = id

def get_all_churches():
    churches = sql_select("SELECT * FROM Churches")

    for churchid, churchname in churches:
        church_dict_glob[churchid] = "ID: {} Church Name: {}".format(churchid, churchname)
        church_dict_glob_id["ID: {} Church Name: {}".format(churchid, churchname)] = churchid
        church_dict_glob_name[churchid] = churchname


def get_all_members():
    
    mAdults = sql_select("SELECT * FROM MembersAdult")
    mChilds = sql_select("SELECT * FROM MembersChild")
    for member_id, fullname, dob, churchid, roleid, occupation, gender, maritalstatus, phonenum, email, dbs, familyid, additionalnotes, religion in mAdults:
        person = Person()
        person.member_id = member_id
        person.fullname = fullname
        person.dob = dob
        person.churchid = churchid
        person.roleids = roleid
        person.occupation = occupation
        person.gender = gender
        person.maritalstatus = maritalstatus
        person.phonenum = phonenum
        person.email = email
        person.dbs = dbs
        person.familyid = familyid
        person.notes = additionalnotes
        person.religion = religion
        person.value = "ID: a{}. {} | {}".format(member_id, fullname, church_dict_glob_name[int(churchid)])
        adults_list.append(person)

    for member_id, fullname, dob, school, sacramentsreceived, churchbaptism, roleid, familyid, notes, churchid, gender, religion in mChilds:
        person = Person()
        person.member_id = member_id
        person.fullname = fullname
        person.dob = dob
        person.gender = gender
        person.school = school
        person.sacramentsreceived = sacramentsreceived
        person.churchbaptism = churchbaptism
        person.roleid = roleid
        person.familyid = familyid
        person.notes = notes
        person.churchid = churchid
        person.religion = religion
        person.value = "ID: c{}. {} | {}".format(member_id, fullname, church_dict_glob_name[int(churchid)])
        childrens_list.append(person)


def tmainArea(userlevel):
    get_all_families()
    get_all_roles()
    get_all_churches()
    get_all_members()

    for person in adults_list:
        print(person.value)
        print(person.fullname)
        print(person.roleids)

    root = tkinter.Tk()
    root.title("Main Area")
    root.geometry('1100x600')
    h2 = tkFont.Font(family='Helvetica', size=15, weight='bold')
    h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # Creating the main frame
    main_frame = tkinter.Frame(root, background='blue')
    main_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.LEFT)

    # Create canvas
    canvas = tkinter.Canvas(main_frame, background="#036bfc")
    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

    # Add scrollbar
    page_scrollbar = ttk.Scrollbar(main_frame, orient=tkinter.VERTICAL, command=canvas.yview)
    page_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


    # Configure the canvas
    canvas.configure(yscrollcommand=page_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _on_mouse_wheel(event):
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", _on_mouse_wheel)
    # Frame INSIDE the canvas
    second_frame = tkinter.Frame(canvas, background="#036bfc")
    

    # add that new frame to a window in the canvas
    canvas_frame = canvas.create_window((0, 0), window=second_frame, anchor='nw')
    
    def FrameWidth(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_frame, width=canvas_width)

    def OnFrameConfigure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    second_frame.bind("<Configure>", OnFrameConfigure)
    canvas.bind("<Configure>", FrameWidth)

    # Top Frame
    topFrame = tkinter.Frame(second_frame, width=100, background="#036bfc")
    topFrame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    second_frame.columnconfigure(2, weight=1)

    # Top Frame Options

    label = tkinter.Label(topFrame, text="Parish Administrator", font=h2, fg="white", bg=blue)
    label.grid(row=0, column=0, pady=(0, 30))

    memberImage = image_converter("icons/member.png")
    membersButton = tkinter.Button(topFrame, text="Members", image=memberImage, compound=LEFT, highlightthickness=0, bd=0, font=h1, command=lambda: memberOptions(pFrame, userlevel), background="#036bfc", fg="white")
    # membersButton = tkinter.Button(topFrame, image=memberImage, compound=LEFT, highlightthickness=0, bd=0, font=h1, command=lambda: memberOptions(pFrame, userlevel), background="#036bfc", fg="white", width=65)
    membersButton.grid(row=1, column=0, pady=10, sticky='w')

    

    bookingImage = image_converter("icons/booking.png")
    churchBookButton = tkinter.Button(topFrame, text="Church Bookings", image=bookingImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: bookingOptions(pFrame))
    # churchBookButton = tkinter.Button(topFrame, image=bookingImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: bookingOptions(pFrame), width=65)
    churchBookButton.grid(row=2, column=0, pady=10, sticky='w')
    
    baptismImage = image_converter("icons/baptism.png")
    BaptismButton = tkinter.Button(topFrame, text="Baptism", image=baptismImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # BaptismButton = tkinter.Button(topFrame, image=baptismImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: baptismOptions(pFrame, canvas))
    BaptismButton.grid(row=3, column=0, pady=10, sticky='w')

    hcImage = image_converter("icons/holy-communion.png")
    HolyCommButton = tkinter.Button(topFrame, text="Holy Communion", image=hcImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # HolyCommButton = tkinter.Button(topFrame, image=hcImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: hcOptions(pFrame, canvas))
    HolyCommButton.grid(row=4, column=0, pady=10, sticky='w')
    
    marriageImage = image_converter("icons/marriage.png")
    MarriageButton = tkinter.Button(topFrame, text="Marriage", image=marriageImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # MarriageButton = tkinter.Button(topFrame, image=marriageImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: marriageOptions(pFrame, canvas))
    MarriageButton.grid(row=5, column=0, pady=10, sticky='w')

    funeralImage = image_converter("icons/funeral.png")
    FuneralsButton = tkinter.Button(topFrame, text="Funeral", image=funeralImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # FuneralsButton = tkinter.Button(topFrame, image=funeralImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: funeralOptions(pFrame, canvas))
    FuneralsButton.grid(row=6, column=0, pady=10, sticky='w')

    emailImage = image_converter("icons/email.png")
    EmailListButton = tkinter.Button(topFrame, text="Email List", image=emailImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # EmailListButton = tkinter.Button(topFrame, image=emailImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: mailOptions(pFrame))
    EmailListButton.grid(row=7, column=0, pady=10, sticky='w')

    roleImage = image_converter("icons/role.png")
    roleButton = tkinter.Button(topFrame, text="Roles", image=roleImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # roleButton = tkinter.Button(topFrame, image=roleImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: roleOptionsArea(pFrame))
    roleButton.grid(row=8, column=0, pady=10, sticky='w')

    userImage = image_converter("icons/user.png")
    userButton = tkinter.Button(topFrame, text="Users", image=userImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0,)
    # userButton = tkinter.Button(topFrame, image=userImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: userOptions(pFrame, canvas))
    userButton.grid(row=9, column=0, pady=10, sticky='w')

    ttk.Separator(second_frame, orient='vertical').grid(row=0, column=1, sticky='wns')

    pFrame = tkinter.Frame(second_frame, background="#036bfc")
    pFrame.grid(row=0, column=2, sticky='news', pady=5)

    root.mainloop()


# tmainArea(1)

def signInArea():
    signArea = tkinter.Tk()
    signArea.title("Sign In")
    signArea.geometry("")
    signArea['bg'] = blue
    h1 = tkFont.Font(family='Helvetica', size=15, weight='bold')
    h2 = tkFont.Font(family='Helvetica', size=12)

    signArea.columnconfigure(0, weight=1)

    # Label
    label = tkinter.Label(signArea, text="Parish Administrator", font=h1, bg=blue).grid(row=0, column=0, columnspan=2, pady=10)

    # Username
    usernamePrompt = tkinter.Label(signArea, text="Username: ", font=h1, fg="white", bg=blue)
    usernamePrompt.grid(row=1, column=0)

    usernameEntry = tkinter.Entry(signArea, width=30, font=h2)
    usernameEntry.grid(row=1, column=1, sticky='ew', padx=(0, 10))

    # Password
    passwordPrompt = tkinter.Label(signArea, text="Password: ", fg="white", bg=blue, font=h1)
    passwordPrompt.grid(row=2, column=0)

    passwordEntry = tkinter.Entry(signArea, font=h2, show="*")
    passwordEntry.grid(row=2, column=1, sticky='ew', padx=(0, 10))

    def checkCreds():
        
        def mainArea(userlevel):
            get_all_families()
            get_all_roles()
            get_all_churches()
            get_all_members()

            for person in adults_list:
                print(person.value)
                print(person.fullname)
                print(person.roleids)

            root = tkinter.Tk()
            root.title("Main Area")
            root.geometry('1300x490')
            h2 = tkFont.Font(family='Helvetica', size=15, weight='bold')
            h1 = tkFont.Font(family='Helvetica', size=12, weight='bold')
            # Creating the main frame
            main_frame = tkinter.Frame(root, background='blue')
            main_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.LEFT)

            # Create canvas
            canvas = tkinter.Canvas(main_frame, background="#036bfc")
            canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

            # Add scrollbar
            page_scrollbar = ttk.Scrollbar(main_frame, orient=tkinter.VERTICAL, command=canvas.yview)
            page_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


            # Configure the canvas
            canvas.configure(yscrollcommand=page_scrollbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            def _on_mouse_wheel(event):
                canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

            canvas.bind("<MouseWheel>", _on_mouse_wheel)
            # Frame INSIDE the canvas
            second_frame = tkinter.Frame(canvas, background="#036bfc")
            

            # add that new frame to a window in the canvas
            canvas_frame = canvas.create_window((0, 0), window=second_frame, anchor='nw')
            
            def FrameWidth(event):
                canvas_width = event.width
                canvas.itemconfig(canvas_frame, width=canvas_width)

            def OnFrameConfigure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            second_frame.bind("<Configure>", OnFrameConfigure)
            canvas.bind("<Configure>", FrameWidth)

            # Top Frame
            topFrame = tkinter.Frame(second_frame, width=100, background="#036bfc")
            topFrame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
            second_frame.columnconfigure(2, weight=1)

            # Top Frame Options

            label = tkinter.Label(topFrame, text="Parish Administrator", font=h2, fg="white", bg=blue)
            label.grid(row=0, column=0, pady=(0, 30))

            memberImage = image_converter("icons/member.png")
            membersButton = tkinter.Button(topFrame, text="Members", image=memberImage, compound=LEFT, highlightthickness=0, bd=0, font=h1, command=lambda: memberOptions(pFrame, userlevel), background="#036bfc", fg="white")
            # membersButton = tkinter.Button(topFrame, image=memberImage, compound=LEFT, highlightthickness=0, bd=0, font=h1, command=lambda: memberOptions(pFrame, userlevel), background="#036bfc", fg="white", width=65)
            membersButton.grid(row=1, column=0, pady=10, sticky='w')
            

            bookingImage = image_converter("icons/booking.png")
            churchBookButton = tkinter.Button(topFrame, text="Church Bookings", image=bookingImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: bookingOptions(pFrame, userlevel, canvas))
            # churchBookButton = tkinter.Button(topFrame, image=bookingImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: bookingOptions(pFrame), width=65)
            churchBookButton.grid(row=2, column=0, pady=10, sticky='w')
            
            baptismImage = image_converter("icons/baptism.png")
            BaptismButton = tkinter.Button(topFrame, text="Baptism", image=baptismImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: baptismOptions(pFrame, canvas, userlevel))
            # BaptismButton = tkinter.Button(topFrame, image=baptismImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: baptismOptions(pFrame, canvas))
            BaptismButton.grid(row=3, column=0, pady=10, sticky='w')

            hcImage = image_converter("icons/holy-communion.png")
            HolyCommButton = tkinter.Button(topFrame, text="Holy Communion", image=hcImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: hcOptions(pFrame, canvas, userlevel))
            # HolyCommButton = tkinter.Button(topFrame, image=hcImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: hcOptions(pFrame, canvas))
            HolyCommButton.grid(row=4, column=0, pady=10, sticky='w')
            
            marriageImage = image_converter("icons/marriage.png")
            MarriageButton = tkinter.Button(topFrame, text="Marriage", image=marriageImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: marriageOptions(pFrame, canvas, userlevel))
            # MarriageButton = tkinter.Button(topFrame, image=marriageImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: marriageOptions(pFrame, canvas))
            MarriageButton.grid(row=5, column=0, pady=10, sticky='w')

            funeralImage = image_converter("icons/funeral.png")
            FuneralsButton = tkinter.Button(topFrame, text="Funeral", image=funeralImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: funeralOptions(pFrame, canvas, userlevel))
            # FuneralsButton = tkinter.Button(topFrame, image=funeralImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: funeralOptions(pFrame, canvas))
            FuneralsButton.grid(row=6, column=0, pady=10, sticky='w')

            emailImage = image_converter("icons/email.png")
            EmailListButton = tkinter.Button(topFrame, text="Email List", image=emailImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: mailOptions(pFrame, userlevel))
            # EmailListButton = tkinter.Button(topFrame, image=emailImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: mailOptions(pFrame))
            EmailListButton.grid(row=7, column=0, pady=10, sticky='w')

            roleImage = image_converter("icons/role.png")
            roleButton = tkinter.Button(topFrame, text="Roles", image=roleImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: roleOptionsArea(pFrame, userlevel))
            # roleButton = tkinter.Button(topFrame, image=roleImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: roleOptionsArea(pFrame))
            roleButton.grid(row=8, column=0, pady=10, sticky='w')

            userImage = image_converter("icons/user.png")
            userButton = tkinter.Button(topFrame, text="Users", image=userImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, command=lambda: userOptions(pFrame, canvas))
            # userButton = tkinter.Button(topFrame, image=userImage, compound=LEFT, font=h1, background="#036bfc", fg="white", highlightthickness=0, bd=0, width=65, command=lambda: userOptions(pFrame, canvas))
            userButton.grid(row=9, column=0, pady=10, sticky='w')

            ttk.Separator(second_frame, orient='vertical').grid(row=0, column=1, sticky='wns')

            pFrame = tkinter.Frame(second_frame, background="#036bfc")
            pFrame.grid(row=0, column=2, sticky='news', pady=5)

            # Check for updates
            connection = mysql.connector.connect(
                host='bn6u1ywrjwklb228a7tv-mysql.services.clever-cloud.com',
                database='bn6u1ywrjwklb228a7tv',
                user='u5ewoi2wzmwuj6mv',
                password='6av3qj58nGWbMtOHrret'
            )

            try:
                connection.ping(reconnect=True, attempts=3, delay=5)
            except mysql.connector.Error as err:
                connection = init_db()

            cursor = connection.cursor()

            cursor.execute("SELECT DriveID, DriveName FROM AdministrationVersions WHERE VersionID > {} ORDER BY VersionID DESC".format(version))
            new_versions = cursor.fetchall()

            print(new_versions)

            if len(new_versions) != 0:

                confirmation = askyesno("A Software Update is Available", "Would you like to make the software update now?\nThe update will take place in the background, but you will not be able to use the software while the update is taking place.")

                if confirmation:
                    import gdown
                    import os
                    import pathlib
                    import shutil

                    # try:
                    #     os.system('cmd /k "echo hello"')
                    # except Exception as e:
                    #     messagebox.showerror("Error", e)

                    current_directory = pathlib.Path().resolve()
                    print(current_directory)

                    file = new_versions[0][0]
                    file_name = new_versions[0][1]
                    

                    
                    try:
                        gdown.download(id=file, output=os.path.join(current_directory, file_name), quiet=False)
                    except Exception as e:
                        messagebox.showerror("Error", e)
                        return None

                    try:
                        root.destroy()
                        # command="PowerShell Expand-Archive -Force -Path '{}' -DestinationPath '{}'".format(os.path.join(current_directory, file_name), current_directory)
                        # os.system('cmd /k "{}"'.format(command))
                        os.system('cmd /k "updater.exe"')
                    except Exception as e:
                        messagebox.showerror("Error", e)

            root.mainloop()


        username = usernameEntry.get()
        password = passwordEntry.get()

        user = sql_items_select("SELECT UserID, UserName, UserEmail, UserPhone, UserLevel FROM Users WHERE SystemName=%s AND UserPassword=%s", (username, password))
        if len(user) == 0:
            messagebox.showerror("Error", "Please check the credentials that you entered.")
            return None
        
        if password == "ChurchSystem1":
            signArea.destroy()
            passwordWin = tkinter.Tk()
            passwordWin.title("Change Password")
            passwordWin.geometry("") 
            passwordWin['bg'] = blue
            h1 = tkFont.Font(family='Helvetica', size=15, weight='bold')
            h2 = tkFont.Font(family='Helvetica', size=12)

            label = tkinter.Label(passwordWin, text="Please Enter a New Password to Update your Password", font=h2, fg="white", bg=blue).grid(row=0, column=0, pady=10)

            container = tkinter.Frame(passwordWin, bg=blue)
            container.grid(row=1, column=0, sticky='ew')

            container.columnconfigure(1, weight=1)

            newPassPrompt = tkinter.Label(container, text="New Password: ", font=h1, fg="white", bg=blue)
            newPassPrompt.grid(row=1, column=0)

            passwordEntryn = tkinter.Entry(container, width=30, font=h2, show="*")
            passwordEntryn.grid(row=1, column=1, sticky='ew', padx=(0, 10))

            repPassPrompt = tkinter.Label(container, text="Repeat New Password: ", font=h1, fg="white", bg=blue)
            repPassPrompt.grid(row=2, column=0)

            passwordEntryR = tkinter.Entry(container, font=h2, show="*")
            passwordEntryR.grid(row=2, column=1, sticky='ew', padx=(0, 10))

            

            def updatePassword():
                new_password = passwordEntryn.get()
                rep_password = passwordEntryR.get()

                if not (new_password == rep_password):
                    messagebox.showerror("Password Mismatch", "The passwords do not match")
                    return None

                if new_password == "ChurchSystem1":
                    messagebox.showerror("Error", "Please select another password")
                    return None

                if len(new_password) < 8:
                    messagebox.showerror("Password Length", "Please select a longer password")
                    return None
                
                if not (any(x.isupper() for x in new_password) and any (x.islower() for x in new_password)):
                    messagebox.showerror("Upper and Lower Cases", "Please ensure your password contains both upper and lower case letters")
                    return None

                try:
                    sql_items("UPDATE Users SET UserPassword=%s WHERE UserID=%s", (new_password, user[0][0]))
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "There was an error updating your password. Please try again later")
                    return None

                messagebox.showinfo("Success", "Successfully updated Password")
                passwordWin.destroy()
                signInArea()

            changeButton = tkinter.Button(passwordWin, text="Change Password", font=h1, fg="white", bg=blue, command=updatePassword)
            changeButton.grid(row=3, column=0, sticky='ew')

            passwordWin.mainloop()
        else:
            signArea.destroy()
            mainArea(user[0][4])

        
    signButton = tkinter.Button(signArea, text="Sign In", fg="white", bg=blue, font=h1, command=checkCreds)
    signButton.grid(row=3, column=1, sticky='ew', padx=(0, 10))

    # signArea.resize(False, False)
    signArea.mainloop()

signInArea()
