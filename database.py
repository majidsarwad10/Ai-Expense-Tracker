import sqlite3
from flask import current_app


SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount TEXT NOT NULL,
    category TEXT NOT NULL,
    expense_date TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(app=None):
    database_path = app.config["DATABASE"] if app else current_app.config["DATABASE"]
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(app):
    with connect(app) as connection:
        connection.executescript(SCHEMA)


def get_expenses(app=None):
    with connect(app) as connection:
        return connection.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()


def get_expense(app, expense_id):
    with connect(app) as connection:
        return connection.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()


def add_expense(app, title, amount, category, expense_date, notes=""):
    with connect(app) as connection:
        connection.execute(
            """INSERT INTO expenses (title, amount, category, expense_date, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (title, amount, category, expense_date, notes),
        )


def update_expense(app, expense_id, title, amount, category, expense_date, notes=""):
    with connect(app) as connection:
        connection.execute(
            """UPDATE expenses
               SET title = ?, amount = ?, category = ?, expense_date = ?, notes = ?
               WHERE id = ?""",
            (title, amount, category, expense_date, notes, expense_id),
        )


def delete_expense(app, expense_id):
    with connect(app) as connection:
        connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
