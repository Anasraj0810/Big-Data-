/*Write a query to list customer names and their order numbers*/
SELECT c.customerName, o.orderNumber
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber;

/*Write a query to show all customers and their orders, including customers with no orders*/
SELECT c.customerName, o.orderNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber;

/*Write a query to find customers who have not placed any orders*/
SELECT c.customerName, o.orderNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE O.orderNumber is NULL;

/*Write a query to display total number of orders per customer*/
SELECT 
    customerName,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.customerNumber = c.customerNumber) AS total_orders
FROM customers c;

/*Write a query to assign row numbers to customers based on credit limit (highest first)*/
SELECT 
    customerName,
    creditLimit,
    ROW_NUMBER() OVER (ORDER BY creditLimit DESC) AS row_num
FROM customers;

/*Write a query to find customers whose credit limit is above the average credit limit*/

SELECT customerName, creditLimit
FROM customers
WHERE creditLimit > (select AVG(creditLimit) from customers);

/*Write a query to display customer name and total payment amount using subquery*/

SELECT
customerName,
(SELECT sum(amount)
FROM payments p
WHERE p.customerNumber = c.customerNumber) AS total_amount
FROM customers c;

/*Write a query to find top 3 customers based on credit limit*/

SELECT customerName, creditLimit
FROM customers
ORDER BY creditLimit DESC
limit 3 ;

/*Write a query to list orders with total order amount (quantity × price)*/

SELECT od.orderNumber, SUM((od.priceEach)*(od.quantityOrdered)) AS total_order_amount
FROM orderdetails od
GROUP BY od.orderNumber;

	/*Write a query to rank customers within each country based on credit limit*/
    
    SELECT 
    customerName,
    creditLimit,
    Country,
    RANK() OVER (partition by Country ORDER BY creditLimit DESC) AS rank_val
FROM customers;

/*Write a query to find customers who placed more orders than the average number of orders per customer*/

SELECT c.customerName, COUNT(o.orderNumber) AS TotalCount
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerName
HAVING COUNT(o.orderNumber) > (
SELECT AVG(order_counts)
FROM (
SELECT COUNT(orderNumber) AS order_counts
FROM orders
GROUP BY customerNumber 
)  AS subquery
);

/*Write a query to display customer name, order number, and product name (use multiple joins)*/

SELECT c.customerName, o.orderNumber, p.productName
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode ;

/*Write a query to find products that have never been ordered*/

SELECT p.productName
FROM products p
LEFT JOIN orderdetails od ON p.productCode = od.productCode
WHERE od.productCode IS NULL ; 

/*Write a query to find 2nd highest credit limit using ranking function*/

SELECT customerName, creditLimit
FROM
(SELECT 
    customerName,
    creditLimit,
  RANK() OVER (ORDER BY creditLimit DESC) AS rnk
FROM customers) AS ranked
WHERE rnk = 2;

/*Write a query to find top 2 customers in each country based on credit limit*/

SELECT customerName, country, creditLimit
FROM (
    SELECT 
        customerName,
        country,
        creditLimit,
        DENSE_RANK() OVER (
            PARTITION BY country 
            ORDER BY creditLimit DESC
        ) AS rnk
    FROM customers
) AS ranked
WHERE rnk <= 2
ORDER BY country, creditLimit DESC;

/*Write a query to find total number of orders placed by each customer*/

SELECT 
    c.customerName,
    COUNT(o.orderNumber) AS total_orders
FROM customers c
JOIN orders o
    ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber, c.customerName;

/*Write a query to calculate total payment amount made by each customer*/

SELECT 
    c.customerName,
    SUM(p.amount) AS total_payment
FROM customers c
JOIN payments p
    ON c.customerNumber = p.customerNumber
GROUP BY c.customerName;

/*Write a query to find average credit limit for each country*/

SELECT country, avg(creditLimit) AS avg_credit_limit
FROM customers
GROUP BY country;

/*Write a query to display total quantity ordered for each product*/

SELECT p.productName, SUM(quantityOrdered) AS total_quantity
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode
ORDER BY p.productName DESC;

/*Write a query to find number of employees working in each office*/

SELECT e.officeCode, COUNT(e.employeeNumber) AS total_employees
FROM employees e
GROUP BY e.officeCode;



