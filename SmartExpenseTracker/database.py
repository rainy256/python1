"""
SQLite数据库操作模块
提供交易记录的增删改查功能
"""

import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "expenses.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT DEFAULT '',
            type TEXT NOT NULL DEFAULT 'expense',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            budget_limit REAL NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def insert_expense_db(expense):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note, type) VALUES (?, ?, ?, ?, ?)",
        (expense.amount, expense.category, expense.date, expense.note, expense.type)
    )
    conn.commit()
    conn.close()


def get_all_expenses_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_month_expenses_db(year, month):
    month_str = f"{year}-{month:02d}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC",
        (f"{month_str}%",)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_category_totals_db(year, month):
    month_str = f"{year}-{month:02d}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? AND type='expense' GROUP BY category",
        (f"{month_str}%",)
    )
    rows = cursor.fetchall()
    conn.close()
    return {row["category"]: row["total"] for row in rows}


def delete_expense_db(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def set_budget_db(category, limit):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO budgets (category, budget_limit) VALUES (?, ?)",
        (category, limit)
    )
    conn.commit()
    conn.close()


def get_budgets_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budgets")
    rows = cursor.fetchall()
    conn.close()
    return {row["category"]: row["budget_limit"] for row in rows}


if __name__ == "__main__":
    init_db()
    print("数据库初始化完成:", DB_PATH)
