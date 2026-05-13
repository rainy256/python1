"""
智能个人记账助手 - 主程序入口
命令行菜单交互系统
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import User, Expense
from validators import validate_date, validate_amount
from storage import save_to_json, load_from_json
from database import init_db, insert_expense_db, get_all_expenses_db
from charts import plot_category_pie, plot_monthly_trend
from config import DEFAULT_CATEGORIES, DATA_FILE


def print_header():
    print("\n" + "=" * 40)
    print("     智能个人记账助手  SmartExpenseTracker")
    print("=" * 40)


def print_menu():
    print("""
    1. 记一笔账
    2. 查看本月账单
    3. 查看分类统计
    4. 生成月度报表（图表）
    5. 设置分类预算
    6. 数据导出
    0. 退出
    """)


def init_user():
    init_db()
    return load_from_json(DATA_FILE)


def add_expense_flow(user):
    print("\n--- 记一笔账 ---")
    print("1. 支出  2. 收入")
    t = input("请选择类型: ").strip()
    expense_type = "expense" if t == "1" else "income"

    date = input("日期 (YYYY-MM-DD，回车=今天): ").strip()
    if not date:
        from datetime import date as dt
        date = str(dt.today())
    elif not validate_date(date):
        print("日期格式错误！请使用 YYYY-MM-DD 格式")
        return

    amount_str = input("金额: ").strip()
    if not validate_amount(amount_str):
        print("金额格式错误！请输入有效数字")
        return
    amount = float(amount_str)
    if expense_type == "expense":
        amount = abs(amount)
    else:
        amount = abs(amount)

    print("可选分类: " + ", ".join(user.categories.keys()) if user.categories else "无预设分类")
    category = input("分类: ").strip()
    if category and category not in user.categories:
        print(f"新增分类: {category}")

    note = input("备注（可选）: ").strip()

    expense = Expense(amount, category, date, note, expense_type)
    user.add_expense(expense)
    insert_expense_db(expense)
    save_to_json(user, DATA_FILE)
    print(f"✅ 记账成功！{date} {category} {amount}元 ({expense_type})")


def view_monthly_bills(user):
    print("\n--- 本月账单 ---")
    today = __import__("datetime").date.today()
    expenses = user.get_all_expenses_by_date(today.year, today.month)

    if not expenses:
        print("暂无记录")
        return

    print(f"{'日期':<12} {'分类':<8} {'金额':>10}  {'类型':<6}  {'备注'}")
    print("-" * 55)
    for e in expenses:
        type_tag = "收入" if e.type == "income" else "支出"
        print(f"{e.date:<12} {e.category:<8} {e.amount:>10.2f}  {type_tag:<6}  {e.note}")

    summary = user.get_monthly_summary(today.year, today.month)
    print("-" * 55)
    print(f"本月收入: {summary['income']:.2f}  本月支出: {summary['expense']:.2f}  结余: {summary['balance']:.2f}")


def view_category_stats(user):
    print("\n--- 分类统计 ---")
    today = __import__("datetime").date.today()
    stats = user.get_category_stats(today.year, today.month)

    if not stats:
        print("本月暂无支出记录")
        budget_status = {}
    else:
        total = sum(stats.values())
        print(f"\n本月光支出合计: {total:.2f}元")
        print(f"{'分类':<10} {'金额':>10}  {'占比':>8}")
        print("-" * 35)
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for cat, amount in sorted_stats:
            pct = amount / total * 100
            print(f"{cat:<10} {amount:>10.2f}  {pct:>7.1f}%")
        budget_status = user.get_category_budget_status(today.year, today.month)

    print("\n--- 预算执行情况 ---")
    has_budget = False
    for cat_name, cat in user.categories.items():
        if cat.budget_limit > 0:
            has_budget = True
            bs = budget_status.get(cat_name, {"spent": 0, "limit": cat.budget_limit, "over": False, "percentage": 0})
            status = "⚠️ 超支!" if bs["over"] else "✅ 正常"
            bar = "█" * int(min(bs["percentage"] / 10, 10))
            print(f"{cat_name:<10} {bs['spent']:>8.2f}/{cat.budget_limit:.0f} [{bar:<10}] {status}")
    if not has_budget:
        print("未设置任何分类预算，请在菜单5中设置")


def generate_report(user):
    print("\n--- 生成月度报表 ---")
    today = __import__("datetime").date.today()
    year_str = input(f"年份 (回车={today.year}): ").strip()
    month_str = input(f"月份 (回车={today.month}): ").strip()
    year = int(year_str) if year_str else today.year
    month = int(month_str) if month_str else today.month

    print("1. 饼图（分类占比）  2. 折线图（月度趋势）  3. 两者都生成")
    choice = input("请选择: ").strip()

    if choice in ("1", "3"):
        plot_category_pie(user, year, month)
    if choice in ("2", "3"):
        plot_monthly_trend(user, year)


def set_budget(user):
    print("\n--- 设置分类预算 ---")
    if not user.categories:
        print("暂无分类，请先在记账时添加分类")

    for name, cat in user.categories.items():
        current = cat.budget_limit if cat.budget_limit > 0 else "未设置"
        print(f"  {name}: 当前预算 = {current}")

    cat_name = input("要设置预算的分类名: ").strip()
    if cat_name not in user.categories:
        print(f"分类 '{cat_name}' 不存在")
        return

    try:
        limit = float(input("预算金额: ").strip())
    except ValueError:
        print("请输入有效数字")
        return

    user.categories[cat_name].set_budget(limit)
    save_to_json(user, DATA_FILE)
    print(f"✅ {cat_name} 月度预算已设为 {limit:.2f}元")


def export_data(user):
    print("\n--- 数据导出 ---")
    print("1. 导出为 JSON  2. 导出为 CSV")
    choice = input("请选择: ").strip()

    if choice == "1":
        save_to_json(user, "export.json")
        print("✅ 已导出到 export.json")
    elif choice == "2":
        import csv
        with open("export.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "日期", "分类", "金额", "类型", "备注"])
            for e in user.expenses:
                writer.writerow([e.id, e.date, e.category, e.amount, e.type, e.note])
        print("✅ 已导出到 export.csv")
    else:
        print("无效选择")


def main():
    user = init_user()
    for cat in DEFAULT_CATEGORIES:
        if cat not in user.categories:
            from models import Category
            user.add_category(Category(cat))

    while True:
        print_header()
        print_menu()
        choice = input("请选择操作: ").strip()

        if choice == "1":
            add_expense_flow(user)
        elif choice == "2":
            view_monthly_bills(user)
        elif choice == "3":
            view_category_stats(user)
        elif choice == "4":
            generate_report(user)
        elif choice == "5":
            set_budget(user)
        elif choice == "6":
            export_data(user)
        elif choice == "0":
            print("\n再见！")
            break
        else:
            print("无效选择，请重新输入")

        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
