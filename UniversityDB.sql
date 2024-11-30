create database UniversityDB;
-- drop DATABASE UniversityDB;

use UniversityDB;

#creating Student Master table
create table StudentMaster (
StudentId int PRIMARY KEY auto_increment,
StudentName varchar(50) NOT NULL,
StudentEmail varchar(50) NOT NULL UNIQUE,
School varchar(50),
Programme varchar(50)
);

-- drop table StudentMaster;

#create Module Master table
create table ModuleMaster (
ModuleID int PRIMARY KEY auto_increment,
ModuleName varchar(50) not null,
Credits int NOT NULL CHECK (Credits > 0)	-- ensure that the Credits value must be greater than 0.
);
 
-- drop table ModuleMaster;

#create Module Details table
create table ModuleDetails (
ModuleID int,
Year INT,
Semester ENUM('1', '2') NOT NULL,
StudentId INT,
GradePoints DECIMAL(4, 2) NOT NULL CHECK (GradePoints >= 0),
FOREIGN KEY (ModuleID) REFERENCES ModuleMaster(ModuleID),
FOREIGN KEY (StudentId) REFERENCES StudentMaster(StudentId)
);

-- drop table ModuleDetails;

-- Insert sample students
INSERT INTO StudentMaster (StudentName, StudentEmail, School, Programme) VALUES
('Alice Johnson', 'alice.johnson@gmail.com', 'Engineering', 'Computer Science'),
('Bob Smith', 'bob.smith@yahoo.com', 'Science', 'Biology');

-- Insert 3 new students with different programmes
INSERT INTO StudentMaster (StudentName, StudentEmail, School, Programme) VALUES
('David Black', 'david.black@gmail.com', 'Engineering', 'Electrical Engineering'),
('Sophia Williams', 'sophia.williams@yahoo.com', 'Humanities', 'Philosophy'),
('Tyrone Adams', 'tyrone.adams@gmail.com', 'Science', 'Chemistry');

-- Insert sample modules
INSERT INTO ModuleMaster (ModuleName, Credits) VALUES
('Calculus I', 4),
('Physics I', 3),
('Introduction to Programming', 4),
('Data Structures', 4);

-- Insert sample module details
INSERT INTO ModuleDetails (ModuleID, Year, Semester, StudentID, GradePoints) VALUES
(1, 2024, '1', 1, 3.5),  -- Alice, Calculus I, 2024, Semester 1 (passed)
(2, 2024, '1', 1, 3.0),  -- Alice, Physics I, 2024, Semester 1 (passed)
(3, 2024, '1', 1, 1.0),  -- Alice, Intro to Programming, 2024, Semester 1 (failed module)
(4, 2024, '1', 2, 4.0),  -- Bob, Data Structures, 2024, Semester 2
(1, 2024, '2', 2, 2.5),  -- Bob, Calculus I, 2024, Semester 2 (redo)
(1, 2024, '1', 3, 2.5),  -- David, Calculus I, Semester 1 (passed)
(2, 2024, '1', 3, 2.1),  -- David, Physics I, Semester 1 (passed)
(3, 2024, '1', 3, 1.5),  -- David, Intro to Programming, Semester 1 (failed)
(3, 2024, '2', 3, 3.0),  -- David, Intro to Programming, Semester 2 (passed reattempt)
(1, 2024, '1', 4, 3.5),  -- Sophia, Calculus I, Semester 1 (passed)
(2, 2024, '1', 4, 2.5),  -- Sophia, Physics I, Semester 1 (passed)
(3, 2024, '1', 4, 1.9),  -- Sophia, Intro to Programming, Semester 1 (failed)
(3, 2024, '2', 4, 3.2),  -- Sophia, Intro to Programming, Semester 2 (passed reattempt)
(1, 2024, '1', 4, 1.3),  -- Tyrone, Calculus I, Semester 1 (failed)
(2, 2024, '1', 4, 2.2),  -- Tyrone, Physics I, Semester 1 (passed)
(4, 2024, '1', 4, 3.3),  -- Tyrone, Data Structures, Semester 1 (passed)
(1, 2024, '2', 4, 3.4);  -- Tyrone, Calculus I, Semester 2 (passed reattempt)


-- Select statements
SELECT * FROM StudentMaster;
SELECT * FROM ModuleMaster;		
SELECT * FROM ModuleDetails;	



delete from universitydb.StudentMaster;
truncate universityDB.StudentMaster;
