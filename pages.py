"""All HTML and CSS of the website, written as Python strings."""

CSS = r"""
:root {
  --bg: #eef2f1; --card: #ffffff; --ink: #1b2a33; --muted: #62727b;
  --primary: #0f766e; --primary-dark: #0b5953; --danger: #b42318;
  --line: #cfd9d6; --err-bg: #fdecea; --ok-bg: #e3f4ef;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: var(--bg); color: var(--ink); line-height: 1.5; }
a { color: var(--primary); }
.topbar { display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1.25rem;
  padding:.75rem 1rem; background:var(--ink); color:#fff; }
.brand { font-weight:700; font-size:1.15rem; color:#fff; text-decoration:none; margin-right:auto; }
.topbar nav { display:flex; flex-wrap:wrap; gap:1rem; }
.topbar nav a { color:#d6e4e0; text-decoration:none; }
.topbar nav a:hover { color:#fff; text-decoration:underline; }
.user { display:flex; align-items:center; gap:.75rem; }
.topbar .btn-outline { color:#fff; border-color:#6c828b; }
.container { max-width:1050px; margin:1.25rem auto; padding:0 1rem; }
.card { background:var(--card); border:1px solid var(--line); border-radius:8px;
  padding:1.25rem; margin-bottom:1.25rem; }
.card.narrow { max-width:480px; margin-left:auto; margin-right:auto; }
h1 { font-size:1.4rem; margin:0 0 1rem; }
h2 { font-size:1.1rem; margin:1.2rem 0 .6rem; }
.section-head { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:.75rem; }
.section-head h1 { margin:0; }
.muted { color:var(--muted); }
label { display:block; font-weight:600; margin-bottom:.9rem; }
input[type=text], input[type=email], input[type=password], input[type=number], input[type=date], select {
  display:block; width:100%; margin-top:.3rem; padding:.55rem .65rem; font:inherit;
  font-weight:400; color:var(--ink); border:1px solid var(--line); border-radius:6px; background:#fff;
}
select[multiple] { min-height:125px; }
input:focus, select:focus, button:focus-visible, .btn:focus-visible { outline:3px solid #7cc5bb; outline-offset:1px; }
.row { display:flex; gap:.5rem; align-items:center; }
.row input[type=text] { margin-top:0; flex:1; min-width:0; }
.btn { display:inline-block; padding:.55rem 1rem; font:inherit; font-weight:600; color:#fff;
  background:var(--primary); border:1px solid var(--primary); border-radius:6px; cursor:pointer;
  text-decoration:none; text-align:center; }
.btn:hover { background:var(--primary-dark); }
.btn-small { padding:.35rem .7rem; font-size:.9rem; }
.btn-block { width:100%; }
.btn-outline { background:transparent; color:var(--primary); }
.btn-outline:hover { background:var(--ok-bg); }
.topbar .btn-outline:hover { background:#2c4350; }
.btn-danger { background:var(--danger); border-color:var(--danger); }
.errors { background:var(--err-bg); border:1px solid #f2b8b2; color:var(--danger);
  border-radius:6px; padding:.5rem .75rem; margin-bottom:.75rem; }
.errors ul { margin:0; padding-left:1.1rem; }
.flash { background:var(--ok-bg); border:1px solid #a8d8cd; color:var(--primary-dark);
  border-radius:6px; padding:.6rem .9rem; margin-bottom:1rem; }
.empty { color:var(--muted); text-align:center; padding:1.5rem .5rem; margin:0; }
.todo-list { list-style:none; margin:1.25rem 0 0; padding:0; }
.todo { display:flex; flex-wrap:wrap; align-items:flex-start; gap:.5rem; padding:.6rem 0; border-top:1px solid var(--line); }
.todo form.edit { flex:1; min-width:180px; }
.check { width:2.1rem; height:2.1rem; border-radius:50%; cursor:pointer; border:2px solid var(--primary);
  background:#fff; color:#fff; font-size:1.1rem; line-height:1; }
.todo.done .check { background:var(--primary); }
.todo.done input[type=text] { text-decoration:line-through; color:var(--muted); background:#f4f7f6; }
.table-wrap { overflow-x:auto; }
table { width:100%; border-collapse:collapse; }
th, td { text-align:left; padding:.55rem .6rem; border-bottom:1px solid var(--line); vertical-align:top; }
th { background:#f3f7f6; font-size:.9rem; }
td.actions { display:flex; gap:.4rem; }
.filter-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:0 1rem; }
.results-count { color:var(--muted); margin:.5rem 0; }
@media (max-width:480px) { .container { margin-top:.75rem; } .card { padding:1rem; } }
"""

TEMPLATES = {}
TEMPLATES["_macros.html"] = r"""
{% macro errors_box(errors) %}
{% if errors %}<div class="errors" role="alert"><ul>{% for e in errors %}<li>{{ e }}</li>{% endfor %}</ul></div>{% endif %}
{% endmacro %}
"""

TEMPLATES["base.html"] = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}Lab Site{% endblock %}</title><style>{{ css|safe }}</style></head><body>
<header class="topbar">
<a class="brand" href="{{ url_for('index') }}">Lab Site</a>
{% if session.user_id %}
<nav>
<a href="{{ url_for('todos') }}">To-Do</a>
<a href="{{ url_for('library') }}">Library</a>
<a href="{{ url_for('book_search') }}">Search books</a>
<a href="{{ url_for('catalogue') }}">Catalogue</a>
<a href="{{ url_for('reports') }}">Reports</a>
<a href="{{ url_for('loans_report') }}">Loans</a>
<a href="{{ url_for('most_borrowed') }}">Most borrowed</a>
<a href="{{ url_for('authors_books') }}">Authors & books</a>
</nav>
<div class="user"><span>Hi, {{ session.name }}</span>
<form method="post" action="{{ url_for('logout') }}"><button class="btn btn-outline btn-small">Log out</button></form></div>
{% endif %}
</header>
<main class="container">{% for message in get_flashed_messages() %}<div class="flash">{{ message }}</div>{% endfor %}
{% block content %}{% endblock %}</main></body></html>
"""

TEMPLATES["register.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}Register{% endblock %}{% block content %}
<section class="card narrow"><h1>Create your account</h1><form method="post" action="{{ url_for('register') }}">
{{ errors_box(errors) }}
<label>Name<input type="text" name="name" value="{{ form.get('name', '') }}" required maxlength="100" pattern=".*\S.*"></label>
<label>Email<input type="email" name="email" value="{{ form.get('email', '') }}" required maxlength="255"></label>
<label>Password<input type="password" name="password" required></label>
<label>Confirm password<input type="password" name="confirm_password" required></label>
<button class="btn btn-block">Register</button></form><p class="muted">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p></section>
{% endblock %}"""

TEMPLATES["login.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}Log in{% endblock %}{% block content %}
<section class="card narrow"><h1>Log in</h1><form method="post" action="{{ url_for('login') }}">
{{ errors_box(errors) }}<label>Email<input type="email" name="email" value="{{ form.get('email', '') }}" required></label>
<label>Password<input type="password" name="password" required></label><button class="btn btn-block">Log in</button></form>
<p class="muted">New here? <a href="{{ url_for('register') }}">Create an account</a></p></section>{% endblock %}"""

TEMPLATES["todos.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}To-Do{% endblock %}{% block content %}<section class="card"><h1>To-Do</h1>
<form method="post" action="{{ url_for('todo_add') }}">{{ errors_box(errors) }}<div class="row">
<input type="text" name="title" placeholder="What needs to be done?" value="{{ new_title }}" required maxlength="200" pattern=".*\S.*"><button class="btn">Add</button></div></form>
{% if todos %}<ul class="todo-list">{% for t in todos %}<li class="todo{% if t.is_done %} done{% endif %}">
<form method="post" action="{{ url_for('todo_toggle', todo_id=t.todo_id) }}"><input type="hidden" name="is_done" value="{{ 0 if t.is_done else 1 }}">
<button class="check" aria-label="{{ 'Mark as not done' if t.is_done else 'Mark as done' }}">{{ '✓' if t.is_done else '' }}</button></form>
<form class="edit" method="post" action="{{ url_for('todo_edit', todo_id=t.todo_id) }}">{{ errors_box(row_errors.get(t.todo_id, [])) }}
<div class="row"><input type="text" name="title" value="{{ row_values.get(t.todo_id, t.title) }}" required maxlength="200" pattern=".*\S.*"><button class="btn btn-small">Save</button></div></form>
<a class="btn btn-danger btn-small" href="{{ url_for('todo_delete', todo_id=t.todo_id) }}">Delete</a></li>{% endfor %}</ul>
{% else %}<p class="empty">Nothing to do yet. Add your first to-do above.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["library.html"] = r"""{% extends "base.html" %}{% block title %}Library Management{% endblock %}{% block content %}
<section class="card"><div class="section-head"><h1>Books</h1><a class="btn btn-small" href="{{ url_for('book_new') }}">Add book</a></div>
<p class="muted">Use the Search books and Catalogue pages in the navigation to explore the Lab 4 features.</p>
{% if books %}<div class="table-wrap"><table><thead><tr><th>ID</th><th>Title</th><th>Price</th><th>Author ID</th><th>Author</th><th></th></tr></thead><tbody>
{% for b in books %}<tr><td>{{ b.book_id }}</td><td>{{ b.title }}</td><td>{{ '%.2f'|format(b.price) }}</td><td>{{ b.author_id }}</td><td>{{ names.get(b.author_id, '') }}</td>
<td class="actions"><a class="btn btn-outline btn-small" href="{{ url_for('book_edit', book_id=b.book_id) }}">Edit</a>
<a class="btn btn-danger btn-small" href="{{ url_for('book_delete', book_id=b.book_id) }}">Delete</a></td></tr>{% endfor %}</tbody></table></div>
{% else %}<p class="empty">No books yet.</p>{% endif %}</section>
<section class="card"><div class="section-head"><h1>Authors</h1><a class="btn btn-small" href="{{ url_for('author_new') }}">Add author</a></div>
{% if authors %}<div class="table-wrap"><table><thead><tr><th>ID</th><th>Name</th><th>Country</th><th></th></tr></thead><tbody>
{% for a in authors %}<tr><td>{{ a.author_id }}</td><td>{{ a.name }}</td><td>{{ a.country }}</td><td class="actions">
<a class="btn btn-outline btn-small" href="{{ url_for('author_edit', author_id=a.author_id) }}">Edit</a>
<a class="btn btn-danger btn-small" href="{{ url_for('author_delete', author_id=a.author_id) }}">Delete</a></td></tr>{% endfor %}</tbody></table></div>
{% else %}<p class="empty">No authors yet.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["author_form.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}{{ 'Edit author' if author_id else 'Add author' }}{% endblock %}{% block content %}
<section class="card narrow"><h1>{{ 'Edit author' if author_id else 'Add author' }}</h1><form method="post">{{ errors_box(errors) }}
<label>Name<input type="text" name="name" value="{{ form.get('name', '') }}" required maxlength="100" pattern=".*\S.*"></label>
<label>Country<input type="text" name="country" value="{{ form.get('country', '') }}" required maxlength="50" pattern=".*\S.*"></label>
<div class="row"><button class="btn">Save author</button><a class="btn btn-outline" href="{{ url_for('library') }}">Cancel</a></div></form></section>{% endblock %}"""

TEMPLATES["book_form.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}{{ 'Edit book' if book_id else 'Add book' }}{% endblock %}{% block content %}
<section class="card narrow"><h1>{{ 'Edit book' if book_id else 'Add book' }}</h1>
{% if not authors or not publishers or not categories %}
<p class="empty">Add at least one author, publisher and category before adding a book.</p>
{% else %}
<form method="post">{{ errors_box(errors) }}
<label>Title<input type="text" name="title" value="{{ form.get('title', '') }}" required maxlength="200" pattern=".*\S.*"></label>
<label>Price<input type="number" name="price" value="{{ form.get('price', '') }}" required min="0" step="0.01"></label>
<label>Publish year<input type="number" name="publish_year" value="{{ form.get('publish_year', '') }}" required min="1000" max="2155"></label>
<label>Author<select name="author_id" required><option value="">Choose an author</option>
{% for a in authors %}<option value="{{ a.author_id }}"{% if form.get('author_id', '')|string == a.author_id|string %} selected{% endif %}>{{ a.name }}</option>{% endfor %}</select></label>
<label>Publisher<select name="publisher_id" required><option value="">Choose a publisher</option>
{% for p in publishers %}<option value="{{ p.publisher_id }}"{% if form.get('publisher_id', '')|string == p.publisher_id|string %} selected{% endif %}>{{ p.name }}</option>{% endfor %}</select></label>
<label>Category<select name="category_id" required><option value="">Choose a category</option>
{% for c in categories %}<option value="{{ c.category_id }}"{% if form.get('category_id', '')|string == c.category_id|string %} selected{% endif %}>{{ c.name }}</option>{% endfor %}</select></label>
<div class="row"><button class="btn">Save book</button><a class="btn btn-outline" href="{{ url_for('library') }}">Cancel</a></div></form>
{% endif %}</section>{% endblock %}"""

TEMPLATES["book_search.html"] = r"""{% extends "base.html" %}{% from "_macros.html" import errors_box %}
{% block title %}Search books{% endblock %}{% block content %}
<section class="card"><h1>F2.1 – Search books</h1>
<p class="muted">Search by title keyword, price range, and one or more categories. Leave a field empty to ignore that filter.</p>
<form method="post" action="{{ url_for('book_search') }}">{{ errors_box(errors) }}
<div class="filter-grid">
<label>Title keyword<input type="text" name="keyword" value="{{ form.keyword }}" placeholder="Enter part of a title"></label>
<label>Minimum price<input type="number" name="min_price" value="{{ form.min_price }}" min="0" step="0.01"></label>
<label>Maximum price<input type="number" name="max_price" value="{{ form.max_price }}" min="0" step="0.01"></label>
<label>Categories <select name="category_ids" multiple>
{% for c in categories %}<option value="{{ c.category_id }}"{% if c.category_id|string in form.category_ids %} selected{% endif %}>{{ c.name }}</option>{% endfor %}
</select><span class="muted">Hold Ctrl (Windows) to select multiple categories.</span></label>
</div><button class="btn">Search</button> <a class="btn btn-outline" href="{{ url_for('book_search') }}">Clear</a></form></section>
{% if searched and not errors %}<section class="card"><h2>Search results</h2>
{% if books %}<p class="results-count">{{ books|length }} matching book(s), cheapest first.</p><div class="table-wrap"><table>
<thead><tr><th>Title</th><th>Price</th><th>Year</th><th>Author</th><th>Category</th></tr></thead><tbody>
{% for b in books %}<tr><td>{{ b.title }}</td><td>{{ '%.2f'|format(b.price) }}</td><td>{{ b.publish_year }}</td><td>{{ b.author_name }}</td><td>{{ b.category_name }}</td></tr>{% endfor %}
</tbody></table></div>{% else %}<p class="empty">No books match your search.</p>{% endif %}</section>{% endif %}
{% endblock %}"""

TEMPLATES["catalogue.html"] = r"""{% extends "base.html" %}{% block title %}Catalogue{% endblock %}{% block content %}
<section class="card"><h1>F2.2 – Book catalogue</h1>{% if books %}<div class="table-wrap"><table>
<thead><tr><th>Book</th><th>Price</th><th>Publish year</th><th>Author</th><th>Publisher</th><th>Category</th></tr></thead><tbody>
{% for b in books %}<tr><td>{{ b.title }}</td><td>{{ '%.2f'|format(b.price) }}</td><td>{{ b.publish_year }}</td><td>{{ b.author_name }}</td><td>{{ b.publisher_name }}</td><td>{{ b.category_name }}</td></tr>{% endfor %}
</tbody></table></div>{% else %}<p class="empty">No books found.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["reports.html"] = r"""{% extends "base.html" %}{% block title %}Library reports{% endblock %}{% block content %}
<section class="card"><h1>F2.3 – Reports</h1><h2>(a) Books and average price per category</h2>
{% if category_stats %}<div class="table-wrap"><table><thead><tr><th>Category</th><th>Number of books</th><th>Average price</th></tr></thead><tbody>
{% for r in category_stats %}<tr><td>{{ r.category_name }}</td><td>{{ r.book_count }}</td><td>{% if r.average_price is not none %}{{ '%.2f'|format(r.average_price) }}{% else %}N/A{% endif %}</td></tr>{% endfor %}
</tbody></table></div>{% endif %}
<h2>(b) Authors who wrote at least 2 books</h2>{% if prolific_authors %}<table><thead><tr><th>Author</th><th>Books written</th></tr></thead><tbody>
{% for a in prolific_authors %}<tr><td>{{ a.name }}</td><td>{{ a.book_count }}</td></tr>{% endfor %}</tbody></table>{% else %}<p class="empty">No author has written at least two books.</p>{% endif %}
<h2>(c) Whole-library price summary</h2><table><tbody><tr><th>Total price</th><td>{% if price_summary.total_price is not none %}{{ '%.2f'|format(price_summary.total_price) }}{% else %}N/A{% endif %}</td></tr>
<tr><th>Smallest price</th><td>{% if price_summary.smallest_price is not none %}{{ '%.2f'|format(price_summary.smallest_price) }}{% else %}N/A{% endif %}</td></tr>
<tr><th>Largest price</th><td>{% if price_summary.largest_price is not none %}{{ '%.2f'|format(price_summary.largest_price) }}{% else %}N/A{% endif %}</td></tr></tbody></table></section>{% endblock %}"""

TEMPLATES["loans_report.html"] = r"""{% extends "base.html" %}{% block title %}Loans report{% endblock %}{% block content %}
<section class="card"><h1>F2.4 – Loans</h1><h2>(a) Loans not returned yet</h2>
{% if unreturned %}<table><thead><tr><th>Loan ID</th><th>Book</th><th>Member</th><th>Loan date</th></tr></thead><tbody>
{% for l in unreturned %}<tr><td>{{ l.loan_id }}</td><td>{{ l.book_title }}</td><td>{{ l.member_name }}</td><td>{{ l.loan_date }}</td></tr>{% endfor %}</tbody></table>
{% else %}<p class="empty">There are no active loans.</p>{% endif %}
<h2>(b) Members who never borrowed a book</h2>{% if members_without_loans %}<table><thead><tr><th>Member</th><th>Email</th></tr></thead><tbody>
{% for m in members_without_loans %}<tr><td>{{ m.name }}</td><td>{{ m.email }}</td></tr>{% endfor %}</tbody></table>{% else %}<p class="empty">Every member has at least one loan.</p>{% endif %}
<h2>(c) Books that were never borrowed</h2>{% if books_never_borrowed %}<table><thead><tr><th>Book</th></tr></thead><tbody>
{% for b in books_never_borrowed %}<tr><td>{{ b.title }}</td></tr>{% endfor %}</tbody></table>{% else %}<p class="empty">Every book has been borrowed.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["most_borrowed.html"] = r"""{% extends "base.html" %}{% block title %}Most borrowed{% endblock %}{% block content %}
<section class="card"><h1>F2.5 – Most borrowed</h1><h2>Top 3 books</h2>
{% if top_books %}<table><thead><tr><th>Rank</th><th>Book</th><th>Number of loans</th></tr></thead><tbody>
{% for b in top_books %}<tr><td>{{ loop.index }}</td><td>{{ b.title }}</td><td>{{ b.loan_count }}</td></tr>{% endfor %}</tbody></table>{% else %}<p class="empty">There are no loans yet.</p>{% endif %}
<h2>Member with the most loans</h2>{% if top_member %}<p><strong>{{ top_member.name }}</strong> – {{ top_member.loan_count }} loan(s).</p>{% else %}<p class="empty">There are no member loans yet.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["authors_books.html"] = r"""{% extends "base.html" %}{% block title %}Authors and books{% endblock %}{% block content %}
<section class="card"><h1>F2.6 – Authors and books</h1><h2>(a) Every author and number of books, including zero</h2>
{% if author_counts %}<table><thead><tr><th>Author</th><th>Country</th><th>Number of books</th></tr></thead><tbody>
{% for a in author_counts %}<tr><td>{{ a.name }}</td><td>{{ a.country }}</td><td>{{ a.book_count }}</td></tr>{% endfor %}</tbody></table>{% endif %}
<h2>(b) Books whose author and publisher are from the same country</h2>{% if same_country_books %}<table><thead><tr><th>Book</th><th>Author</th><th>Publisher</th><th>Country</th></tr></thead><tbody>
{% for b in same_country_books %}<tr><td>{{ b.title }}</td><td>{{ b.author_name }}</td><td>{{ b.publisher_name }}</td><td>{{ b.country }}</td></tr>{% endfor %}</tbody></table>
{% else %}<p class="empty">No matching books found.</p>{% endif %}</section>{% endblock %}"""

TEMPLATES["confirm.html"] = r"""{% extends "base.html" %}{% block title %}Are you sure?{% endblock %}{% block content %}
<section class="card narrow"><h1>Are you sure?</h1><p>{{ message }}</p><form method="post" class="row">
<button class="btn btn-danger">Yes, delete</button><a class="btn btn-outline" href="{{ cancel_url }}">Cancel</a></form></section>{% endblock %}"""

TEMPLATES["error.html"] = r"""{% extends "base.html" %}{% block title %}Error {{ code }}{% endblock %}{% block content %}
<section class="card narrow"><h1>{{ code }}</h1><p>{{ message }}</p><a class="btn" href="{{ url_for('index') }}">Back to the site</a></section>{% endblock %}"""
