import pyodbc
from db_connection import get_db_connection
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import Canvas, Frame, Label, Entry, Button, Radiobutton, StringVar
from PIL import ImageTk, Image
from datetime import datetime
from generate_bill import generate_bill

# Function to go back to the previous window
def go_back(ord_id, user_id):
    # Delete the order from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_summary WHERE order_id = ?", (ord_id,))
    conn.commit()
    conn.close()
    from ice_cream_builder import IceCreamBuilder
    IceCreamBuilder(user_id)

def insert_billing_details(order_id, user_details, address, total_price, payment_mode):
    # Insert billing details into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current date and time
    current_time = datetime.now().date()
    
    # Prepare the SQL query
    sql_query = (f'INSERT INTO Order_details (order_id, member_id, name, member_phone_number, bill_address, bill_amount, payment_method, bill_date) VALUES (\'{order_id}\', \'{user_details[3]}\', \'{user_details[0]}\', \'{user_details[1]}\', \'{address}\', \'{total_price}\', \'{payment_mode}\', \'{current_time}\')')
    # print(sql_query)  # Debugging line to check the SQL query
    # Execute the SQL query
    cursor.execute(sql_query)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def PaymentPage(user_id):
    # Get user details from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone_number, address, member_id FROM user_details WHERE user_id = ?", (user_id,))
    user_details = cursor.fetchone()

    # Get the latest order from the database
    cursor.execute("SELECT order_id, ordered_items, total_price FROM order_summary WHERE user_id = ? ORDER BY date_added DESC", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        order_id, ordered_items, total_price = row
        try:
            # Convert ordered items string to a list of tuples
            # print("ordered_items", ordered_items)
            item_list = [tuple(i.strip().split(":")) for i in ordered_items.split(",")]
            item_list = [(item, int(price)) for item, price in item_list]
            # print("item_list", item_list)
        except Exception as e:
            print("ORDSUMM: Error parsing ordered items:", e)
            item_list = []
    else:
        order_id, item_list, total_price = None, [], 0

    # Create the main payment window
    payment_win = tk.Tk()
    payment_win.title("Payment Page")
    payment_win.state('zoomed')  # Open window in maximized state
    payment_win.resizable(False, False)  # Disable resizing
    
    # Initially uncheck all payment buttons
    payment_var = tk.StringVar()  
    payment_var.set(None)
    
    address_var = StringVar(value=user_details[2])
    total_var = StringVar(value=f"Total: ₹{total_price}")
    
    #adding image to the background
    bg_image = ImageTk.PhotoImage(Image.open("summarytop.png"))
    bg_label = Label(payment_win, image=bg_image)
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=0.2)

    bg_image1 = ImageTk.PhotoImage(Image.open("summary.png"))
    bg_label1 = Label(payment_win, image=bg_image1)
    bg_label1.place(relx=0, rely=0.2, relwidth=1, relheight=1)

    # Background and foreground colors
    bg_color = 'light blue'
    fg_color = 'black'
    heading_bg_color = 'light blue'
    heading_fg_color = 'blue'
    user_bg_color = 'pink'
    user_fg_color = 'black'
    order_bg_color = 'light grey'
    order_fg_color = 'black'
    payment_bg_color = 'light blue'
    payment_fg_color = 'black'
    button_bg_color = 'pink'
    button_fg_color = '#4e0852'
    button_active_bg_color = '#b911c2'
    payment_button_bg_color = '#d153ed'


    # Adding background color
    # payment_win.configure(bg=bg_color)

    def show_payment_window(payment_mode):
        # Create a new top-level window for payment details
        payment_window = tk.Toplevel(payment_win)
        payment_window.title("Payment Details")
        payment_window.geometry('400x300')
        
        # Center the payment window on the screen
        payment_window.update_idletasks()
        width = payment_window.winfo_width()
        height = payment_window.winfo_height()
        x = (payment_window.winfo_screenwidth() // 2) - (width // 2)
        y = (payment_window.winfo_screenheight() // 2) - (height // 2)
        payment_window.geometry(f'{width}x{height}+{x}+{y}')

        # ----- ADD BACKGROUND IMAGE -----
        bg_image_payment = ImageTk.PhotoImage(Image.open("paymentbg5.png"))  # <-- your payment window background
        bg_label_payment = Label(payment_window, image=bg_image_payment)
        bg_label_payment.place(relwidth=1, relheight=1)
        payment_window.bg_image_payment = bg_image_payment  

        def proceed_to_billing():
            payment_window.destroy()
            insert_billing_details(order_id, user_details, address_var.get(), total_price, payment_mode)
            generate_bill(user_id, order_id)
            exit_to_welcome()

        def make_payment():
            if payment_mode == "Net Banking":
                banking_id = banking_id_var.get()
                banking_password = banking_password_var.get()
                if banking_id and banking_password:
                    msg.showinfo("Success", "Payment Successful")
                    msg.showinfo("Order successful", "Your order has been placed successfully!\nExpect delivery soon.")
                    proceed_to_billing()
                else:
                    msg.showinfo("Error", "Please enter Banking ID and Password")
            elif payment_mode == "UPI":
                upi_id = upi_id_var.get()
                if upi_id:
                    msg.showinfo("Success", "Payment Successful")
                    msg.showinfo("Order successful", "Your order has been placed successfully!\nExpect delivery soon.")
                    proceed_to_billing()
                else:
                    msg.showinfo("Error", "Please enter UPI ID")
            elif payment_mode == "Credit Card" or payment_mode == "Debit Card":
                card_number = card_number_var.get()
                card_cvv = card_cvv_var.get()
                if card_number and card_cvv:
                    msg.showinfo("Success", "Payment Successful")
                    msg.showinfo("Order successful", "Your order has been placed successfully!\nExpect delivery soon.")
                    proceed_to_billing()
                else:
                    msg.showinfo("Error", "Please enter Card Number and CVV")
            

        if payment_mode == "Net Banking":
            banking_id_var = StringVar()
            banking_password_var = StringVar()
            tk.Label(payment_window, text="Banking ID:", bg=payment_bg_color, fg=payment_fg_color, font=('Cavolini', 12)).pack(padx=10, pady=5, anchor="w")
            tk.Entry(payment_window, textvariable=banking_id_var, font=('Cavolini', 12)).pack(padx=10, pady=5, fill="x")
            tk.Label(payment_window, text="Password:", bg=payment_bg_color, fg=payment_fg_color, font=('Cavolini', 12)).pack(padx=10, pady=5, anchor="w")
            tk.Entry(payment_window, textvariable=banking_password_var, font=('Cavolini', 12), show="*").pack(padx=10, pady=5, fill="x")
        elif payment_mode == "UPI":
            upi_id_var = StringVar()
            tk.Label(payment_window, text="UPI ID:", bg=payment_bg_color, fg=payment_fg_color, font=('Cavolini', 12)).pack(padx=10, pady=5, anchor="w")
            tk.Entry(payment_window, textvariable=upi_id_var, font=('Cavolini', 12)).pack(padx=10, pady=5, fill="x")
        elif payment_mode == "Credit Card" or payment_mode == "Debit Card":
            card_number_var = StringVar()
            card_cvv_var = StringVar()
            tk.Label(payment_window, text="Card Number:", bg=payment_bg_color, fg=payment_fg_color, font=('Cavolini', 12)).pack(padx=10, pady=5, anchor="w")
            tk.Entry(payment_window, textvariable=card_number_var, font=('Cavolini', 12)).pack(padx=10, pady=5, fill="x")
            tk.Label(payment_window, text="CVV:", bg=payment_bg_color, fg=payment_fg_color, font=('Cavolini', 12)).pack(padx=10, pady=5, anchor="w")
            tk.Entry(payment_window, textvariable=card_cvv_var, font=('Cavolini', 12), show="*").pack(padx=10, pady=5, fill="x")

        tk.Button(payment_window, text="Make Payment", bg=payment_button_bg_color, fg=button_fg_color, overrelief=tk.RAISED, activebackground=button_active_bg_color, font=('arial', 10), command=make_payment).pack(pady=10)

    def proceed_to_payment():
        payment_mode = payment_var.get()
        if payment_mode == "":
            msg.showinfo("Error", "Please select a payment mode")
            return
        if payment_mode == "Cash":
            msg.showinfo("Success", "Your order will be delivered soon! Pay with cash on delivery.")
            insert_billing_details(order_id, user_details, address_var.get(), total_price, payment_mode)
            generate_bill(user_id, order_id)
            exit_to_welcome()
        else:
            show_payment_window(payment_mode)

    def exit_to_welcome():
        payment_win.destroy()
        from welcome_window import welcomePage
        welcomePage(user_id)

    def process_ordered_items(ordered_items_str):
        try:
            # Split the ordered items by commas first
            item_list = ordered_items_str.split(",")
            
            # Parse each item into a tuple of (item_name, price)
            parsed_items = []
            for item in item_list:
                item = item.strip()

                # Handle different separators (':', ',')
                if ":" in item:
                    item_name, price = item.split(":")
                elif "," in item:
                    item_name, price = item.split(",")
                else:
                    print(f"Invalid item format: {item}")
                    continue

                # Clean up the item name and price
                item_name = item_name.strip()
                price = price.strip()

                try:
                    # Convert price to an integer, ensure it's a valid number
                    parsed_items.append((item_name, int(price)))
                except ValueError:
                    print(f"Invalid price format for {item_name}: {price}")
                    continue

            return parsed_items
        except Exception as e:
            print(f"Error parsing ordered items: {e}")
            return []

    # Test Usage
    # ordered_items = "Waffle cone:15, mango:63,chocolate bowl:68, cookies and cream:175"  # Example

    parsed_items = process_ordered_items(ordered_items)
    # print(parsed_items,'parsed_items')

    # Customizing display attributes
    headingFrame = tk.Label(payment_win, text="Check your order and proceed to payment", fg=heading_fg_color, bd=5, font=('arial', 30), bg=heading_bg_color)
    headingFrame.pack(fill="x", pady=5)

    userFrame = tk.Frame(payment_win, bg=user_bg_color, bd=2, relief=tk.RIDGE, height=150, width=300)
    userFrame.pack(padx=20, pady=5)
    userFrame.pack_propagate(False)

    user_label = tk.Label(userFrame, text="User Details", fg=user_fg_color, bg=user_bg_color, bd=1, font=('Cavolini', 15, 'bold'))
    user_label.pack(pady=2)
    user_details_disp = tk.Label(userFrame, text=f"Name: {user_details[0]}\nPhone: {user_details[1]}", fg=user_fg_color, bg=user_bg_color, bd=1, font=('Cavolini', 15))
    user_details_disp.pack(padx=10, pady=5)
    address_entry = tk.Entry(userFrame, textvariable=address_var, font=('Cavolini', 15), width=30)
    address_entry.pack(padx=10, pady=5)

    orderFrame = tk.Frame(payment_win, bg=order_bg_color, bd=2, relief=tk.RIDGE, height=250, width = 600)
    orderFrame.pack(padx=29, pady=5)
    orderFrame.pack_propagate(False)

    order_label = tk.Label(orderFrame, text="Order Summary", fg=order_fg_color, bg=order_bg_color, bd=1, font=('Cavolini', 15, 'bold'), justify='center')
    order_label.pack(pady=10)

    order_canvas = tk.Canvas(orderFrame, bg=order_bg_color)
    order_canvas.pack(side=tk.LEFT,fill="both", expand=1)

    scrollbar = tk.Scrollbar(orderFrame, orient="vertical", command=order_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    order_canvas.configure(yscrollcommand=scrollbar.set)
    order_canvas.bind('<Configure>', lambda e: order_canvas.configure(scrollregion=order_canvas.bbox("all")))

    order_summary_frame = tk.Frame(order_canvas, bg=order_bg_color)
    order_canvas.create_window((0, 0), window=order_summary_frame, anchor="center")

    for item, price in parsed_items:
        tk.Label(order_summary_frame, text=f"{item} - ₹{price}", bg=order_bg_color, font=('Cavolini', 12), justify='center', anchor="center").pack(fill="x", padx=9, pady=2)
    
    total_label = tk.Label(payment_win, textvariable=total_var, fg=heading_fg_color, bg=bg_color, bd=1, font=('Cavolini', 15), justify='center')
    total_label.pack(pady=10)

    paymentFrame = tk.Frame(payment_win, bg=payment_bg_color, bd=2, relief=tk.RIDGE, height=100, width=400)
    paymentFrame.pack(padx=20, pady=5)
    paymentFrame.pack_propagate(False)

    payment_label = tk.Label(paymentFrame, text="Select Payment Mode:", fg=payment_fg_color, bg=payment_bg_color, bd=1, font=('Cavolini', 15), justify='center')
    payment_label.grid(row=0, column=0, columnspan=6, pady=10)

    payment_modes = ["Credit Card", "Debit Card", "Net Banking", "UPI", "Cash"]
    for idx, mode in enumerate(payment_modes):
        rb = tk.Radiobutton(paymentFrame, text=mode, variable=payment_var, value=mode, bg=payment_bg_color, font=('Cavolini', 12))
        rb.grid(row=1 + idx // 6, column=idx % 6, padx=20, pady=5, sticky=tk.W)

    btnBack = tk.Button(payment_win, text="BACK", bg=button_bg_color, fg=button_fg_color, overrelief=tk.RAISED, activebackground=button_active_bg_color, font=('arial', 10), command=lambda: [payment_win.destroy(), go_back(order_id, user_id)])
    btnBack.pack(side=tk.LEFT, padx=20, pady=10)

    btnPay = tk.Button(payment_win, text="Proceed to Payment", bg=payment_button_bg_color, fg=button_fg_color, overrelief=tk.RAISED, activebackground=button_active_bg_color, font=('arial', 10), command=proceed_to_payment)
    btnPay.pack(side=tk.RIGHT, padx=20, pady=10)

    btnExit = tk.Button(payment_win, text="EXIT", bg=button_bg_color, fg=button_fg_color, overrelief=tk.RAISED, activebackground=button_active_bg_color, font=('arial', 10), command=exit_to_welcome)
    btnExit.pack(side=tk.BOTTOM, pady=10)

    # show_payment_window("Credit Card")  # Show the payment window for cash by default
    payment_win.mainloop()

# PaymentPage('star')

