from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from db_connection import get_db_connection

from change_password import open_change_password
from ice_cream_builder import *

def change_password():
    open_change_password(usid,'change')
    pass

def order(user_id):
    welcome_win.destroy()
    IceCreamBuilder(user_id)

def log_out():
    welcome_win.destroy()
    from login import loginPage
    # loginPage()

def welcomePage(user_id):
    # Customizing window
    global welcome_win, bg_image,usid
    
    welcome_win = Tk()
    welcome_win.title("Welcome to Ice Cream Shop")
    welcome_win.resizable(False, False)
    welcome_win.state('zoomed')

    # Adding background image
    bg_image = ImageTk.PhotoImage(Image.open("welcome2.png"))
    bg_label = Label(welcome_win, image=bg_image)
    bg_label.place(relwidth=1, relheight=1, relx=0, rely=0.1)


    # Customizing the buttons
    btn_height = 0.5
    btn_width = 0.15
    btn_bg = '#F5D1EF'
    btn_fg = '#4e0852'
    btn_font = ('arial',10)

    txt_bg = 'light blue'
    txt_fg = '#262499'

    # Customizing the labels
    lbl_height = 0.3
    lbl_width = 0.13
    lbl_font = ('Century', 13)
    lbl_bg = 'lavender'
    lbl_fg = "purple"

    usid = user_id

    # Get the user name from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    query = f"SELECT name FROM user_details WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    # Check if the user name is found
    if result:
        user_name = result[0]
    else:
        user_name = "Unknown"

    # Top bar buttons
    top_bg = ImageTk.PhotoImage(Image.open("welcome2.png"))
    top_bar = Frame(welcome_win)
    top_bar.place(relx=0, rely=0, relwidth=1, relheight=0.2)

    # Adding background image to the top bar
    topBar_bg = ImageTk.PhotoImage(Image.open("bg2.png"))
    topBar_bg_label = Label(top_bar, image=topBar_bg)
    topBar_bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    btnChangePassword = Button(top_bar, text="Change Password", bg=btn_bg, fg=btn_fg, font=(btn_font, 10), command=change_password)
    btnChangePassword.place(relx=0.05, rely=0.2, relwidth=btn_width, relheight=btn_height)

    btnOrder = Button(top_bar, text="Order", bg=btn_bg, fg=btn_fg, font=btn_font, command=lambda: order(user_id))
    btnOrder.place(relx=0.28, rely=0.2, relwidth=btn_width, relheight=btn_height)

    btnLogOut = Button(top_bar, text="Log Out", bg=btn_bg, fg=btn_fg, font=btn_font, command=log_out)
    btnLogOut.place(relx=0.51, rely=0.2, relwidth=btn_width, relheight=btn_height)

    userIdLabel = Label(top_bar, text=f"User ID: {user_id}", bg=lbl_bg, fg=lbl_fg, font=lbl_font)
    userIdLabel.place(relx=0.8, rely=0.1, relwidth=lbl_width, relheight=lbl_height)

    nameLabel = Label(top_bar, text=f"NAME: {user_name}", bg=lbl_bg, fg=lbl_fg, font=lbl_font)
    nameLabel.place(relx=0.8, rely=0.55, relwidth=lbl_width, relheight=lbl_height)

   
    # Get the database connection
    db_connection = get_db_connection()

    # Query the database for the last order date
    query = f"""SELECT bill_date,base_count FROM order_details od
                inner join order_summary os on os.order_id = od.order_id
                WHERE os.user_id = '{user_id}' ORDER BY os.date_added DESC"""
    cursor = db_connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    # print('----',result)
    

    # Display the last order date 
    if result:
        order_date = result[0]
        item_count = result[1] if result[1] is not None else '0'
        # print(item_count,order_date)
        prev_order_label = Label(welcome_win, text=f"Last Order Date: {order_date}", bg=txt_bg, fg=txt_fg, font=lbl_font)
        prev_order_label.place(relx=0.2, rely=0.184, relwidth=0.2, relheight=0.05)
        prev_order_count_label = Label(welcome_win, text=f"No of ice creams bought: {item_count}", bg=txt_bg, fg=txt_fg, font=lbl_font)
        prev_order_count_label.place(relx=0.5, rely=0.184, relwidth=0.2, relheight=0.05)

    else:
        no_order_label = Label(welcome_win, text="Go for your first order!", bg=txt_bg, fg=txt_fg, font=lbl_font)
        no_order_label.place(relx=0.3, rely=0.184, relwidth=0.2, relheight=0.05)

    db_connection.close()
    welcome_win.mainloop()

# welcomePage('aaa')  # Test with a sample user ID