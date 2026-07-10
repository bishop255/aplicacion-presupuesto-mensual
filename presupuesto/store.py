import sqlite3
from datetime import date

from .constants import DEFAULT_FIXED_EXPENSES, DEFAULT_INCOME, DEFAULT_SAVINGS_PERCENT
from .utils import month_key, short_month_label


class BudgetStore:
    """Capa de datos: crea tablas, guarda movimientos y calcula resumenes."""

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.setup()
        self.seed()

    def setup(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS months (
                month TEXT PRIMARY KEY,
                income INTEGER NOT NULL DEFAULT 0,
                savings_percent REAL NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS fixed_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount INTEGER NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS fixed_payments (
                month TEXT NOT NULL,
                template_id INTEGER NOT NULL,
                paid_amount INTEGER NOT NULL DEFAULT 0,
                paid_date TEXT,
                notes TEXT,
                PRIMARY KEY (month, template_id),
                FOREIGN KEY(template_id) REFERENCES fixed_templates(id)
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                spent_on TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Ocio',
                description TEXT NOT NULL,
                amount INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                saved_on TEXT NOT NULL,
                description TEXT NOT NULL,
                amount INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        self.conn.commit()

    def seed(self):
        count = self.conn.execute("SELECT COUNT(*) FROM fixed_templates").fetchone()[0]
        if count == 0:
            self.conn.executemany(
                "INSERT INTO fixed_templates (name, amount) VALUES (?, ?)",
                DEFAULT_FIXED_EXPENSES,
            )
        self.ensure_month(month_key())
        self.conn.commit()

    def ensure_month(self, key):
        previous = self.conn.execute(
            "SELECT income, savings_percent FROM months ORDER BY month DESC LIMIT 1"
        ).fetchone()
        income = previous["income"] if previous else DEFAULT_INCOME
        percent = previous["savings_percent"] if previous else DEFAULT_SAVINGS_PERCENT
        self.conn.execute(
            "INSERT OR IGNORE INTO months (month, income, savings_percent) VALUES (?, ?, ?)",
            (key, income, percent),
        )
        self.conn.commit()

    def months(self):
        rows = self.conn.execute("SELECT month FROM months ORDER BY month DESC").fetchall()
        return [row["month"] for row in rows]

    def month_settings(self, key):
        self.ensure_month(key)
        return self.conn.execute("SELECT * FROM months WHERE month = ?", (key,)).fetchone()

    def save_month_settings(self, key, income, savings_percent):
        self.ensure_month(key)
        self.conn.execute(
            "UPDATE months SET income = ?, savings_percent = ? WHERE month = ?",
            (income, savings_percent, key),
        )
        self.conn.commit()

    def fixed_rows(self, key):
        self.ensure_month(key)
        return self.conn.execute(
            """
            SELECT
                t.id,
                t.name,
                t.amount,
                COALESCE(p.paid_amount, 0) AS paid_amount,
                p.paid_date,
                COALESCE(p.notes, '') AS notes
            FROM fixed_templates t
            LEFT JOIN fixed_payments p ON p.template_id = t.id AND p.month = ?
            WHERE t.active = 1
            ORDER BY t.name
            """,
            (key,),
        ).fetchall()

    def add_fixed_template(self, name, amount):
        self.conn.execute("INSERT INTO fixed_templates (name, amount) VALUES (?, ?)", (name, amount))
        self.conn.commit()

    def edit_fixed_template(self, template_id, name, amount):
        self.conn.execute(
            "UPDATE fixed_templates SET name = ?, amount = ? WHERE id = ?",
            (name, amount, template_id),
        )
        self.conn.commit()

    def deactivate_fixed_template(self, template_id):
        self.conn.execute("UPDATE fixed_templates SET active = 0 WHERE id = ?", (template_id,))
        self.conn.commit()

    def set_fixed_payment(self, key, template_id, amount, paid_date=None, notes=""):
        paid_date = paid_date or date.today().isoformat()
        self.conn.execute(
            """
            INSERT INTO fixed_payments (month, template_id, paid_amount, paid_date, notes)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(month, template_id) DO UPDATE SET
                paid_amount = excluded.paid_amount,
                paid_date = excluded.paid_date,
                notes = excluded.notes
            """,
            (key, template_id, amount, paid_date, notes),
        )
        self.conn.commit()

    def clear_fixed_payment(self, key, template_id):
        self.conn.execute(
            "DELETE FROM fixed_payments WHERE month = ? AND template_id = ?",
            (key, template_id),
        )
        self.conn.commit()

    def expenses(self, key):
        return self.conn.execute(
            "SELECT * FROM expenses WHERE month = ? ORDER BY spent_on DESC, id DESC", (key,)
        ).fetchall()

    def add_expense(self, key, spent_on, category, description, amount):
        self.conn.execute(
            """
            INSERT INTO expenses (month, spent_on, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (key, spent_on, category, description, amount),
        )
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    def savings(self, key):
        return self.conn.execute(
            "SELECT * FROM savings WHERE month = ? ORDER BY saved_on DESC, id DESC", (key,)
        ).fetchall()

    def add_saving(self, key, saved_on, description, amount):
        self.conn.execute(
            "INSERT INTO savings (month, saved_on, description, amount) VALUES (?, ?, ?, ?)",
            (key, saved_on, description, amount),
        )
        self.conn.commit()

    def delete_saving(self, saving_id):
        self.conn.execute("DELETE FROM savings WHERE id = ?", (saving_id,))
        self.conn.commit()

    def summary(self, key):
        settings = self.month_settings(key)
        fixed = self.fixed_rows(key)
        income = settings["income"]
        savings_target = income * settings["savings_percent"] / 100
        fixed_planned = sum(row["amount"] for row in fixed)
        fixed_paid = sum(row["paid_amount"] for row in fixed)
        leisure = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE month = ?", (key,)
        ).fetchone()[0]
        saved = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM savings WHERE month = ?", (key,)
        ).fetchone()[0]
        return {
            "income": income,
            "savings_percent": settings["savings_percent"],
            "savings_target": savings_target,
            "fixed_planned": fixed_planned,
            "fixed_paid": fixed_paid,
            "leisure": leisure,
            "saved": saved,
            "cash_remaining": income - fixed_paid - leisure - saved,
            "planned_remaining": income - fixed_planned - savings_target - leisure,
        }

    def annual_savings(self, year):
        rows = []
        total_saved = 0
        total_target = 0
        for month in range(1, 13):
            key = f"{year:04d}-{month:02d}"
            settings = self.conn.execute(
                "SELECT income, savings_percent FROM months WHERE month = ?", (key,)
            ).fetchone()
            saved = self.conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM savings WHERE month = ?", (key,)
            ).fetchone()[0]
            target = 0
            if settings:
                target = settings["income"] * settings["savings_percent"] / 100
            total_saved += saved
            total_target += target
            rows.append({"month": month, "label": short_month_label(month), "saved": saved, "target": target})
        return {"year": year, "rows": rows, "total_saved": total_saved, "total_target": total_target}

