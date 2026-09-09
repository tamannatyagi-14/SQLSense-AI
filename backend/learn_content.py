LEARN_TOPICS = {
    "SELECT & WHERE": {
        "explanation": "SELECT tells the database which columns you want to see. WHERE filters rows based on a condition — only rows that match are returned.",
        "example": "SELECT name, salary FROM employees WHERE salary > 50000"
    },
    "Filtering: LIKE, IN, BETWEEN": {
        "explanation": "LIKE matches text patterns (% means 'any characters'). IN checks if a value matches any in a list. BETWEEN checks a range (inclusive on both ends).",
        "example": "SELECT * FROM employees WHERE name LIKE 'A%' AND department_id IN (1, 2) AND salary BETWEEN 40000 AND 60000"
    },
    "NULL Handling": {
        "explanation": "NULL means 'no value' — it's not the same as 0 or an empty string. You can't use = to check for it; use IS NULL or IS NOT NULL instead.",
        "example": "SELECT name, email FROM employees WHERE email IS NULL"
    },
    "ORDER BY & LIMIT": {
        "explanation": "ORDER BY sorts your results (ascending by default, or DESC for descending). LIMIT restricts how many rows come back.",
        "example": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5"
    },
    "INNER JOIN": {
        "explanation": "JOIN combines rows from two or more tables based on a related column. INNER JOIN (the default type) only returns rows that have a match in both tables.",
        "example": "SELECT e.name, d.department_name FROM employees e JOIN departments d ON e.department_id = d.id"
    },
    "LEFT JOIN": {
        "explanation": "LEFT JOIN returns every row from the left table, even if there's no match in the right table — unmatched columns show as NULL.",
        "example": "SELECT e.name, p.project_name FROM employees e LEFT JOIN employee_projects ep ON e.id = ep.employee_id LEFT JOIN projects p ON ep.project_id = p.id"
    },
    "Self JOIN": {
        "explanation": "A self join joins a table to itself — useful when rows reference other rows in the same table, like an employee referencing their manager.",
        "example": "SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id"
    },
    "GROUP BY": {
        "explanation": "GROUP BY groups rows that share the same value in a column, so you can run aggregate functions (like COUNT, AVG, SUM) on each group separately.",
        "example": "SELECT department_id, AVG(salary) FROM employees GROUP BY department_id"
    },
    "HAVING": {
        "explanation": "HAVING filters groups after GROUP BY has run — it's like WHERE, but for grouped results. You can't use WHERE for aggregate conditions.",
        "example": "SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*) > 3"
    },
    "Subqueries": {
        "explanation": "A subquery is a query nested inside another query. It runs first, and its result is used by the outer query.",
        "example": "SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)"
    },
    "EXISTS": {
        "explanation": "EXISTS checks whether a subquery returns any rows at all — it's often faster than IN for large subqueries, and handles NULLs more safely.",
        "example": "SELECT name FROM employees e WHERE EXISTS (SELECT 1 FROM employee_projects ep WHERE ep.employee_id = e.id)"
    },
    "Window Functions": {
        "explanation": "Window functions (like RANK, ROW_NUMBER) calculate a value across a set of rows without collapsing them into one row, unlike GROUP BY. PARTITION BY resets the calculation for each group.",
        "example": "SELECT name, department_id, salary, RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank FROM employees"
    },
    "CTE (WITH clause)": {
        "explanation": "A CTE (Common Table Expression) lets you name a temporary result set using WITH, then reference it like a table later in the query — making complex queries easier to read.",
        "example": "WITH high_earners AS (SELECT * FROM employees WHERE salary > 60000) SELECT name FROM high_earners"
    },
    "UNION & UNION ALL": {
        "explanation": "UNION combines the results of two queries into one list, removing duplicates. UNION ALL does the same but keeps duplicates, and is faster since it skips the duplicate check.",
        "example": "SELECT name FROM employees WHERE department_id = 1 UNION SELECT name FROM employees WHERE salary > 60000"
    },
    "CASE Statements": {
        "explanation": "CASE lets you add conditional logic inside a SELECT — like an if/else that returns different values based on a condition.",
        "example": "SELECT name, CASE WHEN salary > 60000 THEN 'High' ELSE 'Standard' END AS pay_band FROM employees"
    },
    "Views": {
        "explanation": "A VIEW is a saved query that behaves like a virtual table. It doesn't store data itself — every time you query it, it re-runs the underlying query.",
        "example": "CREATE VIEW employee_details AS SELECT e.name, d.department_name FROM employees e JOIN departments d ON e.department_id = d.id"
    },
    "Constraints": {
        "explanation": "Constraints enforce rules on data: PRIMARY KEY uniquely identifies each row, FOREIGN KEY links to another table, NOT NULL requires a value, and CHECK validates a condition.",
        "example": "CREATE TABLE employees (id INTEGER PRIMARY KEY, salary INTEGER CHECK(salary > 0), department_id INTEGER, FOREIGN KEY (department_id) REFERENCES departments(id))"
    },
    "Indexes": {
        "explanation": "An index is a lookup structure that speeds up searches on a column, similar to a book's index. Without one, the database scans every row (a 'full table scan').",
        "example": "CREATE INDEX idx_employee_salary ON employees(salary)"
    },
    "Triggers": {
        "explanation": "A trigger is code that runs automatically when a specific event happens (like an INSERT or UPDATE) on a table — useful for logging changes or enforcing extra rules.",
        "example": "CREATE TRIGGER salary_change_trigger AFTER UPDATE OF salary ON employees BEGIN INSERT INTO salary_audit (employee_id, old_salary, new_salary) VALUES (OLD.id, OLD.salary, NEW.salary); END"
    },
}