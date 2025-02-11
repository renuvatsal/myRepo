
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

These answers should provide a strong base for understanding the thought process and techniques in SQL querying. Tableau SQL questions like `EXCEPT` might vary slightly based on the specific RDBMS syntactic conventions.
