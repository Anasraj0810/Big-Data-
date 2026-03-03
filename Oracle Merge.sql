
CREATE TABLE customers_master (
  customer_id   NUMBER PRIMARY KEY,
  customer_name VARCHAR2(100),
  phone         VARCHAR2(20)
);

CREATE TABLE customers_updates (
  customer_id   NUMBER PRIMARY KEY,
  customer_name VARCHAR2(100),
  phone         VARCHAR2(20),
  commentt      VARCHAR2(200)
);

INSERT INTO customers_master (customer_id, customer_name, phone)
VALUES 
(101, 'Alice',   '111-111'),
(102, 'Bob',     '222-222'),
(103, 'Charlie', '333-333'),
(104, 'Diana',   '444-444');


INSERT ALL
  INTO customers_updates (customer_id, customer_name, phone, commentt)
  VALUES (101, 'Alice M', '111-999', 'Should UPDATE')
  INTO customers_updates (customer_id, customer_name, phone, commentt)
  VALUES (103, 'Charlie', '333-333', 'No change')
  INTO customers_updates (customer_id, customer_name, phone, commentt)
  VALUES (105, 'Eva',     '555-555', 'Should INSERT')
SELECT 1 FROM dual;

MERGE INTO customers_master m
USING customers_updates u
ON (m.customer_id = u.customer_id)
WHEN MATCHED THEN
  UPDATE SET
    m.customer_name = u.customer_name,
    m.phone        = u.phone
WHEN NOT MATCHED THEN
  INSERT (customer_id, customer_name, phone)
  VALUES (u.customer_id, u.customer_name, u.phone);


DELETE FROM customers_master m
WHERE NOT EXISTS (
  SELECT 1
  FROM customers_updates u
  WHERE u.customer_id = m.customer_id
);

SELECT * FROM customers_master;