"""
matplotlib可视化模块
生成月度收支饼图和月度趋势折线图
"""

import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use("TkAgg")

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts_output")
os.makedirs(CHART_DIR, exist_ok=True)


def plot_category_pie(user, year, month):
    """
    生成某月按分类的支出饼图
    """
    stats = user.get_category_stats(year, month)
    if not stats:
        print(f"⚠️ {year}年{month}月暂无支出数据，无法生成饼图")
        return

    labels = list(stats.keys())
    sizes = list(stats.values())
    total = sum(sizes)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.cm.Set3(range(len(labels)))

    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=90, pctdistance=0.85
    )

    legend_labels = [f"{l} (¥{s:.0f})" for l, s in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, title="分类", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

    ax.set_title(f"{year}年{month}月 支出分类占比\n合计: ¥{total:.2f}", fontsize=14, fontweight="bold")

    filepath = os.path.join(CHART_DIR, f"pie_{year}_{month:02d}.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ 饼图已保存: {filepath}")


def plot_monthly_trend(user, year):
    """
    生成某年12个月的收入/支出趋势折线图
    """
    months = range(1, 13)
    incomes = []
    expenses = []

    for m in months:
        s = user.get_monthly_summary(year, m)
        incomes.append(s["income"])
        expenses.append(s["expense"])

    month_labels = [f"{m}月" for m in months]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(month_labels, incomes, "o-", color="#2ecc71", linewidth=2, markersize=6, label="收入")
    ax.plot(month_labels, expenses, "o-", color="#e74c3c", linewidth=2, markersize=6, label="支出")

    for i, (inc, exp) in enumerate(zip(incomes, expenses)):
        if inc > 0:
            ax.annotate(f"{inc:.0f}", (month_labels[i], inc), textcoords="offset points",
                       xytext=(0, 10), ha="center", fontsize=8, color="#2ecc71")
        if exp > 0:
            ax.annotate(f"{exp:.0f}", (month_labels[i], exp), textcoords="offset points",
                       xytext=(0, -15), ha="center", fontsize=8, color="#e74c3c")

    ax.set_xlabel("月份", fontsize=12)
    ax.set_ylabel("金额 (元)", fontsize=12)
    ax.set_title(f"{year}年 月度收支趋势", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)

    filepath = os.path.join(CHART_DIR, f"trend_{year}.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ 趋势图已保存: {filepath}")


if __name__ == "__main__":
    from models import User, Expense
    from datetime import date

    u = User("测试用户")
    u.add_expense(Expense(35, "餐饮", "2026-05-01", "午餐"))
    u.add_expense(Expense(50, "餐饮", "2026-05-03", "晚餐"))
    u.add_expense(Expense(20, "交通", "2026-05-02", "地铁"))
    u.add_expense(Expense(200, "购物", "2026-05-05", "T恤"))
    u.add_expense(Expense(100, "娱乐", "2026-05-04", "电影"))

    u.add_expense(Expense(40, "餐饮", "2026-04-03", "午餐"))
    u.add_expense(Expense(30, "交通", "2026-04-05", "打车"))
    u.add_expense(Expense(150, "购物", "2026-04-10", "鞋子"))
    u.add_expense(Expense(5000, "工资", "2026-04-01", "", "income"))

    plot_category_pie(u, 2026, 5)
    plot_monthly_trend(u, 2026)
