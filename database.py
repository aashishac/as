import mysql.connector

# Open a connection to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='onlinebook'
)
cursor = conn.cursor()

# Create the users table
cursor.execute('''CREATE TABLE users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255),
    email VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    zipcode VARCHAR(10),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(20)
)''')

# Create the products table
cursor.execute('''CREATE TABLE products (
    productId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    description TEXT,
    image TEXT,
    stock INT,
    categoryId INT,
    FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
)''')




# Create the orders table
cursor.execute('''CREATE TABLE orders (
    orderId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    productId INT,
    FOREIGN KEY(userId) REFERENCES users(userId),
    FOREIGN KEY(productId) REFERENCES products(productId)
)''')

# Commit changes and close the connection
conn.commit()
conn.close()
