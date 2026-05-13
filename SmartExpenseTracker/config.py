"""
项目全局常量配置
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATA_FILE = os.path.join(DATA_DIR, "expenses.json")

DB_PATH = os.path.join(DATA_DIR, "expenses.db")

CHART_DIR = os.path.join(BASE_DIR, "charts_output")

DEFAULT_CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "医疗", "教育", "人情", "其他"]

CATEGORY_ICONS = {
    "餐饮": "🍔",
    "交通": "🚇",
    "购物": "🛒",
    "娱乐": "🎮",
    "居住": "🏠",
    "医疗": "💊",
    "教育": "📚",
    "人情": "🎁",
    "其他": "📌"
}
