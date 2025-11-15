-- Create database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    isbn VARCHAR(50),
    copies_total INT,
    copies_available INT
);

-- Members table
CREATE TABLE IF NOT EXISTS members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(200)
);

-- Issued books table
CREATE TABLE IF NOT EXISTS issued_books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    member_id INT,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Insert sample books
INSERT INTO books (title, author, isbn, copies_total, copies_available) VALUES
('Atomic Habits', 'James Clear', '9780735211292', 5, 5),
('The Alchemist', 'Paulo Coelho', '9780062315007', 4, 4),
('Think and Grow Rich', 'Napoleon Hill', '9781585424337', 3, 3),
('Python Crash Course', 'Eric Matthes', '9781593276034', 6, 6),
('Clean Code', 'Robert C. Martin', '9780132350884', 2, 2),
('Rich Dad Poor Dad', 'Robert Kiyosaki', '9781612680194', 4, 4),
('Sapiens', 'Yuval Noah Harari', '9780062316097', 2, 2),
('Deep Work', 'Cal Newport', '9781455586691', 3, 3);
