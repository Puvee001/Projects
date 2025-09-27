# importing required packages
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox as msg

from change_password import open_change_password
from db_connection import get_db_connection


connection = get_db_connection()
cursor = connection.cursor()

def reset():
    user_id.delete(0, END)
    password.delete(0, END)

# Function to open the change password page
def change_password():
    usid = user_id.get()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM User_Details WHERE user_ID = ?", (usid,))
    result = cursor.fetchone()

    #check if the user ID exists in the database
    if result:
        open_change_password(usid,'forget')
    else:
        msg.showerror('Invalid User ID', "The provided User ID does not exist")
    pass

# Function to move to the register page
def login_to_register():
    reset()
    win.iconify()
    from register import RegisterPage
    RegisterPage(win)

# Function to check the login credentials
def check_Credentials():
    uid = user_id.get()
    pwd = password.get()
    if uid == '' or pwd == '':
        msg.showerror('No Data', "User ID or Password is null")  
        return      
    else:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM User_Details WHERE user_ID = ? AND password = ?", (uid, pwd))
        result = cursor.fetchone()
        # print(result)
        connection.close()
        # result = True  # For testing without database
        if result:
            win.destroy()
            from welcome_window import welcomePage
            welcomePage(uid)
            
        else:
            msg.showerror('Wrong Data', "You have entered wrong password")
            # print("Wrong User ID or Password")

# Customizing window
def loginPage():
    global win, user_id, password, bg_image

    win = Tk()
    win.title("Login Page")
    win.geometry('900x790+300+0')  # width x height + left space + top space
    win.resizable(False, False)

    # Customizing button attributes
    btn_bg = '#E6E6FA'
    btn_fg = '#4e0852'
    btn_font = 'Segoe UI Black'
    btn_active_bg = '#B0B0F8'
    btn_height = 0.08
    btn_width = 0.3

    # Customizing label attributes
    label_width = 0.3
    label_height = 0.2
    label_bg = 'pink'
    label_fg = "black"
    label_font = ('Segoe UI Black', 13)

    # Customizing entry attributes
    entry_width = 0.3
    entry_height = 0.2
    entry_font = ('Times New Roman',13)

    # Adding background image
    bg_image = ImageTk.PhotoImage(Image.open("login.png"))
    bg_label = Label(win, image=bg_image)
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # Customizing display attributes
    headingFrame = tk.Label(win, text="Welcome to", fg="purple", bd=5, font=('arial', 25),bg='#F8E3FB')
    headingFrame.config(anchor='center', justify=CENTER)
    headingFrame.place(relx=0.35, rely=0, relwidth=0.35, relheight=0.05)

    labelFrame = Frame(win, bg=label_bg)
    labelFrame.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.2)

    label1 = tk.Label(labelFrame, text="User ID ", fg=label_fg, bg=label_bg, bd=1, font=label_font)
    label1.place(relx=0.1, rely=0.2, relwidth=label_width, relheight=label_height)

    user_id = Entry(labelFrame, bd=2, justify=CENTER, font=entry_font)
    user_id.place(relx=0.5, rely=0.2, relwidth=entry_width, relheight=entry_height)

    label2 = tk.Label(labelFrame, text="Password ", fg=label_fg, bg=label_bg, bd=1, font=label_font)
    label2.place(relx=0.1, rely=0.6, relwidth=label_width, relheight=label_height)

    password = Entry(labelFrame, bd=2, justify=CENTER, show='*',font=entry_font)
    password.place(relx=0.5, rely=0.6, relwidth=entry_width, relheight=entry_height)

    # Adding buttons
    btnLogin = Button(win, text="Login", bg=btn_bg, fg=btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=(btn_font, 15), command=check_Credentials)
    btnLogin.place(relx=0.1, rely=0.7, relwidth=btn_width, relheight=btn_height)

    btnReg = Button(win, text="New User! Register Now", bg=btn_bg, fg=btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=(btn_font, 15), command=login_to_register)
    btnReg.place(relx=0.6, rely=0.7, relwidth=btn_width, relheight=btn_height)

    btnExit = Button(win, text="Exit", bg=btn_bg, fg=btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=(btn_font, 15), command=win.destroy)
    btnExit.place(relx=0.1, rely=0.85, relwidth=btn_width, relheight=btn_height)

    btnResetPwd = Button(win, text="Forget Password", bg=btn_bg, fg=btn_fg, overrelief=tk.RAISED, activebackground=btn_active_bg, font=(btn_font, 15), command=change_password)
    btnResetPwd.place(relx=0.6, rely=0.85, relwidth=btn_width, relheight=btn_height)

    win.mainloop()

loginPage()