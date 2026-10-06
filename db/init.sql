-- ============================================================
-- init.sql - Database Initialization Script
-- Stage 2: Creates database, 2 tables, and populates with data
-- This script runs AUTOMATICALLY when MySQL container starts
-- ============================================================

-- Create and select the database
CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

-- ============================================================
-- TABLE 1: employees
-- ============================================================
CREATE TABLE IF NOT EXISTS employees (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)    NOT NULL,
    department  VARCHAR(100)    NOT NULL,
    salary      DECIMAL(10,2)   NOT NULL,
    hire_date   DATE            NOT NULL
);

-- Insert sample employee records
INSERT INTO employees (name, department, salary, hire_date) VALUES
('Alice Johnson',  'Engineering', 95000.00, '2021-03-15'),
('Bob Smith',      'Marketing',   72000.00, '2020-07-01'),
('Carol White',    'HR',          65000.00, '2019-11-20'),
('David Brown',    'Engineering', 105000.00,'2022-01-10'),
('Eva Martinez',   'Finance',     88000.00, '2021-09-05'),
('Frank Lee',      'Marketing',   70000.00, '2023-02-14');

-- ============================================================
-- TABLE 2: products
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    product_name  VARCHAR(100)   NOT NULL,
    category      VARCHAR(100)   NOT NULL,
    price         DECIMAL(10,2)  NOT NULL,
    stock         INT            NOT NULL
);

-- Insert sample product records
INSERT INTO products (product_name, category, price, stock) VALUES
('Laptop Pro',      'Electronics', 1299.99, 50),
('Wireless Mouse',  'Electronics',   29.99, 200),
('Office Chair',    'Furniture',    349.99,  30),
('Standing Desk',   'Furniture',    599.99,  15),
('USB-C Hub',       'Electronics',   49.99, 120),
('Monitor 27"',     'Electronics',  399.99,  40);
