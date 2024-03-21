import sqlite3
from tkinter import messagebox

def Create_Database(Database_Name):
   conn = sqlite3.connect(Database_Name)
   conn.commit
   conn.close()
#Creates table under the circumstance it doesn't exist
def Create_User_Data(Database_Name):
  conn = sqlite3.connect(Database_Name)
  
  c = conn.cursor()
  
  c.execute("""CREATE TABLE IF NOT EXISTS User_Data(
      User_ID INTEGER PRIMARY KEY,
      Username TEXT,
      Password TEXT,
      Log TEXT,
      Privileges INTEGER
  )
  """)
  conn.commit()

  conn.close()

#Displays the table when called
def Show_Table(Database_Name, Table_Name):
  conn = sqlite3.connect(Database_Name)

  c = conn.cursor()

  c.execute(f"SELECT * FROM {Table_Name}")
  
  Users = c.fetchall()
  
  for User in Users:
    print(User)
  
  conn.close()

#Creates a user to add to the database
def Add_User(Database_Name, Table_Name, User_ID, Username, Password, Privelege):
  conn = sqlite3.connect(Database_Name)
  c = conn.cursor()

  Log_Name = f"Log_{User_ID}.dat"

  c.execute(f"INSERT INTO {Table_Name} VALUES (?, ?, ?, ?, ?)",
  (User_ID, Username, Password, Log_Name, Privelege))

  conn.commit()

  conn.close()

#Deletes a user from the database
def Delete_User(Database_Name, Table_Name, User_ID):
  conn = sqlite3.connect(Database_Name)

  c = conn.cursor()

  c.execute(f"DELETE FROM {Table_Name} WHERE User_ID = ?", (User_ID,))

  conn.commit()

  conn.close()

  messagebox.showinfo("Successful", f"Successfully removed User: {User_ID}")

#Validate User from the database
def validate_login(username, password, database_name, table_name):
  # Connect to the SQLite database
  conn = sqlite3.connect(f'{database_name}.db')
  c = conn.cursor()

  # Fetch the record corresponding to the entered username
  c.execute(f"SELECT * FROM {table_name} WHERE Username=?", (username,))
  user_record = c.fetchone()

  if user_record:
      # Check if the entered password matches the password in the database
      if password == user_record[2]:  # Assuming Password is at index 2
          messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
      else:
          messagebox.showerror("Login Failed", "Incorrect password!")
  else:
      messagebox.showerror("Login Failed", "Username not found!")

  # Close the database connection
  conn.close()

def check_username_existence(username, table_name):
  """
  Check if a username already exists in the specified table.

  Args:
    username (str): The username to check for existence.
    table_name (str): The name of the table to search for the username.

  Returns:
    bool: True if the username exists in the table, False otherwise.
  """
  conn = sqlite3.connect("Users.db")
  cursor = conn.cursor()

  # Check if the username exists in the specified table
  cursor.execute(f"SELECT * FROM {table_name} WHERE username=?", (username,))
  result = cursor.fetchone()

  conn.close()

  # If result is not None, the username exists
  if result:
    return True
  else:
    return False


def validate_privilege(username, password, database_name, table_name):
    conn = sqlite3.connect(f'{database_name}.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table_name} WHERE Username=?", (username,))
    user_record = c.fetchone()

    if user_record:
        if password == user_record[2]:  # Assuming Password is at index 2
            conn.close()
            return user_record[4]  # Return privilege level (assuming it's at index 3)
        else:
            conn.close()
            return None
    else:
        conn.close()
        return None
    

def update_info(database_name, table_name, User_ID, Field, NewValue):
  conn = sqlite3.connect(f'{database_name}.db')
  c = conn.cursor()
  if isinstance(NewValue, int):
    if Field.lower() == "privileges":
      c.execute(f"""
          UPDATE {table_name}
          SET {Field} = {NewValue}
          WHERE User_ID = {User_ID}
    """)
      messagebox.showinfo("Success", "User information successfully changed")
  

  elif isinstance(NewValue, str):
    if Field.lower() == "username" or "password":
      c.execute(f"""
          UPDATE {table_name}
          SET {Field} = '{NewValue}'
          WHERE User_ID = {User_ID}
    """)
      messagebox.showinfo("Success", "User information successfully changed")
  else:
     messagebox.showerror("Failed", "Error updating information.")
  
  conn.commit()

  conn.close()
