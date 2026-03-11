#Shopping Cart

CREATE DATABASE IF NOT EXISTS shopping_cart_db;
USE shopping_cart_db;

CREATE TABLE IF NOT EXISTS products (
    serial INT PRIMARY KEY,
    item VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    distance INT NOT NULL,
    delivery_charge DECIMAL(10,2) NOT NULL,
    grand_total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_serial INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    qty INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    line_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_serial) REFERENCES products(serial)
);

USE shopping_cart_db;

REPLACE INTO products (serial, item, quantity, price) VALUES
(1, 'Charger', 5, 20.50),
(2, 'Samsung', 10, 90.00),
(3, 'Iphone', 20, 100.00);

select * from products ;

USE shopping_cart_db;

SELECT * FROM orders;
SELECT * FROM order_items;