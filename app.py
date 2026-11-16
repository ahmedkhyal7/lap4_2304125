import os
from decimal import Decimal, InvalidOperation
from functools import wraps

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from jinja2 import DictLoader
from werkzeug.exceptions import HTTPException

from pages import CSS, TEMPLATES

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
app.jinja_loader = DictLoader(TEMPLATES)


@app.context_processor
def inject_css():
    return {"css": CSS}


def confirm_page(message, cancel_endpoint):
    return render_template("confirm.html", message=message, cancel_url=url_for(cancel_endpoint))


REG_DB = "registration"
LIB_DB = "library"


def get_conn(db):
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=db,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def query(db, sql, params=(), one=False):
    conn = get_conn(db)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone() if one else cur.fetchall()
    finally:
        conn.close()


def execute(db, sql, params=()):
    conn = get_conn(db)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount, cur.lastrowid
    finally:
        conn.close()


def hash_password(password):
    return bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt(12)).decode()


def check_password(password, password_hash):
    try:
        return bcrypt.checkpw(password.encode()[:72], password_hash.encode())
    except ValueError:
        return False


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    return redirect(url_for("todos" if "user_id" in session else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("todos"))
    errors, form = [], {}
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        form = {"name": name, "email": email}
        if not name:
            errors.append("Name is required")
        elif len(name) > 100:
            errors.append("Name is too long (100 characters at most)")
        if not email:
            errors.append("Email is required")
        elif len(email) > 255:
            errors.append("Email is too long (255 characters at most)")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")
        if not errors:
            try:
                _, new_id = execute(
                    REG_DB,
                    "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                    (email, name, hash_password(password)),
                )
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] == 1062:
                    errors.append("Email Already Exists")
                else:
                    raise
            else:
                session.clear()
                session["user_id"] = new_id
                session["name"] = name
                return redirect(url_for("todos"))
    return render_template("register.html", errors=errors, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("todos"))
    errors, form = [], {}
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        form = {"email": email}
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not errors:
            user = query(
                REG_DB,
                "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                (email,),
                one=True,
            )
            if user and check_password(password, user["password_hash"]):
                session.clear()
                session["user_id"] = user["user_id"]
                session["name"] = user["name"]
                return redirect(url_for("todos"))
            errors.append("Invalid email or password")
    return render_template("login.html", errors=errors, form=form)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def check_title(title):
    if not title.strip():
        return ["Title is required"]
    if len(title.strip()) > 200:
        return ["Title is too long (200 characters at most)"]
    return []


def render_todos(errors=None, new_title="", row_errors=None, row_values=None):
    rows = query(
        REG_DB,
        "SELECT todo_id, title, is_done, created_at FROM todos "
        "WHERE user_id = %s ORDER BY todo_id DESC",
        (session["user_id"],),
    )
    return render_template(
        "todos.html", todos=rows, errors=errors or [], new_title=new_title,
        row_errors=row_errors or {}, row_values=row_values or {},
    )


@app.route("/todos")
@login_required
def todos():
    return render_todos()


@app.route("/todos/add", methods=["POST"])
@login_required
def todo_add():
    title = request.form.get("title", "").strip()
    errors = check_title(title)
    if errors:
        return render_todos(errors=errors, new_title=title)
    execute(REG_DB, "INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session["user_id"], title))
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
@login_required
def todo_edit(todo_id):
    title = request.form.get("title", "").strip()
    errors = check_title(title)
    if errors:
        return render_todos(row_errors={todo_id: errors}, row_values={todo_id: title})
    execute(
        REG_DB, "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
        (title, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
@login_required
def todo_toggle(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0
    execute(
        REG_DB, "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
        (is_done, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["GET", "POST"])
@login_required
def todo_delete(todo_id):
    if request.method == "GET":
        return confirm_page("Are you sure you want to delete this to-do?", "todos")
    execute(REG_DB, "DELETE FROM todos WHERE todo_id = %s AND user_id = %s", (todo_id, session["user_id"]))
    return redirect(url_for("todos"))


# ---------------- Existing library management ----------------

def get_authors():
    return query(LIB_DB, "SELECT author_id, name, country FROM author ORDER BY author_id")


def check_author(name, country):
    errors = []
    if not name:
        errors.append("Name is required")
    elif len(name) > 100:
        errors.append("Name is too long (100 characters at most)")
    if not country:
        errors.append("Country is required")
    elif len(country) > 50:
        errors.append("Country is too long (50 characters at most)")
    return errors


def check_book(title, price, author_id, valid_ids):
    errors = []
    if not title:
        errors.append("Title is required")
    elif len(title) > 200:
        errors.append("Title is too long (200 characters at most)")
    if not price:
        errors.append("Price is required")
    else:
        try:
            value = Decimal(price)
            if not value.is_finite():
                raise InvalidOperation
            if value < 0:
                errors.append("Price cannot be negative")
            elif value > Decimal("99999999.99"):
                errors.append("Price is too large")
        except InvalidOperation:
            errors.append("Price must be a number")
    if not author_id:
        errors.append("Author is required")
    elif not author_id.isdigit() or int(author_id) not in valid_ids:
        errors.append("Author does not exist")
    return errors


@app.route("/library")
@login_required
def library():
    authors = get_authors()
    books = query(LIB_DB, "SELECT book_id, title, price, author_id FROM book ORDER BY book_id")
    names = {a["author_id"]: a["name"] for a in authors}
    return render_template("library.html", authors=authors, books=books, names=names)


@app.route("/library/authors/new", methods=["GET", "POST"])
@login_required
def author_new():
    errors, form = [], {"name": "", "country": ""}
    if request.method == "POST":
        form = {"name": request.form.get("name", "").strip(), "country": request.form.get("country", "").strip()}
        errors = check_author(form["name"], form["country"])
        if not errors:
            execute(LIB_DB, "INSERT INTO author (name, country) VALUES (%s, %s)", (form["name"], form["country"]))
            flash("Author added")
            return redirect(url_for("library"))
    return render_template("author_form.html", errors=errors, form=form, author_id=None)


@app.route("/library/authors/<int:author_id>/edit", methods=["GET", "POST"])
@login_required
def author_edit(author_id):
    author = query(
        LIB_DB, "SELECT author_id, name, country FROM author WHERE author_id = %s", (author_id,), one=True
    )
    if not author:
        flash("That author does not exist")
        return redirect(url_for("library"))
    errors, form = [], {"name": author["name"], "country": author["country"]}
    if request.method == "POST":
        form = {"name": request.form.get("name", "").strip(), "country": request.form.get("country", "").strip()}
        errors = check_author(form["name"], form["country"])
        if not errors:
            execute(
                LIB_DB, "UPDATE author SET name = %s, country = %s WHERE author_id = %s",
                (form["name"], form["country"], author_id),
            )
            flash("Author updated")
            return redirect(url_for("library"))
    return render_template("author_form.html", errors=errors, form=form, author_id=author_id)


@app.route("/library/authors/<int:author_id>/delete", methods=["GET", "POST"])
@login_required
def author_delete(author_id):
    if request.method == "GET":
        return confirm_page("Delete this author? All of their books will be deleted too.", "library")
    execute(LIB_DB, "DELETE FROM author WHERE author_id = %s", (author_id,))
    flash("Author and their books deleted")
    return redirect(url_for("library"))


@app.route("/library/books/new", methods=["GET", "POST"])
@login_required
def book_new():
    authors = get_authors()
    publishers = query(LIB_DB, "SELECT publisher_id, name FROM publisher ORDER BY name")
    categories = get_categories()
    valid_author_ids = {str(a["author_id"]) for a in authors}
    valid_publisher_ids = {str(p["publisher_id"]) for p in publishers}
    valid_category_ids = {str(c["category_id"]) for c in categories}
    errors = []
    form = {"title": "", "price": "", "publish_year": "", "author_id": "", "publisher_id": "", "category_id": ""}

    if request.method == "POST":
        form = {
            "title": request.form.get("title", "").strip(),
            "price": request.form.get("price", "").strip(),
            "publish_year": request.form.get("publish_year", "").strip(),
            "author_id": request.form.get("author_id", "").strip(),
            "publisher_id": request.form.get("publisher_id", "").strip(),
            "category_id": request.form.get("category_id", "").strip(),
        }
        errors = check_book(form["title"], form["price"], form["author_id"], {int(x) for x in valid_author_ids})
        if not form["publish_year"].isdigit() or not 1000 <= int(form["publish_year"] or 0) <= 2155:
            errors.append("Publish year must be a valid year.")
        if form["publisher_id"] not in valid_publisher_ids:
            errors.append("Choose a valid publisher.")
        if form["category_id"] not in valid_category_ids:
            errors.append("Choose a valid category.")

        if not errors:
            execute(
                LIB_DB,
                """INSERT INTO book (title, price, publish_year, author_id, publisher_id, category_id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    form["title"], form["price"], int(form["publish_year"]),
                    int(form["author_id"]), int(form["publisher_id"]), int(form["category_id"]),
                ),
            )
            flash("Book added")
            return redirect(url_for("library"))

    return render_template(
        "book_form.html", errors=errors, form=form, authors=authors,
        publishers=publishers, categories=categories, book_id=None,
    )


@app.route("/library/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def book_edit(book_id):
    book = query(
        LIB_DB,
        """SELECT book_id, title, price, publish_year, author_id, publisher_id, category_id
           FROM book WHERE book_id = %s""",
        (book_id,),
        one=True,
    )
    if not book:
        flash("That book does not exist")
        return redirect(url_for("library"))

    authors = get_authors()
    publishers = query(LIB_DB, "SELECT publisher_id, name FROM publisher ORDER BY name")
    categories = get_categories()
    valid_author_ids = {str(a["author_id"]) for a in authors}
    valid_publisher_ids = {str(p["publisher_id"]) for p in publishers}
    valid_category_ids = {str(c["category_id"]) for c in categories}
    errors = []
    form = {
        "title": book["title"], "price": "%.2f" % book["price"],
        "publish_year": str(book["publish_year"]), "author_id": str(book["author_id"]),
        "publisher_id": str(book["publisher_id"]), "category_id": str(book["category_id"]),
    }

    if request.method == "POST":
        form = {
            "title": request.form.get("title", "").strip(),
            "price": request.form.get("price", "").strip(),
            "publish_year": request.form.get("publish_year", "").strip(),
            "author_id": request.form.get("author_id", "").strip(),
            "publisher_id": request.form.get("publisher_id", "").strip(),
            "category_id": request.form.get("category_id", "").strip(),
        }
        errors = check_book(form["title"], form["price"], form["author_id"], {int(x) for x in valid_author_ids})
        if not form["publish_year"].isdigit() or not 1000 <= int(form["publish_year"] or 0) <= 2155:
            errors.append("Publish year must be a valid year.")
        if form["publisher_id"] not in valid_publisher_ids:
            errors.append("Choose a valid publisher.")
        if form["category_id"] not in valid_category_ids:
            errors.append("Choose a valid category.")

        if not errors:
            execute(
                LIB_DB,
                """UPDATE book
                   SET title = %s, price = %s, publish_year = %s, author_id = %s,
                       publisher_id = %s, category_id = %s
                   WHERE book_id = %s""",
                (
                    form["title"], form["price"], int(form["publish_year"]),
                    int(form["author_id"]), int(form["publisher_id"]),
                    int(form["category_id"]), book_id,
                ),
            )
            flash("Book updated")
            return redirect(url_for("library"))

    return render_template(
        "book_form.html", errors=errors, form=form, authors=authors,
        publishers=publishers, categories=categories, book_id=book_id,
    )


@app.route("/library/books/<int:book_id>/delete", methods=["GET", "POST"])
@login_required
def book_delete(book_id):
    if request.method == "GET":
        return confirm_page("Are you sure you want to delete this book?", "library")
    execute(LIB_DB, "DELETE FROM book WHERE book_id = %s", (book_id,))
    flash("Book deleted")
    return redirect(url_for("library"))


# ---------------- Lab 4 Part II: F2.1 - F2.6 ----------------

def get_categories():
    return query(LIB_DB, "SELECT category_id, name FROM category ORDER BY name")


@app.route("/library/search", methods=["GET", "POST"])
@login_required
def book_search():
    categories = get_categories()
    errors = []
    form = {"keyword": "", "min_price": "", "max_price": "", "category_ids": []}
    books = []
    searched = request.method == "POST"

    if searched:
        form = {
            "keyword": request.form.get("keyword", "").strip(),
            "min_price": request.form.get("min_price", "").strip(),
            "max_price": request.form.get("max_price", "").strip(),
            "category_ids": request.form.getlist("category_ids"),
        }

        min_value = max_value = None
        try:
            if form["min_price"]:
                min_value = Decimal(form["min_price"])
                if not min_value.is_finite() or min_value < 0:
                    raise InvalidOperation
            if form["max_price"]:
                max_value = Decimal(form["max_price"])
                if not max_value.is_finite() or max_value < 0:
                    raise InvalidOperation
            if min_value is not None and max_value is not None and min_value > max_value:
                errors.append("Minimum price cannot be greater than maximum price.")
        except InvalidOperation:
            errors.append("Enter valid non-negative prices.")

        valid_category_ids = {str(c["category_id"]) for c in categories}
        if any(cid not in valid_category_ids for cid in form["category_ids"]):
            errors.append("Invalid category selected.")

        if not errors:
            # Only fixed SQL fragments are assembled here. Every user value is
            # passed separately through %s placeholders (prepared parameters).
            sql = """
                SELECT b.book_id, b.title, b.price, b.publish_year,
                       c.name AS category_name, a.name AS author_name
                FROM book b
                JOIN category c ON b.category_id = c.category_id
                JOIN author a ON b.author_id = a.author_id
            """
            conditions, params = [], []

            if form["keyword"]:
                conditions.append("b.title LIKE %s")
                params.append("%" + form["keyword"] + "%")

            if min_value is not None and max_value is not None:
                conditions.append("b.price BETWEEN %s AND %s")
                params.extend([min_value, max_value])
            elif min_value is not None:
                conditions.append("b.price >= %s")
                params.append(min_value)
            elif max_value is not None:
                conditions.append("b.price <= %s")
                params.append(max_value)

            if form["category_ids"]:
                placeholders = ", ".join(["%s"] * len(form["category_ids"]))
                conditions.append(f"b.category_id IN ({placeholders})")
                params.extend([int(cid) for cid in form["category_ids"]])

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            sql += " ORDER BY b.price ASC, b.title ASC"
            books = query(LIB_DB, sql, tuple(params))

    return render_template(
        "book_search.html", categories=categories, books=books,
        form=form, errors=errors, searched=searched,
    )


@app.route("/library/catalogue")
@login_required
def catalogue():
    books = query(
        LIB_DB,
        """
        SELECT b.book_id, b.title, b.price, b.publish_year,
               a.name AS author_name, p.name AS publisher_name, c.name AS category_name
        FROM book b
        INNER JOIN author a ON b.author_id = a.author_id
        INNER JOIN publisher p ON b.publisher_id = p.publisher_id
        INNER JOIN category c ON b.category_id = c.category_id
        ORDER BY b.title
        """,
    )
    return render_template("catalogue.html", books=books)


@app.route("/library/reports")
@login_required
def reports():
    category_stats = query(
        LIB_DB,
        """
        SELECT c.category_id, c.name AS category_name,
               COUNT(b.book_id) AS book_count, AVG(b.price) AS average_price
        FROM category c
        LEFT JOIN book b ON b.category_id = c.category_id
        GROUP BY c.category_id, c.name
        ORDER BY c.name
        """,
    )
    prolific_authors = query(
        LIB_DB,
        """
        SELECT a.author_id, a.name, COUNT(b.book_id) AS book_count
        FROM author a
        INNER JOIN book b ON b.author_id = a.author_id
        GROUP BY a.author_id, a.name
        HAVING COUNT(b.book_id) >= 2
        ORDER BY book_count DESC, a.name
        """,
    )
    price_summary = query(
        LIB_DB,
        "SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price FROM book",
        one=True,
    )
    return render_template(
        "reports.html", category_stats=category_stats,
        prolific_authors=prolific_authors, price_summary=price_summary,
    )


@app.route("/library/loans")
@login_required
def loans_report():
    unreturned = query(
        LIB_DB,
        """
        SELECT l.loan_id, b.title AS book_title, m.name AS member_name, l.loan_date
        FROM loan l
        INNER JOIN book b ON l.book_id = b.book_id
        INNER JOIN member m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL
        ORDER BY l.loan_date
        """,
    )
    members_without_loans = query(
        LIB_DB,
        """
        SELECT m.member_id, m.name, m.email
        FROM member m
        LEFT JOIN loan l ON l.member_id = m.member_id
        WHERE l.loan_id IS NULL
        ORDER BY m.name
        """,
    )
    books_never_borrowed = query(
        LIB_DB,
        """
        SELECT b.book_id, b.title
        FROM book b
        LEFT JOIN loan l ON l.book_id = b.book_id
        WHERE l.loan_id IS NULL
        ORDER BY b.title
        """,
    )
    return render_template(
        "loans_report.html", unreturned=unreturned,
        members_without_loans=members_without_loans,
        books_never_borrowed=books_never_borrowed,
    )


@app.route("/library/most-borrowed")
@login_required
def most_borrowed():
    top_books = query(
        LIB_DB,
        """
        SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count
        FROM book b
        INNER JOIN loan l ON l.book_id = b.book_id
        GROUP BY b.book_id, b.title
        ORDER BY loan_count DESC, b.title
        LIMIT 3
        """,
    )
    top_member = query(
        LIB_DB,
        """
        SELECT m.member_id, m.name, COUNT(l.loan_id) AS loan_count
        FROM member m
        INNER JOIN loan l ON l.member_id = m.member_id
        GROUP BY m.member_id, m.name
        ORDER BY loan_count DESC, m.name
        LIMIT 1
        """,
        one=True,
    )
    return render_template("most_borrowed.html", top_books=top_books, top_member=top_member)


@app.route("/library/authors-books")
@login_required
def authors_books():
    author_counts = query(
        LIB_DB,
        """
        SELECT a.author_id, a.name, a.country, COUNT(b.book_id) AS book_count
        FROM author a
        LEFT JOIN book b ON b.author_id = a.author_id
        GROUP BY a.author_id, a.name, a.country
        ORDER BY a.name
        """,
    )
    same_country_books = query(
        LIB_DB,
        """
        SELECT b.book_id, b.title, a.name AS author_name, p.name AS publisher_name,
               a.country
        FROM book b
        INNER JOIN author a ON b.author_id = a.author_id
        INNER JOIN publisher p ON b.publisher_id = p.publisher_id
        WHERE a.country = p.country
        ORDER BY b.title
        """,
    )
    return render_template(
        "authors_books.html", author_counts=author_counts,
        same_country_books=same_country_books,
    )


@app.errorhandler(Exception)
def handle_error(exc):
    if isinstance(exc, HTTPException):
        code, message = exc.code, exc.description
    else:
        app.logger.exception(exc)
        code = 500
        message = "Something went wrong. Check that MySQL is running and try again."
    return render_template("error.html", code=code, message=message), code


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
