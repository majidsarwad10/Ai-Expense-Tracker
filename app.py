import csv
import io
import os
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Flask, flash, make_response, redirect, render_template, request, url_for

from ai_categorizer import suggest_category
from database import add_expense, delete_expense, get_expense, get_expenses, init_db, update_expense


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development-only-change-me"),
        DATABASE=os.environ.get("DATABASE_PATH", str(Path(app.instance_path) / "expenses.sqlite")),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_db(app)

    @app.get("/")
    def index():
        expenses = get_expenses(app)
        total = sum((Decimal(str(item["amount"])) for item in expenses), Decimal("0"))
        return render_template("index.html", expenses=expenses, total=total)

    @app.post("/expenses")
    def create_expense():
        title = request.form.get("title", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        notes = request.form.get("notes", "").strip()

        if not title or len(title) > 100:
            flash("Enter a description between 1 and 100 characters.", "error")
            return redirect(url_for("index"))

        try:
            amount = Decimal(amount_raw)
            if not amount.is_finite() or amount <= 0 or amount > Decimal("100000000"):
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            flash("Enter a valid positive amount.", "error")
            return redirect(url_for("index"))

        try:
            date.fromisoformat(expense_date)
        except ValueError:
            flash("Choose a valid expense date.", "error")
            return redirect(url_for("index"))

        if not category:
            category = suggest_category(title)

        add_expense(app, title, str(amount.quantize(Decimal("0.01"))), category, expense_date, notes)
        flash("Expense added successfully.", "success")
        return redirect(url_for("index"))

    @app.get("/dashboard")
    def dashboard():
        expenses = get_expenses(app)
        category_totals = {}
        month_totals = {}
        for item in expenses:
            category_totals[item["category"]] = category_totals.get(item["category"], 0) + float(item["amount"])
            month = item["expense_date"][:7]
            month_totals[month] = month_totals.get(month, 0) + float(item["amount"])
        return render_template(
            "dashboard.html",
            category_labels=list(category_totals.keys()),
            category_values=list(category_totals.values()),
            month_labels=sorted(month_totals.keys()),
            month_values=[month_totals[m] for m in sorted(month_totals)],
            expense_count=len(expenses),
        )

    @app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
    def edit_expense(expense_id):
        expense = get_expense(app, expense_id)
        if expense is None:
            flash("Expense not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            amount_raw = request.form.get("amount", "").strip()
            category = request.form.get("category", "").strip()
            expense_date = request.form.get("expense_date", "").strip()
            notes = request.form.get("notes", "").strip()

            try:
                amount = Decimal(amount_raw)
                if not title or len(title) > 100 or not amount.is_finite() or amount <= 0:
                    raise ValueError
                date.fromisoformat(expense_date)
            except (InvalidOperation, ValueError):
                flash("Check the description, amount and date.", "error")
                return render_template("edit_expense.html", expense=expense), 400

            update_expense(app, expense_id, title, str(amount.quantize(Decimal("0.01"))),
                           category or suggest_category(title), expense_date, notes)
            flash("Expense updated.", "success")
            return redirect(url_for("index"))

        return render_template("edit_expense.html", expense=expense)

    @app.post("/expenses/<int:expense_id>/delete")
    def remove_expense(expense_id):
        delete_expense(app, expense_id)
        flash("Expense deleted.", "success")
        return redirect(url_for("index"))

    @app.get("/export")
    def export_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Description", "Amount", "Category", "Date", "Notes"])
        for item in get_expenses(app):
            writer.writerow([item["title"], item["amount"], item["category"],
                             item["expense_date"], item["notes"]])
        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
