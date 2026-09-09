import sqlite3

conn = sqlite3.connect("database/sample.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS salary_audit")
cursor.execute("DROP TABLE IF EXISTS employee_projects")
cursor.execute("DROP TABLE IF EXISTS projects")
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS departments")

cursor.execute("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER,
    salary INTEGER CHECK(salary > 0),
    joining_date TEXT,
    email TEXT UNIQUE,
    manager_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
)
""")

cursor.execute("""
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    department_id INTEGER,
    budget INTEGER,
    start_date TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")

cursor.execute("""
CREATE TABLE employee_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    project_id INTEGER,
    role TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
""")

cursor.execute("""
CREATE TABLE salary_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    old_salary INTEGER,
    new_salary INTEGER,
    changed_at TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
""")

cursor.execute("""
INSERT INTO departments (department_name, location) VALUES
('IT', 'Bangalore'),
('HR', 'Delhi'),
('Sales', 'Mumbai'),
('Finance', 'Pune')
""")

cursor.execute("""
INSERT INTO employees (name, department_id, salary, joining_date, email, manager_id) VALUES
('Amit Sharma', 1, 65000, '2021-03-15', 'amit@company.com', NULL),
('Neha Verma', 2, 42000, '2022-06-01', 'neha@company.com', NULL),
('Ravi Kumar', 3, 61000, '2020-11-20', 'ravi@company.com', NULL),
('Priya Singh', 1, 48000, '2023-01-10', 'priya@company.com', 1),
('Suresh Rao', 1, 55000, '2022-08-05', 'suresh@company.com', 1),
('Anjali Gupta', 2, 39000, '2023-04-18', NULL, 2),
('Vikram Joshi', 3, 58000, '2021-09-30', 'vikram@company.com', 3),
('Sneha Patel', 4, 47000, '2022-12-01', 'sneha@company.com', NULL),
('Karan Mehta', 1, 72000, '2019-07-14', 'karan@company.com', 1),
('Divya Nair', 3, 63000, '2021-05-25', 'divya@company.com', 3),
('Arjun Das', 4, 51000, '2023-02-20', 'arjun@company.com', 8),
('Pooja Reddy', 2, 44000, '2022-10-11', 'pooja@company.com', 2),
('Rohit Malhotra', 1, 49000, '2023-06-08', NULL, 1),
('Kavita Iyer', 4, 53000, '2021-12-19', 'kavita@company.com', 8),
('Manish Yadav', 3, 60000, '2020-04-02', 'manish@company.com', 3)
""")

cursor.execute("""
INSERT INTO projects (project_name, department_id, budget, start_date) VALUES
('Website Revamp', 1, 500000, '2023-01-05'),
('Employee Onboarding System', 2, 200000, '2022-11-15'),
('Q3 Sales Campaign', 3, 350000, '2023-07-01'),
('Budget Automation Tool', 4, 150000, '2023-03-20'),
('Mobile App Development', 1, 800000, '2022-09-10'),
('Recruitment Drive', 2, 100000, '2023-05-01')
""")

cursor.execute("""
INSERT INTO employee_projects (employee_id, project_id, role) VALUES
(1, 1, 'Lead Developer'),
(4, 1, 'Frontend Developer'),
(5, 1, 'Backend Developer'),
(9, 5, 'Project Manager'),
(1, 5, 'Technical Advisor'),
(13, 5, 'Developer'),
(2, 2, 'HR Lead'),
(6, 2, 'Coordinator'),
(12, 6, 'Recruiter'),
(3, 3, 'Sales Lead'),
(7, 3, 'Sales Executive'),
(10, 3, 'Sales Executive'),
(8, 4, 'Finance Analyst'),
(14, 4, 'Finance Analyst'),
(11, 4, 'Junior Analyst')
""")


cursor.execute("""
CREATE TRIGGER IF NOT EXISTS salary_change_trigger
AFTER UPDATE OF salary ON employees
BEGIN
    INSERT INTO salary_audit (employee_id, old_salary, new_salary, changed_at)
    VALUES (OLD.id, OLD.salary, NEW.salary, datetime('now'));
END;
""")

cursor.execute("""
CREATE VIEW IF NOT EXISTS employee_details AS
SELECT e.id, e.name, e.salary, d.department_name, d.location
FROM employees e
JOIN departments d ON e.department_id = d.id
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_employee_department ON employees(department_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_employee_salary ON employees(salary)
""")

conn.commit()
conn.close()

print("Database created successfully with all tables, data, trigger, view, and indexes!")