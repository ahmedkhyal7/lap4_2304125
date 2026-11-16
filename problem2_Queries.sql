USE library;

-- F2.1
-- Search by optional title keyword, price range and selected categories.
-- For the website implementation, values are bound using %s placeholders.
SELECT b.book_id, b.title, b.price, b.publish_year, a.name AS author_name, c.name AS category_name
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN category c ON b.category_id = c.category_id
WHERE b.title LIKE '%love%'
  AND b.price BETWEEN 10 AND 20
  AND b.category_id IN (1, 3)
ORDER BY b.price ASC;

-- F2.2
SELECT b.book_id, b.title, b.price, b.publish_year,
       a.name AS author_name, p.name AS publisher_name, c.name AS category_name
FROM book b
INNER JOIN author a ON b.author_id = a.author_id
INNER JOIN publisher p ON b.publisher_id = p.publisher_id
INNER JOIN category c ON b.category_id = c.category_id
ORDER BY b.title;

-- F2.3 (a)
SELECT c.category_id, c.name AS category_name,
       COUNT(b.book_id) AS book_count, AVG(b.price) AS average_price
FROM category c
LEFT JOIN book b ON b.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY c.name;

-- F2.3 (b)
SELECT a.author_id, a.name, COUNT(b.book_id) AS book_count
FROM author a
INNER JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2
ORDER BY book_count DESC;

-- F2.3 (c)
SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price
FROM book;

-- F2.4 (a)
SELECT l.loan_id, b.title AS book_title, m.name AS member_name, l.loan_date
FROM loan l
INNER JOIN book b ON l.book_id = b.book_id
INNER JOIN member m ON l.member_id = m.member_id
WHERE l.return_date IS NULL;

-- F2.4 (b)
SELECT m.member_id, m.name, m.email
FROM member m
LEFT JOIN loan l ON l.member_id = m.member_id
WHERE l.loan_id IS NULL;

-- F2.4 (c)
SELECT b.book_id, b.title
FROM book b
LEFT JOIN loan l ON l.book_id = b.book_id
WHERE l.loan_id IS NULL;

-- F2.5 (a)
SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count
FROM book b
INNER JOIN loan l ON l.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY loan_count DESC
LIMIT 3;

-- F2.5 (b)
SELECT m.member_id, m.name, COUNT(l.loan_id) AS loan_count
FROM member m
INNER JOIN loan l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
ORDER BY loan_count DESC
LIMIT 1;

-- F2.6 (a)
SELECT a.author_id, a.name, a.country, COUNT(b.book_id) AS book_count
FROM author a
LEFT JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name, a.country
ORDER BY a.name;

-- F2.6 (b)
SELECT b.book_id, b.title, a.name AS author_name, p.name AS publisher_name, a.country
FROM book b
INNER JOIN author a ON b.author_id = a.author_id
INNER JOIN publisher p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;
