import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import re
from datetime import datetime

class LoginWindow:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("Academic System Login")
            self.window.geometry('340x440')
            self.window.configure(bg='#b1cee6')
            
            # Create main frame
            self.frame = tk.Frame(self.window, bg='#b1cee6')
            
            # Login widgets
            login_label = tk.Label(
                self.frame,
                text="Login",
                bg='#b1cee6',
                fg="#FFFFFF",
                font=("Arial", 30)
            )
            
            # Role selection
            self.role_var = tk.StringVar(value="student")
            
            role_frame = tk.Frame(self.frame, bg='#b1cee6')
            tk.Radiobutton(
                role_frame,
                text="Student",
                variable=self.role_var,
                value="student",
                font= (40),  
                bg='#b1cee6',
                fg="#FFFFFF",
                selectcolor='#84a9c9'
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Radiobutton(
                role_frame,
                text="Staff",
                variable=self.role_var,
                value="staff",
                font= (40),  
                bg='#b1cee6',
                fg="#FFFFFF",
                selectcolor='#84a9c9'
            ).pack(side=tk.LEFT, padx=10)
            
            id_label = tk.Label(
                self.frame,
                text="ID Number",
                bg='#b1cee6',
                fg="#FFFFFF",
                font=("Arial", 16)
            )
            
            self.id_entry = tk.Entry(
                self.frame,
                font=("Arial", 16)
            )
            
            password_label = tk.Label(
                self.frame,
                text="Password",
                bg='#b1cee6',
                fg="#FFFFFF",
                font=("Arial", 16)
            )
            
            self.password_entry = tk.Entry(
                self.frame,
                font=("Arial", 16),
                show="*"
            )
            
            login_button = tk.Button(
                self.frame,
                text="Login",
                bg="#9FE2BF",
                fg="#FFFFFF",
                font=("Arial", 16),
                command=self.login
            )
            
            # Widget placement
            login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
            role_frame.grid(row=1, column=0, columnspan=2, pady=20)
            id_label.grid(row=2, column=0)
            self.id_entry.grid(row=2, column=1, pady=20)
            password_label.grid(row=3, column=0)
            self.password_entry.grid(row=3, column=1, pady=20)
            login_button.grid(row=4, column=0, columnspan=2, pady=30)
            
            self.frame.pack()
            
        except Exception as e:
            print(f"Error initializing LoginWindow: {str(e)}")
            print(traceback.format_exc())
    
    def validate_id(self, id_number, role):
        if not id_number.isdigit() or len(id_number) != 4:
            return False
        
        first_digit = int(id_number[0])
        if role == "student":
            return 1 <= first_digit <= 7
        else:  # staff
            return first_digit == 8
    
    def login(self):
        try:
            id_number = self.id_entry.get()
            password = self.password_entry.get()
            role = self.role_var.get()
            
            # Validate ID format
            if not self.validate_id(id_number, role):
                messagebox.showerror("ERROR", f"Invalid {role} ID format")
                return
            
            # In a real application, you would check against a database
            # For demo purposes, we'll use a simple password
            valid_password = "password"
            
            if password == valid_password:
                print("Login successful, attempting to open dashboard...")
                self.window.withdraw()  # Hide login window
                try:
                    if role == "student":
                        dashboard = StudentDashboard(self.window, id_number)
                    else:
                        dashboard = StaffDashboard(self.window)
                    print("Dashboard opened successfully")
                except Exception as e:
                    print(f"Error opening dashboard: {str(e)}")
                    print(traceback.format_exc())
                    self.window.deiconify()  # Show login window again if dashboard fails
                    messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}")
            else:
                messagebox.showerror("ERROR", "Invalid password")
        except Exception as e:
            print(f"Error in login process: {str(e)}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Login error: {str(e)}")

    def run(self):
        try:
            print("Starting application...")
            self.window.mainloop()
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            print(traceback.format_exc())
class StudentDashboard:
    def __init__(self, parent_window, student_id):
        try:
            self.parent = parent_window
            self.student_id = student_id
            self.dashboard_window = tk.Toplevel(parent_window)
            self.dashboard_window.title(f"Student Dashboard - ID: {student_id}")
            self.dashboard_window.geometry('800x600')
            self.dashboard_window.configure(bg='#b1cee6')
            
            # Create main frame
            main_frame = tk.Frame(self.dashboard_window, bg='#b1cee6')
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Header with student info
            self.header_frame = tk.Frame(main_frame, bg='#b1cee6')
            self.header_frame.pack(fill='x', pady=(0, 20))
            
            # Add student info (this would typically come from a database)
            self.student_info = {
                'id': student_id,
                'first_name': 'John',  # Demo data
                'last_name': 'Doe',    # Demo data
            }
            
            # Display student name and ID
            tk.Label(
                self.header_frame,
                text=f"Student: {self.student_info['first_name']} {self.student_info['last_name']} (ID: {student_id})",
                font=("Arial", 20, "bold"),
                bg='#b1cee6',
                fg='white'
            ).pack(side='left', pady=10)
            
            # Year selection frame
            year_frame = tk.Frame(main_frame, bg='#b1cee6')
            year_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                year_frame,
                text="Select Academic Year:",
                bg='#b1cee6',
                fg='white',
                font=("Arial", 12)
            ).pack(side='left', padx=(0, 10))
            
            # Create year dropdown with last 5 years
            current_year = datetime.now().year
            years = [str(year) for year in range(current_year-4, current_year+1)]
            self.year_var = tk.StringVar(value=str(current_year))
            year_dropdown = ttk.Combobox(
                year_frame,
                textvariable=self.year_var,
                values=years,
                state='readonly',
                width=10
            )
            year_dropdown.pack(side='left')
            year_dropdown.bind('<<ComboboxSelected>>', self.update_grades)
            
            # Create table frame
            table_frame = tk.Frame(main_frame, bg='#b1cee6')
            table_frame.pack(fill='both', expand=True)
            
            # Create Treeview for grades
            columns = ('subject', 'midterm', 'final', 'grade')
            self.grade_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
            
            # Define column headings
            self.grade_tree.heading('subject', text='Subject')
            self.grade_tree.heading('midterm', text='Midterm')
            self.grade_tree.heading('final', text='Final')
            self.grade_tree.heading('grade', text='Final Grade')
            
            # Define column widths
            for col in columns:
                self.grade_tree.column(col, width=100, anchor='center')
            self.grade_tree.column('subject', width=200, anchor='w')
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.grade_tree.yview)
            self.grade_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack the table and scrollbar
            self.grade_tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Add summary frame
            summary_frame = tk.Frame(main_frame, bg='#b1cee6')
            summary_frame.pack(fill='x', pady=20)
            
            self.gpa_label = tk.Label(
                summary_frame,
                text="GPA: 0.00",
                bg='#b1cee6',
                fg='white',
                font=("Arial", 12, "bold")
            )
            self.gpa_label.pack(side='left', padx=20)
            
            # Logout button
            tk.Button(
                main_frame,
                text="Logout",
                command=self.logout,
                bg="#FF6B6B",
                fg="white",
                font=("Arial", 12)
            ).pack(side='bottom', pady=20)
            
            # Load initial grades
            self.update_grades(None)
            
        except Exception as e:
            print(f"Error in StudentDashboard initialization: {str(e)}")
            print(traceback.format_exc())
            raise

    def update_grades(self, event):
        try:
            # Clear existing items
            for item in self.grade_tree.get_children():
                self.grade_tree.delete(item)
            
            # In a real application, you would fetch this data from a database
            # This is demo data
            grades_data = {
                '2024': [
                    ('Mathematics', 85, 88, 87),
                    ('Physics', 78, 82, 80),
                    ('Chemistry', 90, 92, 91),
                    ('English', 88, 85, 86),
                    ('Computer Science', 95, 94, 94)
                ],
                '2023': [
                    ('Mathematics', 82, 85, 84),
                    ('Physics', 75, 80, 78),
                    ('Chemistry', 88, 90, 89),
                    ('English', 85, 83, 84),
                    ('Computer Science', 92, 90, 91)
                ]
            }
            
            selected_year = self.year_var.get()
            year_grades = grades_data.get(selected_year, [])
            
            # Calculate GPA
            total_grade = 0
            for subject in year_grades:
                self.grade_tree.insert('', 'end', values=subject)
                total_grade += subject[3]
            
            if year_grades:
                gpa = total_grade / len(year_grades) / 20  # Convert to 4.0 scale
                self.gpa_label.config(text=f"GPA: {gpa:.2f}")
            else:
                self.gpa_label.config(text="GPA: N/A")
                self.grade_tree.insert('', 'end', values=('No grades available for selected year', '', '', ''))
                
        except Exception as e:
            print(f"Error updating grades: {str(e)}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to update grades: {str(e)}")

    def logout(self):
        try:
            if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                self.dashboard_window.destroy()
                self.parent.deiconify()
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            print(traceback.format_exc())
class StaffDashboard:
    def __init__(self, parent_window):
        try:
            self.parent = parent_window
            self.dashboard_window = tk.Toplevel(parent_window)
            self.dashboard_window.title("Staff Dashboard")
            self.dashboard_window.geometry('600x500')
            self.dashboard_window.configure(bg='#b1cee6')
            
            # Create main frame
            main_frame = tk.Frame(self.dashboard_window, bg='#b1cee6')
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Header
            tk.Label(
                main_frame,
                text="Staff Dashboard - Student Record Management",
                font=("Arial", 20, "bold"),
                bg='#b1cee6',
                fg='white'
            ).pack(pady=20)
            
            # Record entry form
            form_frame = tk.Frame(main_frame, bg='#b1cee6')
            form_frame.pack(pady=20)
            
            # Student ID
            tk.Label(
                form_frame,
                text="Student ID:",
                bg='#b1cee6',
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
                bg='#b1cee6',
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
                bg='#b1cee6',
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
            
            # Save button
            tk.Button(
                form_frame,
                text="Save Record",
                command=self.save_record,
                bg="#9FE2BF",
                fg="white",
                font=("Arial", 12)
            ).grid(row=3, column=0, columnspan=2, pady=20)
            
            # Logout button
            tk.Button(
                main_frame,
                text="Logout",
                command=self.logout,
                bg="#FF6B6B",
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
            
            # Here you would typically save to a database
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

if __name__ == "__main__":
    try:
        print("Initializing application...")
        app = LoginWindow()
        app.run()
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        print(traceback.format_exc())