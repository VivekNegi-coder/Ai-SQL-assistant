import sqlite3

conn = sqlite3.connect("company.db")

cursor = conn.cursor()

# Customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
)
""")

# Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price INTEGER
)
""")

# Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    amount INTEGER
)
""")

# Insert customers
cursor.execute("""
INSERT INTO customers (name, city)
VALUES
('Rahul', 'Pune'),
('Amit', 'Mumbai'),
('Sneha', 'Delhi')
""")

# Insert products
cursor.execute("""
INSERT INTO products (product_name, category, price)
VALUES
('Laptop', 'Electronics', 70000),
('Phone', 'Electronics', 30000),
('Shoes', 'Fashion', 5000)
""")

# Insert orders
cursor.execute("""
INSERT INTO orders (customer_id, product_id, amount)
VALUES
(1, 1, 70000),
(2, 2, 30000),
(3, 3, 5000),
(1, 2, 30000)
""")

conn.commit()

print("Database created successfully!")

conn.close()