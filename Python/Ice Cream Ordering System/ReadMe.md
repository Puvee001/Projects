# **Ice Cream Ordering System**



This project is a desktop-based Ice Cream Ordering System built with Python and the Tkinter GUI toolkit. It provides an interactive, user-friendly interface for customers to register, log in, build custom ice cream orders, make payments, and manage account details. The backend uses an SQL Server database accessed via 'pyodbc'.



**Features**



\- User Registration \& Login: Secure registration and authentication system.

\- Password Management: Change and reset password functionality.

\- Ice Cream Builder: Custom ice cream ordering with selection of bases,  number of scoops, and flavours, including dynamic pricing.

\- Order Summary \& Payment: Detailed order summary view, multiple payment options (Credit/Debit Card, Net Banking, UPI, Cash).

\- Bill Generation: Generates and saves a printable bill for each order.

\- User Dashboard: View last order date and purchase summary upon login.

\- Database Integration: All user and order data is stored in an SQL Server database.



**Requirements**



\- Python 3.x

\- Tkinter

\- pyodbc ('pip install pyodbc')

\- Pillow ('pip install pillow')

\- SQL Server 

\- Image files for UI (PNG/JPG files referenced in the code should be present in the project directory)



**File Overview**



\- 'login.py' — User authentication and main login window.

\- 'register.py' — Handles new user registration.

\- 'change\_password.py' — Allows users to change or reset their password.

\- 'db\_connection.py' — Database connection utility.

\- 'welcome\_window.py' — Dashboard after login; shows user info and order actions.

\- 'ice\_cream\_builder.py' — UI for building custom ice cream orders.

\- 'order\_summary\_payment.py' — Displays order summary, collects payment, and generates bill.

\- 'generate\_bill.py' — Generates and saves the bill as a text file.



**How to Run**



1\. Clone/download the project and ensure all '.py' and required image files are in the same directory.

2\. Configure the 'db\_connection.py' file with your SQL Server details.

3\. Run 'login.py' to start the application:

4\. Register a new user or log in with an existing account to begin ordering.



**Database Setup**



Ensure your database has the following tables:



\- 'User\_Details' (with columns: name, phone\_number, address, user\_ID, password, etc.)

\- 'Order\_Summary' (ordered\_items, total\_price, user\_id, Item\_Count, base\_count, flavour\_count, date\_added)

\- 'Order\_Details' (order\_id, member\_id, name, member\_phone\_number, bill\_address, bill\_amount, payment\_method, bill\_date)

\- 'IceCream\_Bases' and 'IceCream\_Flavours' (base/flavour names, prices)





**Enhancement Ideas**



\- Add more ice cream bases/flavours to the database.

\- Implement admin features for managing inventory and viewing sales.

\- Add email/SMS notifications on order completion.

\- Enhance GUI with more advanced effects or animations.





🍦 Enjoy building and ordering your favorite ice creams! 🍦

