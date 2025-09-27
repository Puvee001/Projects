from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
from datetime import datetime

from order_summary_payment import PaymentPage
from db_connection import get_db_connection


def reset_fields():
    global current_scoop_count, current_ice_creams_made, current_edit_index
    current_scoop_count = 0
    current_ice_creams_made = 0
    current_edit_index = -1

    ice_cream_data.clear()
    selectedList.delete(0, tk.END)
    listCost.delete(0, tk.END)
    labelPrice.config(text='')

    quants.delete( 0, last=None )
    base_selected.set('')
    scoops.delete(0, tk.END)
    base_selected.config(state='disabled')
    scoops.config(state='disabled')
    flavour.set('')
    flavour.config(state='disabled')
    btnAddBase.config(state='disabled')
    btnAddFlavour.config(state='disabled')
    btnBuild.config(state='disabled')


def get_base_pricing():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Base_name, price FROM IceCream_Bases")
    base_pricing = {row.Base_name: row.price for row in cursor.fetchall()}
    conn.close()
    return base_pricing

def get_flavour_pricing():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT flavour_name, price FROM IceCream_Flavours")
    flav_pricing = {row.flavour_name: row.price for row in cursor.fetchall()}
    conn.close()
    return flav_pricing

base_pricing = get_base_pricing()
bases = [f"{name} ({price})" for name, price in base_pricing.items()]
base_name_map = {f"{name} ({price})": name for name, price in base_pricing.items()}

flav_pricing = get_flavour_pricing()
flavours = [f"{name} ({price})" for name, price in flav_pricing.items()]
flav_name_map = {f"{name} ({price})": name for name, price in flav_pricing.items()}

current_scoop_count = 0
total_ice_creams_needed = 0
current_ice_creams_made = 0
current_edit_index = -1


ice_cream_data = []

def go_back(user_id):
    reset_fields()
    ordwin.destroy()
    from welcome_window import welcomePage
    welcomePage(user_id)

def submit():
    ordered_items = ''
    total_price = 0
    total_items = 0  # Initialize the total items counter
    total_bases = 0
    total_flavours = 0
    base_count = quants.get()
    for ice_cream in ice_cream_data:
        base = ice_cream['base']
        scoops = ice_cream['scoops']
        flavors = ice_cream['flavours']

        # Add the base and its price
        item_string = base + ":" + str(base_pricing[base])
        total_price += base_pricing[base]
        total_bases += 1  # Count Increment for the base

        # Add the flavors and their prices
        for flav in flavors:
            item_string += "," + flav + ":" + str(flav_pricing[flav])
            total_price += flav_pricing[flav]
            total_flavours += 1  # Count Increment for each flavor
            
        ordered_items += item_string + ","
        # print(ordered_items)
    ordered_items = ordered_items.strip(",")
    total_items = total_bases + total_flavours  # Total items is the sum of bases and flavors

    # Insert the order into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f'INSERT INTO Order_Summary (ordered_items, total_price, user_id, Item_Count, base_count, flavour_count, date_added) VALUES (\'{ordered_items}\', {total_price}, \'{uid}\', {total_items}, {total_bases}, {total_flavours}, ?)',
        (datetime.now(),)
    )
    conn.commit()
    conn.close()

    # Close the order window and proceed to the payment page
    ordwin.destroy()
    PaymentPage(uid)


def bill_calculate():
    total = 0
    for ice_cream in ice_cream_data:
        cost = base_pricing[ice_cream['base']] + sum(flav_pricing[f] for f in ice_cream['flavours'])
        total += cost
    labelPrice.config(text=f'{total}')

def add_base():
    global current_scoop_count, current_ice_creams_made, current_edit_index

    base_display = base_selected.get()
    base = base_name_map.get(base_display)
    try:
        scoop_num = int(scoops.get())
    except ValueError:
        return

    if base and scoop_num > 0:
        ice_cream_data.append({
            'base': base,
            'scoops': scoop_num,
            'flavours': []
        })

        current_edit_index = len(ice_cream_data) - 1
        current_scoop_count = scoop_num
        current_ice_creams_made += 1

        base_selected.set('')
        base_selected.config(state='disabled')
        scoops.config(state='disabled')
        flavour.config(state='normal')
        btnAddBase.config(state='disabled')
        btnAddFlavour.config(state='normal')

        update_selected_list()
        bill_calculate()

def add_flavour():
    global current_scoop_count, current_edit_index

    scoop_display = flavour.get()
    scoop = flav_name_map.get(scoop_display)
    if not scoop or current_edit_index == -1:
        return

    ice_cream_data[current_edit_index]['flavours'].append(scoop)
    current_scoop_count -= 1

    flavour.set('')
    update_selected_list()
    bill_calculate()

    if current_scoop_count == 0:
        current_edit_index = -1

        base_selected.set('')
        scoops.delete(0, tk.END)
        base_selected.config(state='normal')
        scoops.config(state='normal')
        flavour.set('')
        flavour.config(state='disabled')
        btnAddFlavour.config(state='disabled')
        btnAddBase.config(state='normal')

        if current_ice_creams_made == total_ice_creams_needed:
            btnAddBase.config(state='disabled')
            btnBuild.config(state='normal')
            messagebox.showinfo("Information", "All scoops added. Click Build to proceed.")

def remove_ice():
    global current_ice_creams_made, current_scoop_count, current_edit_index

    index = selectedList.curselection()
    if not index:
        return

    idx = index[0]
    flat_list = []

    for i, ice_cream in enumerate(ice_cream_data):
        flat_list.append((i, 'base', ice_cream['base']))
        for j, flav in enumerate(ice_cream['flavours']):
            flat_list.append((i, 'flavour', j, flav))

    if idx >= len(flat_list):
        return

    selected = flat_list[idx]

    if selected[1] == 'base':
        del ice_cream_data[selected[0]]
        current_ice_creams_made -= 1
        current_scoop_count = 0
        current_edit_index = -1

        base_selected.set('')
        scoops.delete(0, tk.END)
        base_selected.config(state='normal')
        scoops.config(state='normal')
        flavour.set('')
        flavour.config(state='disabled')
        btnAddBase.config(state='normal')
        btnAddFlavour.config(state='disabled')
        btnBuild.config(state='disabled')

        messagebox.showinfo("Information", "Base and its flavours removed. Please re-add.")

    elif selected[1] == 'flavour':
        i = selected[0]
        j = selected[2]
        del ice_cream_data[i]['flavours'][j]
        current_scoop_count = ice_cream_data[i]['scoops'] - len(ice_cream_data[i]['flavours'])
        current_edit_index = i

        flavour.set('')
        flavour.config(state='normal')
        btnAddFlavour.config(state='normal')
        base_selected.config(state='disabled')
        scoops.config(state='disabled')
        btnAddBase.config(state='disabled')
        btnBuild.config(state='disabled')

        messagebox.showinfo("Information", f"Flavour removed. Please add {current_scoop_count} more scoop(s).")

    update_selected_list()
    bill_calculate()

def update_selected_list():
    selectedList.delete(0, tk.END)
    listCost.delete(0, tk.END)

    for ice_cream in ice_cream_data:
        base = ice_cream['base']
        flavours = ice_cream['flavours']

        selectedList.insert(tk.END, base )
        listCost.insert(tk.END, f"{base_pricing[base]}")
        total_cost = base_pricing[base]

        for flav in flavours:
            selectedList.insert(tk.END, f"  └ {flav}")
            # selectedList.insert(tk.END, f"  └ {flav}")
            total_cost += flav_pricing[flav]
            listCost.insert(tk.END, f"{flav_pricing[flav]}")

        # listCost.insert(tk.END, total_cost)

def enable_fields(*args):
    global total_ice_creams_needed, current_ice_creams_made
    try:
        total_ice_creams_needed = int(quants.get())
        current_ice_creams_made = 0
        base_selected.config(state='normal')
        scoops.config(state='normal')
        flavour.config(state='disabled')
        btnAddBase.config(state='normal')
        btnBuild.config(state='disabled')
    except ValueError:
        base_selected.config(state='disabled')
        scoops.config(state='disabled')
        flavour.config(state='disabled')
        btnAddBase.config(state='disabled')
        btnBuild.config(state='disabled')

def IceCreamBuilder(user_id):
    global ordwin, base_selected, scoops, flavour, selectedList, listCost, labelPrice
    global btnAddBase, btnAddFlavour, btnBuild, quants, uid, selectedwin

    # Initialize variables
    uid = user_id

    lbl_width = 0.3
    lbl_height = 0.05
    lbl_fg = 'black'
    lbl_bg = 'light blue'
    lbl_font = ('Cavolini', 13, 'bold')

    entry_width = 0.4
    entry_height = 0.05
    entry_fg = 'black'
    entry_bg = 'white'
    entry_font = ('Cavolini', 13, 'bold')

    tot_bg = '#DED5F8'
    tot_fg = '#843799'
    tot_font = ('Cavolini', 13, 'bold')

    btn_bg = '#DED5F8'
    btn_fg = '#843799'
    btn_font = ('Broadway', 13)
    btn_width = 0.2
    btn_height = 0.08

    ordwin = Tk()
    ordwin.title("Order Page")
    ordwin.resizable(False, False)
    ordwin.state('zoomed')

    bg_image = ImageTk.PhotoImage(Image.open("bld.png"))
    bg_label = Label(ordwin, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    bg_colour = 'light blue'

    builder_frame = Frame(ordwin, bg='light blue')
    builder_frame.place(relx=0.05, rely=0.05, relwidth=0.65, relheight=0.9)
    
    builder_bg_image = ImageTk.PhotoImage(Image.open("build1.png"))
    builder_bg_label = Label(builder_frame, image=builder_bg_image)
    builder_bg_label.place(relwidth=1, relheight=1)

    selectedwin = Frame(ordwin, bg='white')
    selectedwin.place(relx=0.72, rely=0.05, relwidth=0.23, relheight=0.9)

    selected_bg_image = ImageTk.PhotoImage(Image.open("build2.png"))
    selected_bg_label = Label(selectedwin, image=selected_bg_image)
    selected_bg_label.place(relwidth=1, relheight=1)

    headingFrame = tk.Label(builder_frame, text="Build your Ice Cream", fg="purple", bd=5, font=('arial', 20), bg='light blue')
    headingFrame.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.1)

    label1 = tk.Label(builder_frame, text="Number of Ice Creams needed", fg=lbl_fg, bg=lbl_bg, bd=1, font=lbl_font)
    label1.place(relx=0.05, rely=0.15, relwidth=lbl_width, relheight=lbl_height)

    quants = Entry(builder_frame, bd=2, justify=CENTER, fg=entry_fg, bg=entry_bg, font=entry_font)
    quants.place(relx=0.5, rely=0.15, relwidth=entry_width, relheight=entry_height)
    quants.bind('<KeyRelease>', enable_fields)
    
    label2 = tk.Label(builder_frame, text="Choose the base", fg=lbl_fg, bg=lbl_bg, bd=1, font=lbl_font)
    label2.place(relx=0.05, rely=0.25, relwidth=lbl_width, relheight=lbl_height)

    base_selected = ttk.Combobox(builder_frame, value=bases, justify=CENTER, font = entry_font, state='disabled')
    base_selected.place(relx=0.5, rely=0.25, relwidth=entry_width, relheight=entry_height)

    label3 = tk.Label(builder_frame, text="Number of Scoops needed", fg=lbl_fg, bg=lbl_bg, bd=1, font=lbl_font)
    label3.place(relx=0.05, rely=0.35, relwidth=lbl_width, relheight=lbl_height)

    scoops = Entry(builder_frame, bd=2, justify=CENTER, fg=entry_fg, bg=entry_bg, font=entry_font,  state='disabled')
    scoops.place(relx=0.5, rely=0.35, relwidth=entry_width, relheight=entry_height)

    label4 = tk.Label(builder_frame, text="Flavours", fg=lbl_fg, bg=lbl_bg, bd=1, font=lbl_font)
    label4.place(relx=0.05, rely=0.45, relwidth=lbl_width, relheight=lbl_height)

    flavour = ttk.Combobox(builder_frame, value=flavours, font = entry_font, state='disabled')
    flavour.place(relx=0.5, rely=0.45, relwidth=entry_width, relheight=entry_height)

    btnAddBase = Button(builder_frame, text="Add Base", bg=btn_bg, fg=btn_fg, font=btn_font, state='disabled', command=add_base)
    btnAddBase.place(relx=0.1, rely=0.6, relwidth=btn_width, relheight=btn_height)

    btnAddFlavour = Button(builder_frame, text="Add Flavour", bg=btn_bg, fg=btn_fg, font=btn_font, state='disabled', command=add_flavour)
    btnAddFlavour.place(relx=0.65, rely=0.6, relwidth=btn_width, relheight=btn_height)

    btnBuild = Button(builder_frame, text="Build", bg=btn_bg, fg=btn_fg, font=btn_font, state='disabled', command=submit)
    btnBuild.place(relx=0.37, rely=0.7, relwidth=btn_width, relheight=btn_height)

    btnBack = Button(builder_frame, text="BACK", bg=btn_bg, fg=btn_fg, font=btn_font, command=lambda: go_back(user_id))
    btnBack.place(relx=0.1, rely=0.8, relwidth=btn_width, relheight=btn_height)

    btnReset = Button(builder_frame, text="Reset", bg=btn_bg, fg=btn_fg, font=btn_font, command=lambda: reset_fields())
    btnReset.place(relx=0.65, rely=0.8, relwidth=btn_width, relheight=btn_height)

    selectedList = tk.Listbox(selectedwin, bg='white', font=("arial", 10), justify='left', selectbackground='#DED5F8', selectforeground='black')
    selectedList.place(relx=0.05, rely=0.05, relwidth=0.7, relheight=0.8)

    listCost = tk.Listbox(selectedwin, bg='black', fg='white', font=lbl_font, justify='center')
    listCost.place(relx=0.77, rely=0.05, relwidth=0.18, relheight=0.8)

    labeltot = tk.Label(selectedwin, text="Total :", fg=tot_fg, bg=tot_bg, font=tot_font)
    labeltot.place(relx=0.05, rely=0.88, relwidth=0.4, relheight=0.05)

    labelPrice = tk.Label(selectedwin, text="", fg=tot_fg, bg=tot_bg, font=tot_font)
    labelPrice.place(relx=0.5, rely=0.88, relwidth=0.4, relheight=0.05)

    btnMelt = Button(selectedwin, text="Melt", bg='orange', fg='#4e0852', font=('Broadway', 10), command=remove_ice)
    btnMelt.place(relx=0.35, rely=0.94, relwidth=0.3, relheight=0.05)

    ordwin.mainloop()

# IceCreamBuilder('aaa')
