# importing required packages
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox as msg
from db_connection import get_db_connection

# Function to go back to the login page
def goToLogin(callback):
    win2.destroy()
    callback.deiconify()

# Function to insert new user details into the database
def newUserInsert(name, phn, addr, uid, pwd):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO User_Details (name, phone_Number, address, user_ID, password) VALUES (?, ?, ?, ?, ?)", (name, phn, addr, uid, pwd))
    connection.commit()
    connection.close()
    pass

# Function to validate the details entered by the user
def check_details():
    name = usr_name.get()
    ph_no = phone.get()
    digs = len(ph_no)
    addr = address.get()
    uid = usr_id.get()
    pwd = pswd.get()
    pwd1 = rpwd.get()

    if name == '' or ph_no == '' or addr == '':
        msg.showinfo("Error", "Fill all the fields")

    elif not (name.isalpha()):
        msg.showinfo("Error", "Invalid Name, Enter Proper Name")
    elif not (ph_no.isdigit()) or digs != 10:
        msg.showinfo("Error", "Invalid phone number! Enter Proper phone number")
    elif uid == '':
        msg.showinfo("Error", "Enter User ID")
    elif len(pwd) < 4:
        msg.showinfo("Error", "Password should be minimum of 4 characters")
    elif pwd == '' or pwd1 == '':
        msg.showifo("Error", "Enter & re-enter your password")
    elif pwd != pwd1:
        msg.showinfo("Error", "Password mismatch")
    else:
        newUserInsert(name, ph_no, addr, uid, pwd)
        msg.showinfo("Info", "Registration Successful")
        goToLogin(logwin)
        reset()

# Function to reset the input fields
def reset():
    usr_name.delete(0, END)
    phone.delete(0, END)
    address.delete(0, END)
    usr_id.delete(0, END)
    pswd.delete(0, END)
    rpwd.delete(0, END)

def check_phone_exists(event):
    phone_number = phone.get()
    if phone_number == '':
        return  # Skip check if the field is empty
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM User_Details WHERE phone_Number = ?", (phone_number,))
    result = cursor.fetchone()
    connection.close()
    if result[0] > 0:
        msg.showinfo("Error", "Phone number already exist. Please choose a different phone number/ Login with your user ID.")
        phone.delete(0, END)


# Function to check if the User ID already exists in the database
def check_user_id_exists(event):
    uid = usr_id.get()
    if uid == '':
        return  # Skip check if the field is empty
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM User_Details WHERE user_ID = ?", (uid,))
    result = cursor.fetchone()
    connection.close()
    if result[0] > 0:
        msg.showinfo("Error", "User ID already taken. Please choose a different User ID.")
        usr_id.delete(0, END)  # Clear the field if the User ID is taken

def RegisterPage(callback):
    global win2, usr_name, phone, address, usr_id, pswd, rpwd,logwin

    logwin = callback
    # Customizing window
    win2 = tk.Toplevel()
    win2.title("Registration Page")
    win2.configure(bg='light blue')
    win2.resizable(False, False)
    win2.state('zoomed')

    fnt_size = 15
    # Adding background color
    label_fg =  'black'
    label_bg =  'light blue'
    label_font = 'Arial Black'

    #Customizing button attributes
    btn_fg = 'white'
    btn_bg = '#047185'
    btn_font = ('Broadway', 10)
    btn_active_bg = '#b911c2'

    # Customizing entry attributes
    entry_bg = '#aae8f0'
    entry_font = ('arial',fnt_size)

    # Adding background image
    bg_image = ImageTk.PhotoImage(Image.open("register 3.png"))
    bg_label = Label(win2, image=bg_image)
    bg_label.place(relx=0, rely=0.09, relwidth=1, relheight=1)
    

    # Customizing display attributes
    headingFrame = tk.Label(win2, text="Kindly Enter your details to register", fg="purple", bd=4, font=(entry_font, 20), bg='light blue')
    headingFrame.place(relx=0., rely=0, relwidth=1, relheight=0.16)

    labelFrame = Frame(win2, bg=label_bg)
    labelFrame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.5)

    label1 = tk.Label(labelFrame, text="Name", fg= label_fg, bg= label_bg, bd=1, font=(label_font, fnt_size))
    label1.place(relx=0.05, rely=0.2, relwidth=0.15, relheight=0.1)

    usr_name = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, font=entry_font)
    usr_name.place(relx=0.25, rely=0.2, relwidth=0.2, relheight=0.1)

    label2 = tk.Label(labelFrame, text="Phone Number", fg= label_fg, bg= label_bg, bd=1, font=(label_font, fnt_size))
    label2.place(relx=0.05, rely=0.4, relwidth=0.15, relheight=0.1)

    phone = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, font=entry_font)
    phone.place(relx=0.25, rely=0.4, relwidth=0.2, relheight=0.1)
    phone.bind("<FocusOut>", check_phone_exists)

    label3 = tk.Label(labelFrame, text="Address", fg= label_fg, bg= label_bg, bd=1, font=(label_font,fnt_size))
    label3.place(relx=0.05, rely=0.6, relwidth=0.15, relheight=0.1)

    address = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, font=entry_font)
    address.place(relx=0.25, rely=0.6, relwidth=0.2, relheight=0.1)

    label4 = tk.Label(labelFrame, text="User ID", fg= label_fg, bg= label_bg, bd=1, font=(label_font,fnt_size))
    label4.place(relx=0.55, rely=0.2, relwidth=0.15, relheight=0.1)

    usr_id = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, font=entry_font)
    usr_id.place(relx=0.75, rely=0.2, relwidth=0.2, relheight=0.1)
    usr_id.bind("<FocusOut>", check_user_id_exists)  


    label5 = tk.Label(labelFrame, text="Password", fg= label_fg, bg= label_bg, bd=1, font=(label_font,fnt_size))
    label5.place(relx=0.55, rely=0.4, relwidth=0.15, relheight=0.1)

    pswd = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, show='*', font=entry_font)
    pswd.place(relx=0.75, rely=0.4, relwidth=0.2, relheight=0.1)

    label6 = tk.Label(labelFrame, text="Re-enter Password", fg= label_fg, bg= label_bg, bd=1, font=(label_font,fnt_size))
    label6.place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.1)

    rpwd = Entry(labelFrame, bd=2, justify=CENTER, bg= entry_bg, show='*', font=entry_font)
    rpwd.place(relx=0.75, rely=0.6, relwidth=0.2, relheight=0.1)

    btnBack = Button(win2, text="BACK", bg=  btn_bg, fg=  btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=btn_font, command=lambda: goToLogin(callback))
    btnBack.place(relx=0.1, rely=0.72, relwidth=0.3, relheight=0.1)

    btnReg = Button(win2, text="REGISTER", bg=  btn_bg, fg=  btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=btn_font, command=check_details)
    btnReg.place(relx=0.6, rely=0.72, relwidth=0.3, relheight=0.1)

    btnReset = Button(win2, text="RESET", bg=  btn_bg, fg=  btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=btn_font, command=reset)
    btnReset.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.1)

    win2.mainloop()

RegisterPage(Tk())