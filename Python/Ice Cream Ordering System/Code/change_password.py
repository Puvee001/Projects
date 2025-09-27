from tkinter import *
import tkinter as tk
from tkinter import messagebox as msg
from PIL import ImageTk, Image
from db_connection import get_db_connection

def update_password(uid, old_pwd, new_pwd, change_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM User_Details WHERE user_ID = ?", (uid,))
    result = cursor.fetchone()
    if result and result[0] == old_pwd and change_type == 'change':
        cursor.execute("UPDATE User_Details SET password = ? WHERE user_ID = ?", (new_pwd, uid))
        connection.commit()
        connection.close()
        return True
    elif change_type == 'forget':
        cursor.execute("UPDATE User_Details SET password = ? WHERE user_ID = ?", (new_pwd, uid))
        connection.commit()
        connection.close()
        return True
    connection.close()
    return False

def open_change_password(usid, Type):
    global change_pwd_win, uid, change_type
    global old_password_var, new_password_var, confirm_password_var
    global old_password_entry, new_password_entry, confirm_password_entry

    change_type = Type

    change_pwd_win = tk.Toplevel()
    change_pwd_win.title("Change Password")
    change_pwd_win.geometry('600x550+500+200')
    change_pwd_win.resizable(False, False)

    background_image = ImageTk.PhotoImage(Image.open("paymentbg3.png"))
    background_label = Label(change_pwd_win, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bg_colour = '#FFC1CC'
    lbl_font = ('arial', 15, 'bold italic')
    entry_font = ('arial', 15)

    uid = usid

    show_hide = ImageTk.PhotoImage(Image.open("eye.jpg"))  # 👁️ closed image
    show_open = ImageTk.PhotoImage(Image.open("eye_op.jpg"))      # 👁️ open image

    def create_password_field(parent, label_text, variable):
        frame = Frame(parent, bg=bg_colour)
        frame.pack(pady=10)

        Label(frame, text=label_text, font=lbl_font, bg=bg_colour).pack(anchor="w")

        entry_frame = Frame(frame, bg=bg_colour)
        entry_frame.pack()

        entry = Entry(entry_frame, textvariable=variable, show="*", font=entry_font, bg=bg_colour)
        entry.pack(side="left", pady=5, ipady=3)

        show_state = {"show": True}  # mutable object to toggle

        def toggle_show():
            if show_state["show"]:
                entry.config(show="")
                btn_show.config(image=show_open)
            else:
                entry.config(show="*")
                btn_show.config(image=show_hide)
            show_state["show"] = not show_state["show"]

        btn_show = Button(entry_frame, image=show_hide, command=toggle_show, bg=bg_colour, bd=0, activebackground=bg_colour)
        btn_show.pack(side="left", padx=5)

        return entry

    # Vars for password fields
    old_password_var = StringVar()
    new_password_var = StringVar()
    confirm_password_var = StringVar()

    frame = Frame(change_pwd_win, bg=bg_colour)
    frame.pack(ipady=20, pady=15)

    image_label = Label(frame, image=background_image, bg=bg_colour)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(frame, text="User ID", font=lbl_font, bg=bg_colour).pack(pady=5)
    Label(frame, text=f"{usid}", font=entry_font, bg=bg_colour).pack(pady=5)

    if Type == 'change':
        old_password_entry = create_password_field(frame, "Old Password", old_password_var)

    new_password_entry = create_password_field(frame, "New Password", new_password_var)
    confirm_password_entry = create_password_field(frame, "Confirm New Password", confirm_password_var)

    def check_password():
        old_pwd = old_password_var.get()
        new_pwd = new_password_var.get()
        confirm_pwd = confirm_password_var.get()

        if new_pwd != confirm_pwd:
            msg.showinfo("Error", "New Password and Confirm Password do not match")
            return

        if update_password(uid, old_pwd, new_pwd, change_type):
            msg.showinfo("Success", "Password updated successfully")
            change_pwd_win.destroy()
        else:
            msg.showinfo("Error", "Old Password is incorrect or User ID does not exist")

    Button(change_pwd_win, text="Update Password", font=('arial', 15), command=check_password).pack(pady=20)

    change_pwd_win.mainloop()

# open_change_password('aaa', 'change') # For testing
