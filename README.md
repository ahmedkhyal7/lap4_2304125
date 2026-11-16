# Database Lab 4
## Ahmed Khyal Ahmed (2304125)

## Included
- `app.py`, `pages.py`
- `problem1_DDL.sql`, `problem1_DML.sql`,`problem2_DDL.sql`, `problem2_DML.sql`, `problem2_Queries.sql`
- `.env.example`, `.gitignore`, `requirements.txt`.


## Setup
 In MySQL Workbench, run `problem2_DDL.sql`, then `problem2_DML.sql`. **The DDL drops and recreates the `library` database**, so back up any Library data you need first. The existing `registration` database is not recreated by these two scripts.
 Run `python app.py`.
 Open `http://127.0.0.1:5000`.


## Lab 4 pages

Use the navigation bar:

- Search books – F2.1
- Catalogue – F2.2
- Reports – F2.3
- Loans – F2.4
- Most borrowed – F2.5
- Authors & books – F2.6


## Bonus: prepared statements in F2.1

The search route builds only fixed SQL clauses and passes all user-entered values separately in a parameter tuple to PyMySQL. For example, title search uses `b.title LIKE %s`, and the actual keyword is passed in `params`. Category IDs use one `%s` placeholder per selected category. User input is never inserted directly into the SQL text.

`problem2_Queries.sql` contains the corresponding SQL queries for running and demonstrating F2.1–F2.6 in MySQL.