from datetime import datetime
from db_connection import get_db_connection
import os
import stat


# Function to get user details from the database
def get_order_info(uid, orid):
    conn = get_db_connection()
    cursor = conn.cursor() 
    qry = f"""
        SELECT ud.Member_ID, ud.Name, Member_Phone_number, Bill_Date, Payment_method, bill_address 
        FROM Order_Details od
        INNER JOIN User_Details ud ON od.Member_id = ud.Member_ID 
        WHERE User_ID = '{uid}'
        AND Order_ID = '{orid}'
    """
    cursor.execute(qry)
    row = cursor.fetchone()
    conn.close()

    if row:
        order_info = list(row[i] for i in range(len(row)))
        # print(f"User details: {order_info}")
        return order_info
    else:
        print("No user details found.")
        return []

# Function to get ordered items from the database
def get_order_items(oid):
    conn = get_db_connection()
    cursor = conn.cursor() 
    qry = f"SELECT ordered_items FROM Order_Summary WHERE Order_ID = '{oid}' ORDER BY date_added DESC"
    cursor.execute(qry)
    row = cursor.fetchone()
    conn.close()

    if row is not None:
        items_str = row[0]  # e.g., "Ice Cream:100, Chocolate:50"
        try:
            items_raw = items_str.split(",")
            items_Ordered = []
            for item in items_raw:
                if ":" in item:
                    name, price = item.strip().split(":")
                    items_Ordered.append((name.strip(), int(price.strip())))
                else:
                    print(f"BILL: Invalid item format: {item}")
            return items_Ordered
        except Exception as e:
            print(f"Error parsing ordered items: {e}")
            return []
    else:
        print("No order items found.")
        return []

# Function to generate and save the bill in text format
def generate_bill(user_id, order_id):
    count = 0
    order_info = get_order_info(user_id, order_id)
    if not order_info:
        return

    order_items = get_order_items(order_id)
    if not order_items:
        return

    # Unpacking user details
    member_id, name, phone, bill_date, payment_method, address = order_info

    # Calculate total
    total_amount = sum(price for _, price in order_items)

    # Format bill date
    bill_date_str = datetime.strptime(str(bill_date), "%Y-%m-%d").strftime("%d-%m-%Y")

    # Generate bill content
    bill_lines = [
        "    Mystry Ice Cream Store",
        "    **************************************",
        "",
        f"    Bill Date: {bill_date_str}",
        f"    Order ID: {order_id}",
        "",
        "    Customer Details:",
        f"    Name: {name}",
        f"    Phone: {phone}",
        f"    Address: {address}",
        "",
        "    Order Summary:",
        "    Item                   Price",
        "    -------------------------------"
    ]

    for item, price in order_items:
        # Align item name and price
        bill_lines.append(f"    {item.ljust(23)} ₹{price}")
        count+=1

    bill_lines += [
        "",
        f"    Total: ₹{total_amount}",
        "",
        f"    Payment Method: {payment_method}",
        "",
        "",
        f"    Total items: {count}",
        "",
        "",
        "    **************************************",
        "     😊 Thanks for shopping with us 😊",
        "         🍦 Enjoy your ice cream 🍦",
        "    **************************************"
    ]

    # Join all lines
    bill_text = "\n".join(bill_lines)

    # Save to text file
    file_name = f"bill_{order_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(file_name, "w", encoding="utf-8") as bill_file:
        bill_file.write(bill_text)

    print(f"Bill generated and saved to {file_name}")
    os.startfile(file_name) # Open the file after saving


# Example usage
# generate_bill('aaa', '1055')
