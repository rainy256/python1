from models import User, Expense, Category
from storage import save_to_json, load_from_json
from database import init_db

init_db()

u = User("测试用户")
u.add_category(Category("餐饮", 1500))
u.add_expense(Expense(35, "餐饮", "2026-05-13", "午餐", "expense"))
u.add_expense(Expense(8000, "工资", "2026-05-10", "五月工资", "income"))

save_to_json(u, "data/expenses.json")
print("JSON保存成功")

u2 = load_from_json("data/expenses.json")
print(f"用户: {u2.username}")
print(f"支出笔数: {len(u2.expenses)}")
print(f"分类数: {len(u2.categories)}")

s = u2.get_monthly_summary(2026, 5)
print(f"5月: 收入{s['income']} 支出{s['expense']} 结余{s['balance']}")

stats = u2.get_category_stats(2026, 5)
print(f"分类统计: {stats}")

print("数据流验证通过")
