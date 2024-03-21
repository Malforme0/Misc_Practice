import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

import Database_Manager


class Application(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.title("File_Management_Application")

    container = tk.Frame(self, height=400, width=600)
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}

    for F in (Welcome_Page, Login_Page, Register_Page, UserPage, AdminPage, DeleteUser, UpdateUser):
      frame = F(container, self)

      self.frames[F] = frame
      frame.grid(row=0, column=0, sticky="nsew")

      self.database_viewer = None

      self.show_frame(Welcome_Page)

  def show_frame(self, cont):
    frame = self.frames[cont]
    if frame:
      frame.tkraise()

def open_database_viewer(controller):
  if not controller.database_viewer:
    controller.database_viewer = DatabaseViewer(controller)
  else:
    controller.database_viewer.lift()


def create_new_file(file_path):
  try:
    with open(file_path, 'w'):
      pass
    print(f"File '{file_path}' created successfully.")
  except Exception as e:
    print(f"Error creating file '{file_path}': {e}")


def delete_file(file_path):
  try:
    os.remove(file_path)
    print(f"File '{file_path}' deleted successfully.")
  except Exception as e:
    print(f"Error deleting file '{file_path}': {e}")

def show_all_files(directory):
  try:
    files = os.listdir(directory)
    print("Files in directory:")
    for file in files:
      print(file)
  except Exception as e:
    print(f"Error showing files in directory '{directory}': {e}")


def organize_files(source_directory, destination_directory):
  try:
    files = os.listdir(source_directory)

    for file in files:
      source_file_path = os.path.join(source_directory, file)
      destination_file_path = os.path.join(destination_directory, file)
      os.rename(source_file_path, destination_file_path)

    print(f"All files in '{source_directory}' organized successfully to '{destination_directory}'.")
  except Exception as e:
    print(f"Error organizing files: {e}")

def classify_files(folder_path, output_file):
  extensions = {}
  for root, dirs, files in os.walk(folder_path):
    for file in files:

      _, ext = os.path.splitext(file)
      ext = ext.lower()

      extensions[ext] = extensions.get(ext, 0) + 1


  with open(output_file, 'w') as f:
    f.write("Extension,Count\n")
    for ext, count in extensions.items():
      f.write(f"{ext},{count}\n")

class Welcome_Page(tk.Frame):
  def __init__(self, parent, controller):
    Database_Manager.Create_User_Data("Users.db")
    tk.Frame.__init__(self, parent)
    label = tk.Label(self, text="Welcome to the File Management Application")
    label.pack(padx=10, pady=10)

    Go_To_Login_Page = tk.Button(
      self,
      text="Login",
      command=lambda: controller.show_frame(Login_Page)
      )
    Go_To_Login_Page.pack(side="bottom", fill=tk.X)

    Go_To_Register_Page = tk.Button(
      self,
      text="Register",
      command=lambda: controller.show_frame(Register_Page)
      )
    Go_To_Register_Page.pack(side="bottom", fill=tk.X)




class Login_Page(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    self.Username_label = ttk.Label(
      self,
      text='Username:'
      )
    self.Username_label.pack(padx=10, pady=10)

    self.Username_entry = ttk.Entry(
      self
      )
    self.Username_entry.pack(padx=10, pady=10)

    self.Password_label = ttk.Label(
      self,
      text='Password:'
      )
    self.Password_label.pack(padx=10, pady=10)

    self.Password_entry = ttk.Entry(
      self,
      show='*'
      )
    self.Password_entry.pack(padx=10, pady=10)

    self.Login_Button = ttk.Button(
      self,
      text='Login',
      command=self.login
      )
    self.Login_Button.pack(padx=10, pady=10)

    Go_To_Welcome_Page = tk.Button(
      self,
      text="Back",
      command=lambda: controller.show_frame(Welcome_Page)
      )
    Go_To_Welcome_Page.pack(side="bottom", fill=tk.X)




  def login(self):
    username = self.Username_entry.get()
    password = self.Password_entry.get()
    privilege = Database_Manager.validate_privilege(username, password, 'Users', 'User_Data')

    if privilege is not None and privilege == 2:
      messagebox.showinfo("Login Successful", "Login Successful")
      self.controller.show_frame(AdminPage)
    elif privilege is not None and privilege == 0:
      messagebox.showinfo("Login Successful", "Login Successful")
      self.controller.show_frame(UserPage)
    else:
      messagebox.showerror("Invalid Login", "Incorrect Username or Password")

    self.Username_entry.delete(0, 9999999)
    self.Password_entry.delete(0, 9999999)


class Register_Page(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Username_label = ttk.Label(
      self,
      text='Username:'
      )
    self.Username_label.pack(padx=10, pady=10)

    self.Username_entry = ttk.Entry(
      self
      )
    self.Username_entry.pack(padx=10, pady=10)

    self.Password_label = ttk.Label(
      self,
      text='Password:'
      )
    self.Password_label.pack(padx=10, pady=10)

    self.Password_entry = ttk.Entry(
      self
      )
    self.Password_entry.pack(padx=10, pady=10)

    self.Register_Button = ttk.Button(
      self,
      text='Register',
      command=self.Register
      )
    self.Register_Button.pack(padx=10, pady=10)

    Go_To_Welcome_Page = tk.Button(
      self,
      text="Back",
      command=lambda: controller.show_frame(Welcome_Page)
      )
    Go_To_Welcome_Page.pack(side="bottom", fill=tk.X)

  def Register(self):
    username = self.Username_entry.get()
    password = self.Password_entry.get()
    total = 0
    for char in username:
      total += ord(char)

    user_id = total

    if not username or not password:
      messagebox.showerror("Error", "Please enter both username and password")
      return

    if Database_Manager.check_username_existence(username, 'User_Data'):
      messagebox.showerror("Error", "Username already exists. Please choose another one.")
      return

    Database_Manager.Add_User('Users.db', 'User_Data', user_id, username, password, 0)

    messagebox.showinfo("Success", "Registration successful. You can now login.")

    self.Username_entry.delete(0, 9999999)
    self.Password_entry.delete(0, 9999999)


class AdminPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Page_Label = ttk.Label(
      self,
      text="File Management(Administrator)"
    )
    self.Page_Label.pack()


    Display_Database = tk.Button(
    self,
    text="User Information",
    command=lambda: open_database_viewer(controller)
    )
    Display_Database.pack(pady=10)

    Go_To_Welcome_Page = tk.Button(
      self,
      text="Logout",
      command=lambda: controller.show_frame(Welcome_Page)
      )
    Go_To_Welcome_Page.pack(side="bottom", fill=tk.X)

    Go_To_DeleteUser = tk.Button(
      self,
      text= "Delete User",
      command= lambda: controller.show_frame(DeleteUser)
    )
    Go_To_DeleteUser.pack()

    Go_To_UpdateUser = tk.Button(
      self,
      text= "Update User",
      command= lambda: controller.show_frame(UpdateUser)
    )
    Go_To_UpdateUser.pack()

    Go_To_File_Page = tk.Button(
      self,
      text="File Management",
      command=lambda: controller.show_frame(FileManagementPage)
      )
    Go_To_File_Page.pack(side="bottom", fill=tk.X)


class UpdateUser(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Page_Label = ttk.Label(
      self,
      text="Update User"
    )
    self.Page_Label.pack()

    self.UserID_label = ttk.Label(
      self,
      text="Please enter the UserID of the user you whose information you wish to update"
    )
    self.UserID_label.pack()

    self.UserID_Entry = ttk.Entry(
      self,
    )
    self.UserID_Entry.pack()

    self.Field_label = ttk.Label(
      self,
      text= "Please enter which field of the user's information you wish to change"
    )
    self.Field_label.pack()

    self.Field_Entry = ttk.Entry(
      self
    )
    self.Field_Entry.pack()

    self.Value_Label = ttk.Label(
      self,
      text= "Please enter what you wish to update the data to"
    )
    self.Value_Label.pack()

    self.Value_Entry = ttk.Entry(
      self
    )
    self.Value_Entry.pack()

    self.Update_Button = ttk.Button(
      self,
      text= "Update",
      command= lambda: Database_Manager.update_info("Users", "User_Data", self.UserID_Entry.get(), self.Field_Entry.get(), self.Value_Entry.get())
    )
    self.Update_Button.pack()

    Go_To_AdminPage = tk.Button(
      self,
      text= "Back",
      command= lambda: controller.show_frame(AdminPage)
    )
    Go_To_AdminPage.pack(side="bottom", fill=tk.X)






class DeleteUser(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Page_Label = ttk.Label(
      self,
      text= "Delete User"
    )
    self.Page_Label.pack()

    self.UserID_label = ttk.Label(
      self,
      text='Please input the User ID of the user you wish to remove:'
      )
    self.UserID_label.pack(padx=10, pady=10)

    self.UserID_entry = ttk.Entry(
      self
      )
    self.UserID_entry.pack(padx=10, pady=10)

    self.Delete_Button = ttk.Button(
      self,
      text='Delete User',
      command= lambda: Database_Manager.Delete_User("Users.db", "User_Data", self.UserID_entry.get())
      )
    self.Delete_Button.pack(padx=10, pady=10)

    Go_To_AdminPage = tk.Button(
      self,
      text= "Back",
      command= lambda: controller.show_frame(AdminPage)
    )
    Go_To_AdminPage.pack(side="bottom", fill=tk.X)


class UserPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Page_Label = ttk.Label(
      self,
      text="User Page"
    )
    self.Page_Label.pack()

    Go_To_Welcome_Page = tk.Button(
      self,
      text="Logout",
      command=lambda: controller.show_frame(Welcome_Page)
      )
    Go_To_Welcome_Page.pack(side="bottom", fill=tk.X)


    Go_To_File_Page = tk.Button(
      self,
      text="File Management",
      command=lambda: controller.show_frame(FileManagementPage)
      )
    Go_To_File_Page.pack(side="bottom", fill=tk.X)



class FileManagementPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    self.Page_Label = ttk.Label(
      self,
      text = "File Management"
    )
    self.Page_Label.pack()




class DatabaseViewer(tk.Toplevel):
  def __init__(self, controller):
    super().__init__()
    self.title("Database Viewer")
    self.controller = controller

    self.geometry("800x400")

    # Create Treeview widget to display database table
    self.tree = ttk.Treeview(self)
    self.tree.pack(fill="both", expand=True)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
    scrollbar.pack(side="right", fill="y")
    self.tree.configure(yscrollcommand=scrollbar.set)

    # Populate Treeview initially
    self.populate_treeview()

    # Update Treeview periodically
    self.after(1000, self.update_treeview)  # Update every 5 seconds

  def populate_treeview(self):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(User_Data)")
    columns = [col[1] for col in cursor.fetchall()]

    self.tree["columns"] = columns
    self.tree.heading("#0", text="ID")
    for col in columns:
      self.tree.heading(col, text=col)
      self.tree.column(col, width=100)

    cursor.execute("SELECT * FROM User_Data")
    rows = cursor.fetchall()
    for row in rows:
      self.tree.insert("", "end", values=row)

    conn.close()

  def update_treeview(self):
    for item in self.tree.get_children():
      self.tree.delete(item)

    self.populate_treeview()

    self.after(1000, self.update_treeview)





if __name__ == "__main__":
  testObj = Application()
  testObj.mainloop()
