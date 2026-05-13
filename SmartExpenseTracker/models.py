"""
智能个人记账助手 - 核心数据模型
Expense: 单笔收支记录
Category: 消费分类
User: 用户（管理所有财务数据）
"""

import json
from datetime import datetime


class Category:
    def __init__(self, name, budget_limit=0):
        self.name = name
        self.budget_limit = budget_limit
        self.icon = "📌"

    def set_budget(self, limit):
        self.budget_limit = limit

    def check_over_budget(self, amount):
        if self.budget_limit <= 0:
            return False
        return amount > self.budget_limit

    def to_dict(self):
        return {
            "name": self.name,
            "budget_limit": self.budget_limit
        }

    @staticmethod
    def from_dict(data):
        return Category(data["name"], data.get("budget_limit", 0))


class Expense:
    _id_counter = 0

    def __init__(self, amount, category, date, note="", expense_type="expense"):
        Expense._id_counter += 1
        self.id = Expense._id_counter
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.note = note
        self.type = expense_type

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note,
            "type": self.type
        }

    @staticmethod
    def from_dict(data):
        expense = Expense(
            data["amount"],
            data["category"],
            data["date"],
            data.get("note", ""),
            data.get("type", "expense")
        )
        expense.id = data.get("id", 0)
        expense.type = data.get("type", "expense")
        return expense

    @staticmethod
    def set_id_counter(value):
        Expense._id_counter = value

    @staticmethod
    def get_id_counter():
        return Expense._id_counter


class User:
    def __init__(self, username="默认用户"):
        self.username = username
        self.categories = {}
        self.expenses = []

    def add_category(self, category):
        self.categories[category.name] = category

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, expense_id):
        self.expenses = [e for e in self.expenses if e.id != expense_id]

    def get_monthly_summary(self, year, month):
        month_str = f"{year}-{month:02d}"
        total_income = sum(e.amount for e in self.expenses
                          if e.type == "income" and e.date.startswith(month_str))
        total_expense = sum(e.amount for e in self.expenses
                           if e.type == "expense" and e.date.startswith(month_str))
        return {
            "year": year,
            "month": month,
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense,
            "count": len([e for e in self.expenses if e.date.startswith(month_str)])
        }

    def get_category_stats(self, year, month):
        month_str = f"{year}-{month:02d}"
        stats = {}
        for e in self.expenses:
            if e.type == "expense" and e.date.startswith(month_str):
                cat = e.category if e.category else "其他"
                stats[cat] = stats.get(cat, 0) + e.amount
        return stats

    def get_all_expenses_by_date(self, year=None, month=None):
        result = self.expenses
        if year:
            year_str = str(year)
            result = [e for e in result if e.date.startswith(year_str)]
        if month:
            month_str = f"{month:02d}"
            result = [e for e in result if len(e.date) >= 7 and e.date[5:7] == month_str]
        return sorted(result, key=lambda e: e.date, reverse=True)

    def to_dict(self):
        return {
            "username": self.username,
            "categories": {k: v.to_dict() for k, v in self.categories.items()},
            "expenses": [e.to_dict() for e in self.expenses]
        }

    @staticmethod
    def from_dict(data):
        user = User(data.get("username", "默认用户"))
        user.categories = {
            k: Category.from_dict(v) for k, v in data.get("categories", {}).items()
        }
        max_id = 0
        for e_data in data.get("expenses", []):
            exp = Expense.from_dict(e_data)
            user.expenses.append(exp)
            if exp.id > max_id:
                max_id = exp.id
        Expense.set_id_counter(max_id)
        return user

    def get_category_budget_status(self, year, month):
        stats = self.get_category_stats(year, month)
        status = {}
        for cat_name, amount in stats.items():
            cat = self.categories.get(cat_name)
            limit = cat.budget_limit if cat else 0
            status[cat_name] = {
                "spent": amount,
                "limit": limit,
                "over": limit > 0 and amount > limit,
                "percentage": round(amount / limit * 100, 1) if limit > 0 else 0
            }
        return status
