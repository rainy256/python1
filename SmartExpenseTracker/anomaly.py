"""
异常消费检测模块
基于历史均值自动标记异常消费
"""

from datetime import date


def detect_anomaly(user, year=None, month=None, threshold=2.0):
    """
    检测指定月份的异常消费
    返回异常列表，每项包含: category, current, average, ratio, months_count
    """
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month

    current_stats = user.get_category_stats(year, month)
    if not current_stats:
        return []

    warnings = []
    for cat_name, current_amount in current_stats.items():
        historical = []
        for offset in range(1, 4):
            m = month - offset
            y = year
            if m <= 0:
                m += 12
                y -= 1
            stats = user.get_category_stats(y, m)
            historical.append(stats.get(cat_name, 0))

        months_with_data = sum(1 for h in historical if h > 0)
        avg_history = sum(historical) / months_with_data if months_with_data > 0 else 0

        if months_with_data >= 2 and avg_history > 0 and current_amount > avg_history * threshold:
            warnings.append({
                "category": cat_name,
                "current": current_amount,
                "average": round(avg_history, 2),
                "ratio": round(current_amount / avg_history, 1),
                "months_count": months_with_data
            })

    return sorted(warnings, key=lambda w: w["ratio"], reverse=True)


def detect_new_spike(user, year=None, month=None, min_amount=200):
    """
    检测之前几乎没有记录、本月突然大额的消费
    返回新异常列表
    """
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month

    current_stats = user.get_category_stats(year, month)
    if not current_stats:
        return []

    new_warnings = []
    for cat_name, current_amount in current_stats.items():
        if current_amount < min_amount:
            continue

        historical_total = 0
        for offset in range(1, 4):
            m = month - offset
            y = year
            if m <= 0:
                m += 12
                y -= 1
            stats = user.get_category_stats(y, m)
            historical_total += stats.get(cat_name, 0)

        if historical_total == 0:
            new_warnings.append({
                "category": cat_name,
                "current": current_amount,
                "type": "new_spike",
                "message": f"新增大额消费: {cat_name}"
            })

    return new_warnings


def run_anomaly_check(user):
    """
    综合检测：均值异常 + 新增大额
    返回 (anomalies, new_spikes)
    """
    today = date.today()
    anomalies = detect_anomaly(user, today.year, today.month, threshold=2.0)
    new_spikes = detect_new_spike(user, today.year, today.month, min_amount=200)
    return anomalies, new_spikes


def print_anomaly_report(user):
    """
    打印完整的异常消费报告
    返回是否有异常
    """
    anomalies, new_spikes = run_anomaly_check(user)
    has_anomaly = False

    if anomalies or new_spikes:
        print("\n" + "=" * 45)
        print("  ⚠️  消费异常检测报告")
        print("=" * 45)

    if anomalies:
        has_anomaly = True
        print("\n📊 基于历史均值的异常消费:")
        print(f"  {'分类':<8} {'本月消费':>10}  {'历史均值':>10}  {'超出倍数':>10}")
        print("  " + "-" * 42)
        for w in anomalies:
            print(f"  {w['category']:<8} {w['current']:>10.2f}  {w['average']:>10.2f}  {w['ratio']:>9.1f}x")
            print(f"    → 近{w['months_count']}个月均消费{w['average']}元，本月消费大幅超出！")

    if new_spikes:
        has_anomaly = True
        print("\n🆕 新增大额消费提醒:")
        for s in new_spikes:
            print(f"  {s['category']}: 本月消费{s['current']:.2f}元，前3个月无此分类记录")

    if has_anomaly:
        print("=" * 45)

    return has_anomaly


if __name__ == "__main__":
    from models import User, Expense, Category

    u = User("测试用户")
    u.add_category(Category("餐饮"))
    u.add_category(Category("购物"))
    u.add_category(Category("娱乐"))

    for m in range(1, 6):
        u.add_expense(Expense(40, "餐饮", f"2026-{m:02d}-05", "午餐"))
        u.add_expense(Expense(30, "餐饮", f"2026-{m:02d}-10", "晚餐"))
        u.add_expense(Expense(80, "购物", f"2026-{m:02d}-15", "日用品"))

    u.add_expense(Expense(500, "购物", "2026-05-13", "大额异常消费"))
    u.add_expense(Expense(300, "娱乐", "2026-05-14", "突然看电影"))

    from datetime import date
    a, n = run_anomaly_check(u)
    print("=== 均值异常 ===")
    for w in a:
        print(w)
    print("\n=== 新增大额 ===")
    for s in n:
        print(s)
    print()
    print_anomaly_report(u)
