import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # type: ignore # Importing Pillow for image handling
import traceback
import re
from datetime import datetime
import sys
import logging
import mysql.connector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Print to console
        logging.FileHandler('academic_system.log')  # Also log to file
    ]
)

# Define StudentDashboard 
class StudentDashboard:
    def __init__(self, parent_window, student_id):
        try:
           logging.info(f"Initializing StudentDashboard for student ID: {student_id}")
            
            self.parent = parent_window
            self.student_id = student_id
            self.dashboard_window = tk.Toplevel(parent_window)
            self.dashboard_window.title(f"Student Dashboard - ID: {student_id}")
            self.dashboard_window.geometry('1000x700')
            self.dashboard_window.configure(bg='#b1cee6')
            
            # Database connection method
            self.connect_to_database()
            
            # Main container
            main_container = tk.Frame(self.dashboard_window, bg='#8FBFDA')
            main_container.pack(expand=True, fill='both')
            
            # Sidebar
            sidebar = tk.Frame(main_container, width=200, bg='#2C6485')
            sidebar.pack(side='left', fill='y')
            
            # University Header
            tk.Label(
                main_container,
                text="University of Technology",
                font=("Arial", 24, "bold"),
                bg='#8FBFDA',
                fg='white'
            ).pack(pady=(20, 10))
            
            # Academic Probation Alert
            tk.Label(
                main_container,
                text="Academic Probation Alert GPA Report",
                font=("Arial", 16, "bold"),
                bg='#8FBFDA',
                fg='#B83556'
            ).pack(pady=(0, 20))
            
            # Content Frame
            content_frame = tk.Frame(main_container, bg='#8FBFDA')
            content_frame.pack(side='right', expand=True, fill='both', padx=20, pady=20)
            
            # Get student information
            self.student_info = self.get_student_info()
            
            # Display student name and ID
            tk.Label(
                main_container,
                text=f"Student: {self.student_info['first_name']} {self.student_info['last_name']} (ID: {student_id})",
                font=("Arial", 16, "bold"),
                bg='#8FBFDA',
                fg='white'
            ).pack(pady=(0, 20))
            
            # Sidebar Buttons
            btn_info = tk.Button(
                sidebar, 
                text="View Information", 
                command=self.show_gpa_table,
                bg='#2C6485', 
                fg='white', 
                font=("Arial", 12)
            )
            btn_info.pack(side='top', padx=10, pady=10, fill='x')
            
            btn_logout = tk.Button(
                sidebar, 
                text="Logout", 
                command=self.logout,
                bg="#B83556", 
                fg="white", 
                font=("Arial", 12)
            )
            btn_logout.pack(side='bottom', padx=10, pady=10, fill='x')
            
            # GPA Table Frame
            self.table_frame = tk.Frame(content_frame, bg='#b1cee6')
            
            # Create Treeview for GPA
            columns = ('name', 'id', 'semester1', 'semester2', 'cumulative')
            self.gpa_tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
            
            # Define column headings
            self.gpa_tree.heading('name', text='Student Name')
            self.gpa_tree.heading('id', text='Student ID')
            self.gpa_tree.heading('semester1', text='GPA Semester 1')
            self.gpa_tree.heading('semester2', text='GPA Semester 2')
            self.gpa_tree.heading('cumulative', text='Cumulative GPA')
            
            # Define column widths
            for col in columns:
                self.gpa_tree.column(col, width=120, anchor='center')
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.gpa_tree.yview)
            self.gpa_tree.configure(yscrollcommand=scrollbar.set)
            
            # Initially hide the table
            self.table_frame.pack_forget()
            
            logging.info("StudentDashboard initialized successfully")
            
        except Exception as e:
            logging.error(f"Error in StudentDashboard initialization: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to initialize Student Dashboard: {str(e)}")
            raise

    def connect_to_database(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",  
                user="",  
                password="'Password123$'",  
                database="UniversityDB"
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            logging.error(f"Database connection error: {e}")
            messagebox.showerror("Database Error", "Failed to connect to the database")
            raise

    def get_student_info(self):
        """Retrieve student information from database"""
        try:
            query = """
            SELECT StudentName, School, Programme 
            FROM StudentMaster 
            WHERE StudentId = %s
            """
            self.cursor.execute(query, (self.student_id,))
            student = self.cursor.fetchone()
            
            if student:
                # Split name into first and last name
                name_parts = student['StudentName'].split()
                return {
                    'first_name': name_parts[0],
                    'last_name': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                    'school': student['School'],
                    'programme': student['Programme']
                }
            else:
                return {
                    'first_name': 'Unknown',
                    'last_name': 'Student',
                    'school': 'N/A',
                    'programme': 'N/A'
                }
        except mysql.connector.Error as e:
            logging.error(f"Error fetching student info: {e}")
            return {
                'first_name': 'Error',
                'last_name': 'Retrieving',
                'school': 'N/A',
                'programme': 'N/A'
            }

    def show_gpa_table(self):
        try:
            logging.info("Showing GPA table")
            
            # Clear existing items
            for item in self.gpa_tree.get_children():
                self.gpa_tree.delete(item)
            
            # Fetch GPA data
            query = """
            SELECT 
                sm.StudentName,
                sm.StudentId,
                ROUND(AVG(CASE WHEN md.Semester = '1' THEN md.GradePoints END), 2) as Semester1GPA,
                ROUND(AVG(CASE WHEN md.Semester = '2' THEN md.GradePoints END), 2) as Semester2GPA,
                ROUND(AVG(md.GradePoints), 2) as CumulativeGPA
            FROM 
                StudentMaster sm
            JOIN 
                ModuleDetails md ON sm.StudentId = md.StudentId
            WHERE 
                sm.StudentId = %s
            GROUP BY 
                sm.StudentId, sm.StudentName
            """
            
            self.cursor.execute(query, (self.student_id,))
            gpa_data = self.cursor.fetchall()
            
            # Insert data
            for record in gpa_data:
                self.gpa_tree.insert('', 'end', values=(
                    record['StudentName'], 
                    record['StudentId'], 
                    record['Semester1GPA'] or 0.0, 
                    record['Semester2GPA'] or 0.0, 
                    record['CumulativeGPA']
                ))
            
            # Pack the table elements if not already packed
            if not self.table_frame.winfo_ismapped():
                self.table_frame.pack(fill='both', expand=True)
                self.gpa_tree.pack(side='left', fill='both', expand=True)
                scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.gpa_tree.yview)
                scrollbar.pack(side='right', fill='y')
                self.gpa_tree.configure(yscrollcommand=scrollbar.set)
            
        except mysql.connector.Error as e:
            logging.error(f"Error showing GPA table: {e}")
            messagebox.showerror("Error", f"Failed to retrieve GPA data: {e}")

    def logout(self):
        try:
            logging.info("Logout initiated")
            if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                logging.info("User confirmed logout")
                # Close database connection
                if hasattr(self, 'connection'):
                    self.cursor.close()
                    self.connection.close()
                
                self.dashboard_window.destroy()
                self.parent.deiconify()
        except Exception as e:
            logging.error(f"Error during logout: {str(e)}")
            logging.error(traceback.format_exc())


class StaffDashboard:
    def __init__(self, parent_window):
        try:
            self.parent = parent_window
            self.dashboard_window = tk.Toplevel(parent_window)
            self.dashboard_window.title("Staff Dashboard")
            self.dashboard_window.geometry('600x500')
            self.dashboard_window.configure(bg='#567C8D')
            
            
            self.logo_image = Image.open("C:/Users/cassy/Downloads/project/logo.png")
            self.logo_image = self.logo_image.resize((200, 210), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            
            # Logo label
            self.logo_label = tk.Label(self.dashboard_window, image=self.logo_photo, bg='#567C8D')
            self.logo_label.pack(pady=10)
            
            # Create main frame
            main_frame = tk.Frame(self.dashboard_window, bg='#567C8D')
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Header
            tk.Label(
                main_frame,
                text="Staff Dashboard - Student Record Management",
                font=("Arial", 20, "bold"),
                bg='#567C8D',
                fg='white'
            ).pack(pady=20)
            
            # Record entry form
            form_frame = tk.Frame(main_frame, bg='#567C8D')
            form_frame.pack(pady=20)
            
            # Student ID
            tk.Label(
                form_frame,
                text="Student ID:",
                bg='#567C8D',
                fg='white',
                font=("Arial", 12)
            ).grid(row=0, column=0, padx=10, pady=10)
            
            self.student_id_var = tk.StringVar()
            self.student_id_entry = ttk.Entry(
                form_frame,
                textvariable=self.student_id_var,
                font=("Arial", 12)
            )
            self.student_id_entry.grid(row=0, column=1, padx=10, pady=10)
            
            # Academic Year
            tk.Label(
                form_frame,
                text="Academic Year:",
                bg='#567C8D',
                fg='white',
                font=("Arial", 12)
            ).grid(row=1, column=0, padx=10, pady=10)
            
            self.year_var = tk.StringVar(value="2024")
            self.year_entry = ttk.Entry(
                form_frame,
                textvariable=self.year_var,
                font=("Arial", 12)
            )
            self.year_entry.grid(row=1, column=1, padx=10, pady=10)
            
            # GPA (optional)
            tk.Label(
                form_frame,
                text="GPA (optional):",
                bg='#567C8D',
                fg='white',
                font=("Arial", 12)
            ).grid(row=2, column=0, padx=10, pady=10)
            
            self.gpa_var = tk.StringVar()
            self.gpa_entry = ttk.Entry(
                form_frame,
                textvariable=self.gpa_var,
                font=("Arial", 12)
            )
            self.gpa_entry.grid(row=2, column=1, padx=10, pady=10)
          
            tk.Button(
                form_frame,
                text="Save Record",
                command=self.save_record,
                bg="#22303F",
                fg="white",
                font=("Arial", 12)
            ).grid(row=3, column=0, columnspan=2, pady=20)
            
            # Logout button
            tk.Button(
                main_frame,
                text="Logout",
                command=self.logout,
                bg="#B83556",
                fg="white",
                font=("Arial", 12)
            ).pack(side='bottom', pady=20)
            
        except Exception as e:
            print(f"Error in StaffDashboard initialization: {str(e)}")
            print(traceback.format_exc())
            raise
    
    def validate_student_id(self, student_id):
        if not student_id.isdigit() or len(student_id) != 4:
            return False
        return 1 <= int(student_id[0]) <= 7
    
    def save_record(self):
        try:
            student_id = self.student_id_var.get()
            year = self.year_var.get()
            gpa = self.gpa_var.get()
            
            if not self.validate_student_id(student_id):
                messagebox.showerror("Error", "Invalid student ID format")
                return
            
            if not year.isdigit():
                messagebox.showerror("Error", "Invalid year format")
                return
            
            if gpa and not re.match(r'^\d*\.?\d*$', gpa):
                messagebox.showerror("Error", "Invalid GPA format")
                return
            
            # save to a database
            messagebox.showinfo("Success", "Record saved successfully!")
            
            # Clear fields
            self.student_id_var.set("")
            self.year_var.set("2024")
            self.gpa_var.set("")
            
        except Exception as e:
            print(f"Error saving record: {str(e)}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to save record: {str(e)}")
    
    def logout(self):
        try:
            if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                self.dashboard_window.destroy()
                self.parent.deiconify()
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            print(traceback.format_exc())

class LoginWindow:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("Academic System Login")
            self.window.geometry('680x440')  # Doubled width to accommodate image and frame

            # Load and resize background image
            self.bg_image = Image.open("C:/Users/cassy/Downloads/project/book.png")  
            self.bg_image = self.bg_image.resize((400, 440), Image.LANCZOS)  
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)

            # Background label placed on the left side
            self.background_label = tk.Label(self.window, image=self.bg_photo)
            self.background_label.place(x=0, y=0, relwidth=0.3, relheight=1)

            # Create main frame with a transparent background, placed on the right side
            self.frame = tk.Frame(self.window, bg='#567C8D', bd=10)
            self.frame.place(relx=0.6, rely=0.5, anchor='center', relwidth=0.4)

            # Login widgets
            login_label = tk.Label(self.frame, text="Login", bg='#567C8D', fg="#FFFFFF", font=("Arial", 30))
            login_label.grid(row=1, column=3, columnspan=2, sticky="news", pady=40)

            self.role_var = tk.StringVar(value="student")
            role_frame = tk.Frame(self.frame, bg='#567C8D')
            tk.Radiobutton(role_frame, text="Student", variable=self.role_var, value="student",
                           font=(40), bg='#567C8D', fg="#FFFFFF", selectcolor='#84a9c9').pack(side=tk.LEFT, padx=10)
            tk.Radiobutton(role_frame, text="Staff", variable=self.role_var, value="staff",
                           font=(40), bg='#567C8D', fg="#FFFFFF", selectcolor='#84a9c9').pack(side=tk.LEFT, padx=10)
            role_frame.grid(row=2, column=2, columnspan=2, pady=20)

            id_label = tk.Label(self.frame, text="ID Number", bg='#567C8D', fg="#FFFFFF", font=("Arial", 16))
            id_label.grid(row=3, column=2)

            self.id_entry = tk.Entry(self.frame, font=("Arial", 16))
            self.id_entry.grid(row=3, column=4, pady=20)

            password_label = tk.Label(self.frame, text="Password", bg='#567C8D', fg="#FFFFFF", font=("Arial", 16))
            password_label.grid(row=4, column=2)

            self.password_entry = tk.Entry(self.frame, font=("Arial", 16), show="*")
            self.password_entry.grid(row=4, column=4, pady=20)

            login_button = tk.Button(self.frame, text="Login", bg="#567C8D", fg="#FFFFFF",
                                     font=("Arial", 16), command=self.login)
            login_button.grid(row=5, column=3, columnspan=2, pady=30)

        except Exception as e:
            print(f"Error initializing LoginWindow: {str(e)}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Error initializing LoginWindow: {str(e)}")

    def validate_id(self, id_number, role):
        if not id_number.isdigit() or len(id_number) != 4:
            return False
        first_digit = int(id_number[0])
        return (role == "student" and 1 <= first_digit <= 7) or (role == "staff" and first_digit == 8)
    def login(self):
        try:
            id_number = self.id_entry.get()
            password = self.password_entry.get()
            role = self.role_var.get()

            logging.info(f"Login attempt - Role: {role}, ID: {id_number}")

            if not self.validate_id(id_number, role):
                logging.warning(f"Invalid {role} ID format")
                messagebox.showerror("ERROR", f"Invalid {role} ID format")
                return

            valid_password = "password"
            if password == valid_password:
                logging.info(f"Login successful - Role: {role}, ID: {id_number}")
                messagebox.showinfo("Success", "Login successful!")
                
                # Hide the login window
                self.window.withdraw()
                
                # Open the appropriate dashboard based on role
                if role == "student":
                    logging.info(f"Opening Student Dashboard for ID: {id_number}")
                    StudentDashboard(self.window, id_number)
                elif role == "staff":
                    logging.info("Opening Staff Dashboard")
                    StaffDashboard(self.window)
            else:
                logging.warning("Invalid password")
                messagebox.showerror("ERROR", "Invalid password")

        except Exception as e:
            logging.error(f"Error in login process: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Error", f"Login process failed: {str(e)}")
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    try:
        logging.info("Starting Academic System Application")
        app = LoginWindow()
        app.run()
    except Exception as e:
        logging.critical(f"Critical error in main: {str(e)}")
        logging.critical(traceback.format_exc())
        messagebox.showerror("Critical Error", f"Application failed to start: {str(e)}")