### BASICS
1. **Basic Queries:**
   - **Write a SQL query to select all columns from a table named `Employees`.**
     ```sql
     SELECT * FROM Employees;
     ```

   - **How would you retrieve only the `name` and `email` columns from the `Customers` table?**
     ```sql
     SELECT name, email FROM Customers;
     ```

   - **Write a query to find all records in the `Orders` table where the order date is after January 1, 2023.**
     ```sql
     SELECT * FROM Orders WHERE order_date > '2023-01-01';
     ```

2. **Filtering and Sorting:**
   - **How do you write a query to get names of employees with a salary greater than 50,000?**
     ```sql
     SELECT name FROM Employees WHERE salary > 50000;
     ```

   - **Write a SQL query to order employees by their last name in ascending order.**
     ```sql
     SELECT * FROM Employees ORDER BY last_name ASC;
     ```

   - **Retrieve a list of customers from `Customer` table, ordered by their `signup_date` descending.**
     ```sql
     SELECT * FROM Customer ORDER BY signup_date DESC;
     ```

3. **Aggregations and Grouping:**
   - **How would you find the total number of orders in the `Orders` table?**
     ```sql
     SELECT COUNT(*) AS total_orders FROM Orders;
     ```

   - **Generate a list of customers and the count of orders they have placed.**
     ```sql
     SELECT customer_id, COUNT(*) AS order_count FROM Orders GROUP BY customer_id;
     ```

   - **Write a query to calculate the average salary of employees in each department.**
     ```sql
     SELECT department_id, AVG(salary) AS average_salary FROM Employees GROUP BY department_id;
     ```

4. **Joins:**
   - **Write a SQL query to find all employees and their respective department names using a `JOIN`.**
     ```sql
     SELECT Employees.name, Departments.department_name
     FROM Employees
     JOIN Departments ON Employees.department_id = Departments.id;
     ```

   - **How do you display a list of orders along with customer names using an `INNER JOIN`?**
     ```sql
     SELECT Orders.id, Customers.name
     FROM Orders
     INNER JOIN Customers ON Orders.customer_id = Customers.id;
     ```

   - **Create a query fetching all products along with the supplier name using a `LEFT JOIN`.**
     ```sql
     SELECT Products.product_name, Suppliers.supplier_name
     FROM Products
     LEFT JOIN Suppliers ON Products.supplier_id = Suppliers.id;
     ```

5. **Subqueries:**
   - **Write a query to find employees who earn more than the average salary.**
     ```sql
     SELECT * FROM Employees WHERE salary > (SELECT AVG(salary) FROM Employees);
     ```

   - **How do you retrieve the names of customers who have placed more than ten orders using a subquery?**
     ```sql
     SELECT name FROM Customers
     WHERE id IN (
         SELECT customer_id FROM Orders
         GROUP BY customer_id
         HAVING COUNT(*) > 10
     );
     ```

   - **Use a subquery to find the highest order amount from the `Orders` table.**
     ```sql
     SELECT MAX(order_amount) FROM Orders;
     ```
     *(Alternatively, as a subquery within SELECT)*
     ```sql
     SELECT order_amount FROM Orders WHERE order_amount = (SELECT MAX(order_amount) FROM Orders);
     ```

6. **Set Operations:**
   - **Describe a query that combines results from two tables using a `UNION`.**
     ```sql
     SELECT name FROM TableA
     UNION
     SELECT name FROM TableB;
     ```
     *(Note: `UNION` removes duplicates by default. Use `UNION ALL` to include duplicates.)*

   - **Write a query that finds all products not sold in 2023 using `EXCEPT` or `MINUS`.**
     *(Use `MINUS` if using Oracle or `EXCEPT` if using SQL Server)*
     ```sql
     SELECT product_id FROM Products
     EXCEPT
     SELECT product_id FROM Sales WHERE sale_date >= '2023-01-01';
     ```

7. **Advanced Queries:**
   - **Write a query to find the nth highest salary from the `Employees` table.**
     *(Example for 3rd highest salary)*
     ```sql
     SELECT DISTINCT salary
     FROM Employees
     ORDER BY salary DESC
     LIMIT 1 OFFSET 2;
     ```

   - **How would you update the `email` domain of all employees to `@company.com` in the `Employees` table?**
     ```sql
     UPDATE Employees
     SET email = CONCAT(SUBSTRING_INDEX(email, '@', 1), '@company.com');
     ```

   - **Create a recursive query using Common Table Expressions (CTE) to list all managers in the `Management` hierarchy.**
     ```sql
     WITH RECURSIVE ManagementHierarchy AS (
         SELECT id, name, manager_id
         FROM Employees
         WHERE manager_id IS NULL
         UNION ALL
         SELECT e.id, e.name, e.manager_id
         FROM Employees e
         INNER JOIN ManagementHierarchy mh ON e.manager_id = mh.id
     )
     SELECT * FROM ManagementHierarchy;
     ```

8. **Indexes and Performance:**
   - **What is an index, and how would you create one for the `email` column of the `Users` table?**
     - An index is a database object that improves the speed of data retrieval. It acts like a pointer to data in a table to allow quicker searches.
     ```sql
     CREATE INDEX idx_users_email ON Users(email);
     ```

   - **How do you find and explain a query execution plan in SQL?**
     - Use `EXPLAIN` or `EXPLAIN ANALYZE` (depending on the DBMS) before your query to display the execution plan.
     ```sql
     EXPLAIN SELECT * FROM Employees WHERE salary > 50000;
     ```

9. **Data Modification:**
   - **Write a query to delete all records from the `Users` table where the user hasn't logged in the past five years.**
     ```sql
     DELETE FROM Users WHERE last_login < DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
     ```

   - **How do you insert a new record into the `Products` table with specified values?**
     ```sql
     INSERT INTO Products (product_name, price, quantity)
     VALUES ('New Product', 25.00, 100);
     ```

10. **Data Integrity and Constraints:**
    - **Explain how to enforce referential integrity with a foreign key constraint.**
      - To ensure referential integrity, define a foreign key constraint that links to a primary key in another table.
      ```sql
      ALTER TABLE Orders
      ADD CONSTRAINT fk_customer
      FOREIGN KEY (customer_id) REFERENCES Customers(id);
      ```

    - **Write a query that alters a table to add a NOT NULL constraint to an existing column.**
      ```sql
      ALTER TABLE Employees
      MODIFY COLUMN department_id INT NOT NULL;
      ```

### ADVANCED

### Scenario 1: Employee Salaries by Department
**Scenario:** Identify the highest, lowest, and average salary within each department and display these alongside the department name. Order the results by average salary in descending order.
**Query:**

```sql
SELECT 
    Departments.department_name,
    MAX(Employees.salary) AS highest_salary,
    MIN(Employees.salary) AS lowest_salary,
    AVG(Employees.salary) AS average_salary
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
GROUP BY 
    Departments.department_name
ORDER BY 
    average_salary DESC;
```

### Scenario 2: Department Employee Distribution
**Scenario:** For each department, determine the percentage of total employees company-wide that belong to that department. Display the department name and the percentage, rounded to two decimal places.
**Query:**

```sql
SELECT 
    Departments.department_name,
    ROUND((COUNT(Employees.id) * 100.0) / (SELECT COUNT(*) FROM Employees), 2) AS percentage_of_total
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
GROUP BY 
    Departments.department_name;
```

### Scenario 3: Salary Budget Comparison
**Scenario:** For departments where the average salary exceeds the overall company's average salary, list the department names and their average salaries. Order them by the salary difference from the company's average, in descending order.
**Query:**

```sql
WITH AvgCompanySalary AS (
    SELECT AVG(salary) AS company_average_salary FROM Employees
)
SELECT 
    Departments.department_name,
    AVG(Employees.salary) AS average_salary
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
GROUP BY 
    Departments.department_name
HAVING 
    AVG(Employees.salary) > (SELECT company_average_salary FROM AvgCompanySalary)
ORDER BY 
    AVG(Employees.salary) - (SELECT company_average_salary FROM AvgCompanySalary) DESC;
```

### Scenario 4: Recent Hires
**Scenario:** Display the names and department names of employees hired in the last 6 months. Ensure that the list is ordered by hire date, showing the most recent hires first.
**Query:**

```sql
SELECT 
    Employees.name,
    Departments.department_name,
    Employees.hire_date
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
WHERE 
    Employees.hire_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
ORDER BY 
    Employees.hire_date DESC;
```

### Scenario 5: Departments with Employee Count Range
**Scenario:** List departments with employee counts between 10 and 50, inclusive. Provide the department name and the number of employees.
**Query:**

```sql
SELECT 
    Departments.department_name,
    COUNT(Employees.id) AS employee_count
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
GROUP BY 
    Departments.department_name
HAVING 
    employee_count BETWEEN 10 AND 50;
```

### Scenario 6: Senior Employees in Each Department
**Scenario:** For each department, list the names of the top 3 highest-paid employees. Include their salaries, and order them by salary descending within each department.
**Query:**

```sql
SELECT 
    e.name, 
    d.department_name, 
    e.salary
FROM 
    Employees e
JOIN 
    Departments d ON e.department_id = d.id
WHERE 
    (SELECT COUNT(*) 
     FROM Employees e2 
     WHERE e2.department_id = e.department_id AND e2.salary > e.salary) < 3
ORDER BY 
    d.department_name, e.salary DESC;
```

### Scenario 7: Department Budget Overview
**Scenario:** Calculate the total salary budget for each department and list departments where the budget exceeds $500,000. Display the department name and total budget, and order by budget in descending order.
**Query:**

```sql
SELECT 
    Departments.department_name,
    SUM(Employees.salary) AS total_budget
FROM 
    Employees
JOIN 
    Departments ON Employees.department_id = Departments.id
GROUP BY 
    Departments.department_name
HAVING 
    total_budget > 500000
ORDER BY 
    total_budget DESC;
```

### Scenario 8: Employee Turnover Rate
**Scenario:** For each department, calculate and display the employee turnover rate over the last year, given information on hires and terminations. Present the department name alongside the turnover rate.
**Query:**

```sql
WITH TurnoverData AS (
    SELECT 
        department_id,
        COUNT(CASE WHEN termination_date IS NOT NULL AND termination_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN 1 END) AS terminations,
        COUNT(CASE WHEN hire_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN 1 END) AS hires
    FROM 
        Employees
    GROUP BY 
        department_id
)
SELECT 
    Departments.department_name,
    (terminations / GREATEST(hires, 1)) * 100 AS turnover_rate
FROM 
    TurnoverData
JOIN 
    Departments ON TurnoverData.department_id = Departments.id;
```

### Scenario 9: Departmental Salary Allocation
**Scenario:** Display each department's name along with a breakdown of the total salary allocation into four quartiles (Q1-Q4). Order the results alphabetically by department name.
**Query:**

```sql
SELECT 
    department_name,
    MIN(CASE WHEN quartile = 1 THEN salary END) AS Q1,
    MIN(CASE WHEN quartile = 2 THEN salary END) AS Q2,
    MIN(CASE WHEN quartile = 3 THEN salary END) AS Q3,
    MIN(CASE WHEN quartile = 4 THEN salary END) AS Q4
FROM (
    SELECT 
        d.department_name,
        e.salary,
        NTILE(4) OVER (PARTITION BY e.department_id ORDER BY e.salary) AS quartile
    FROM 
        Employees e
    JOIN 
        Departments d ON e.department_id = d.id
) sub
GROUP BY 
    department_name
ORDER BY 
    department_name;
```

### Scenario 10: Promotable Employees
**Scenario:** Identify employees in each department who have a salary in the top 5% within their department. List their names, current salary, and department name, ordering by department name first and salary second.
**Query:**

```sql
WITH SalaryPercentiles AS (
    SELECT 
        department_id,
        salary,
        NTILE(100) OVER (PARTITION BY department_id ORDER BY salary DESC) AS percentile
    FROM 
        Employees
)
SELECT 
    e.name,
    e.salary,
    d.department_name
FROM 
    Employees e
JOIN 
    SalaryPercentiles sp ON e.department_id = sp.department_id AND e.salary = sp.salary
JOIN 
    Departments d ON e.department_id = d.id
WHERE 
    sp.percentile <= 5
ORDER BY 
    d.department_name, e.salary DESC;
```
