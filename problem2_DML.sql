USE library;

INSERT INTO author (author_id, name, country) VALUES
(1, 'Naguib Mahfouz', 'Egypt'),
(2, 'Ahdaf Soueif', 'Egypt'),
(3, 'Jane Austen', 'United Kingdom'),
(4, 'Gabriel Garcia Marquez', 'Colombia'),
(5, 'Chinua Achebe', 'Nigeria'),
(6, 'Taha Hussein', 'Egypt');

INSERT INTO publisher (publisher_id, name, country) VALUES
(1, 'Cairo House', 'Egypt'),
(2, 'Penguin Classics', 'United Kingdom'),
(3, 'Editorial Sudamericana', 'Colombia');

INSERT INTO category (category_id, name) VALUES
(1, 'Novel'),
(2, 'Historical Fiction'),
(3, 'Literature');

INSERT INTO book (book_id, title, price, publish_year, author_id, publisher_id, category_id) VALUES
(1, 'Palace Walk', 15.50, 1956, 1, 1, 2),
(2, 'Midaq Alley', 12.00, 1947, 1, 1, 1),
(3, 'The Map of Love', 19.50, 1999, 2, 2, 1),
(4, 'In the Eye of the Sun', 17.25, 1992, 2, 2, 3),
(5, 'Pride and Prejudice', 9.99, 1813, 3, 2, 1),
(6, 'Emma', 11.25, 1815, 3, 2, 1),
(7, 'One Hundred Years of Solitude', 18.75, 1967, 4, 3, 3),
(8, 'Love in the Time of Cholera', 16.40, 1985, 4, 3, 1),
(9, 'Things Fall Apart', 14.00, 1958, 5, 2, 3),
(10, 'No Longer at Ease', 13.50, 1960, 5, 2, 3);

INSERT INTO member (member_id, name, email, join_date) VALUES
(1, 'Ahmed Hassan', 'ahmed@example.com', '2025-01-10'),
(2, 'Sara Ali', 'sara@example.com', '2025-02-15'),
(3, 'Omar Khaled', 'omar@example.com', '2025-03-20'),
(4, 'Mona Adel', 'mona@example.com', '2025-04-05'),
(5, 'Youssef Samir', 'youssef@example.com', '2025-05-12'),
(6, 'Nour Mostafa', 'nour@example.com', '2025-06-01');

INSERT INTO loan (loan_id, book_id, member_id, loan_date, return_date) VALUES
(1, 1, 1, '2025-07-01', '2025-07-10'),
(2, 1, 2, '2025-07-12', '2025-07-20'),
(3, 1, 3, '2025-08-01', '2025-08-12'),
(4, 2, 1, '2025-08-15', '2025-08-25'),
(5, 2, 4, '2025-09-01', '2025-09-11'),
(6, 3, 2, '2025-09-15', '2025-09-25'),
(7, 3, 3, '2025-10-01', '2025-10-10'),
(8, 4, 1, '2025-10-12', '2025-10-22'),
(9, 5, 4, '2025-11-01', '2025-11-12'),
(10, 7, 5, '2025-11-15', '2025-11-25'),
(11, 8, 2, '2025-12-01', NULL),
(12, 9, 3, '2025-12-05', NULL);
