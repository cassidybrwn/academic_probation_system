import mysql.connector
from pyswip import Prolog

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123$',  # Replace with your MySQL root password
    'database': 'UniversityDB'
}

# Initialize Prolog Engine
prolog = Prolog()
prolog.consult("gpa_calculations.pl")  # Ensure the Prolog file is in the same directory


def connect_db():
    """Establish connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def get_student_data(student_id, year):
    """Fetch student data and module grades from the database."""
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch student details
        cursor.execute("SELECT * FROM StudentMaster WHERE StudentId = %s", (student_id,))
        student = cursor.fetchone()

        # Fetch module grades for the student
        cursor.execute("""
            SELECT m.ModuleName, d.Year, d.Semester, m.Credits, d.GradePoints
            FROM ModuleDetails d
            JOIN ModuleMaster m ON d.ModuleID = m.ModuleID
            WHERE d.StudentId = %s AND d.Year = %s
        """, (student_id, year))
        modules = cursor.fetchall()

        return student, modules
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def calculate_gpa_with_prolog(modules):
    """Calculate GPA and cumulative GPA using Prolog."""
    # Separate modules by semester
    sem1_modules = [m for m in modules if m['Semester'] == '1']
    sem2_modules = [m for m in modules if m['Semester'] == '2']

    # Helper function to calculate GPA
    def calculate_semester_gpa(modules):
        total_grade_points = sum(m['Credits'] * m['GradePoints'] for m in modules)  # Use dictionary keys
        total_credits = sum(m['Credits'] for m in modules)  # Use dictionary keys

        if total_credits == 0:
            return 0.0

        query = list(prolog.query(f"calculate_gpa({total_grade_points}, {total_credits}, GPA)"))
        return query[0]['GPA'] if query else 0.0

    # Calculate semester GPAs
    gpa_sem1 = calculate_semester_gpa(sem1_modules)
    gpa_sem2 = calculate_semester_gpa(sem2_modules)

    # Calculate cumulative GPA
    total_grade_points = sum(m['Credits'] * m['GradePoints'] for m in modules)  # Use dictionary keys
    total_credits = sum(m['Credits'] for m in modules)  # Use dictionary keys


    # edit calculations *********
    cumulative_query = list(prolog.query(
        f"calculate_cumulative_gpa({gpa_sem1}, {gpa_sem2}, CumulativeGPA)"
    ))
    cumulative_gpa = cumulative_query[0]['CumulativeGPA'] if cumulative_query else gpa_sem1

    return gpa_sem1, gpa_sem2, cumulative_gpa



def generate_report(student_id, year):
    """Generate GPA report for a given student and year."""
    student, modules = get_student_data(student_id, year)
    if not student or not modules:
        print("No data found for the given student ID and year.")
        return

    gpa_sem1, gpa_sem2, cumulative_gpa = calculate_gpa_with_prolog(modules)

    # Check academic probation status
    probation_query = list(prolog.query(f"check_academic_probation({cumulative_gpa}, Status)"))
    status = probation_query[0]['Status'] if probation_query else "Unknown"

    # Print Report
    print("\n--- University of Technology ---")
    print("Academic Probation Alert GPA Report")
    print(f"Year: {year}")
    print(f"Student ID: {student['StudentId']}")
    print(f"Name: {student['StudentName']}")
    print(f"School: {student['School']}")
    print(f"Programme: {student['Programme']}")
    print(f"GPA Semester 1: {gpa_sem1:.2f}")
    print(f"GPA Semester 2: {gpa_sem2:.2f}")
    print(f"Cumulative GPA: {cumulative_gpa:.2f}")
    print(f"Status: {status}")


def main():
    """Main program flow."""
    print("Welcome to the GPA Monitoring System")
    print("1. Generate Student Report")
    print("2. Update Default GPA")
    choice = input("Enter your choice: ")

    if choice == "1":
        student_id = int(input("Enter Student ID: "))
        year = int(input("Enter Year: "))
        generate_report(student_id, year)
    elif choice == "2":
        new_gpa = float(input("Enter new default GPA: "))
        prolog.query(f"update_default_gpa({new_gpa})")
        print("Default GPA updated successfully!")
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
