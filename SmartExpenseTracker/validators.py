"""
正则表达式校验模块
校验日期格式、金额格式、解析自然语言输入
"""

import re
from datetime import date, timedelta


def validate_date(date_str):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_str))


def validate_amount(amount_str):
    pattern = r"^-?\d+(\.\d{1,2})?$"
    return bool(re.match(pattern, amount_str))


def parse_natural_input(text):
    """
    解析自然语言记账输入
    示例:
        "昨天午饭花了35元" -> ("2026-05-12", "餐饮", 35, "expense")
        "今天工资收入8000" -> ("2026-05-13", "工资", 8000, "income")
        "前天理发50" -> ("2026-05-11", "理发", 50, "expense")
    """
    today = date.today()

    relative_dates = {
        "今天": today,
        "昨天": today - timedelta(days=1),
        "前天": today - timedelta(days=2),
        "大前天": today - timedelta(days=3),
    }

    parsed_date = str(today)
    for word, d in relative_dates.items():
        if word in text:
            parsed_date = str(d)
            break

    date_pattern = r"(\d{1,2})月(\d{1,2})[日号]"
    m = re.search(date_pattern, text)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        parsed_date = f"{today.year}-{month:02d}-{day:02d}"

    amount_pattern = r"(\d+(?:\.\d{1,2})?)\s*(?:元|块|块钱|万)"
    amount_match = re.search(amount_pattern, text)
    if not amount_match:
        bare_pattern = r"(?:花了|收入|赚了?|消费|用了|付了?|支出|到账)\s*(\d+(?:\.\d{1,2})?)(?:\s|$)"
        amount_match = re.search(bare_pattern, text)
    if not amount_match:
        standalone = re.search(r"(\d+(?:\.\d{1,2})?)\s*$", text)
        if standalone:
            amount_match = standalone
    amount = float(amount_match.group(1)) if amount_match else 0

    expense_type = "expense"
    income_keywords = ["收入", "工资", "奖金", "报销", "入账", "收到", "赚"]
    for kw in income_keywords:
        if kw in text:
            expense_type = "income"
            break

    category_map = {
        "吃饭": "餐饮", "午饭": "餐饮", "晚饭": "餐饮", "早餐": "餐饮", "外卖": "餐饮",
        "饭": "餐饮", "聚餐": "餐饮", "零食": "餐饮", "喝": "餐饮",
        "地铁": "交通", "公交": "交通", "打车": "交通", "加油": "交通", "停车": "交通",
        "衣服": "购物", "买": "购物", "淘宝": "购物", "京东": "购物",
        "游戏": "娱乐", "电影": "娱乐", "KTV": "娱乐", "旅游": "娱乐",
        "房租": "居住", "水电": "居住", "物业": "居住",
        "医院": "医疗", "药": "医疗",
        "书": "教育", "课程": "教育", "培训": "教育",
        "理发": "其他", "工资": "工资", "奖金": "工资", "报销": "工资",
    }
    category = "其他"
    for kw, cat in category_map.items():
        if kw in text:
            category = cat
            break

    return parsed_date, category, amount, expense_type


def parse_user_input(text):
    result = parse_natural_input(text)
    if result[2] > 0:
        return result
    return None


if __name__ == "__main__":
    tests = [
        "昨天午饭花了35元",
        "今天工资收入8000",
        "前天理发50",
        "5月10日买衣服花了299",
        "打车30块"
    ]
    for t in tests:
        r = parse_natural_input(t)
        print(f"输入: {t}")
        print(f"  -> 日期:{r[0]} 分类:{r[1]} 金额:{r[2]} 类型:{r[3]}")
        print()
