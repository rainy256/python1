"""
JSON文件数据持久化模块
负责将User对象序列化到JSON文件，以及从JSON文件反序列化
"""

import json
import os
from models import User, Expense


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def save_to_json(user, filepath):
    """
    将User对象保存为JSON文件
    """
    full_path = filepath if os.path.isabs(filepath) else os.path.join(DATA_DIR, os.path.basename(filepath))
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(user.to_dict(), f, ensure_ascii=False, indent=2)
    return full_path


def load_from_json(filepath):
    """
    从JSON文件加载User对象
    如果文件不存在，返回一个新User
    """
    full_path = filepath if os.path.isabs(filepath) else os.path.join(DATA_DIR, os.path.basename(filepath))
    if not os.path.exists(full_path):
        return User()
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return User.from_dict(data)


def export_to_csv(user, filepath):
    """
    将账单数据导出为CSV文件
    """
    import csv
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "日期", "分类", "金额", "类型", "备注"])
        for e in user.expenses:
            writer.writerow([e.id, e.date, e.category, e.amount, e.type, e.note])
