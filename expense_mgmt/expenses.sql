CREATE DATABASE expense_management;
USE expense_management;

CREATE TABLE users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(100),
                       email VARCHAR(100) UNIQUE,
                       password VARCHAR(255)
);


CREATE TABLE expenses (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          user_id INT,
                          amount DECIMAL(10, 2),
                          expense_type VARCHAR(50),
                          expense_date DATE,
                          FOREIGN KEY (user_id) REFERENCES users(id)
);
