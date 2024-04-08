-- create_tables.sql

-- Create the users table
CREATE TABLE users (
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
);

-- Create the products table
CREATE TABLE products (
    productId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    description TEXT,
    image TEXT,
    stock INT,
    categoryId INT,
    FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
);

-- Create the kart table
CREATE TABLE kart (
    userId INT,
    productId INT,
    FOREIGN KEY(userId) REFERENCES users(userId),
    FOREIGN KEY(productId) REFERENCES products(productId)
);

-- Create the categories table
CREATE TABLE categories (
    categoryId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

-- Create the orders table
CREATE TABLE orders (
    orderId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    productId INT,
    FOREIGN KEY(userId) REFERENCES users(userId),
    FOREIGN KEY(productId) REFERENCES products(productId)
);
