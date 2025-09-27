import pyodbc

def get_db_connection():
    server = 'Server_Name'
    database = 'DB_Name'
    # !-- UserName & Password does not required if you use windows login --!
    # username = 'your_username'
    # password = 'your_password'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes' #Change the driver according to your machine
    connection = pyodbc.connect(connection_string)
    return connection