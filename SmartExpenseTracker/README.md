# 智能个人记账助手 (SmartExpenseTracker)

命令行个人记账工具，支持收支记录、分类统计、月度报表生成、异常消费提醒。

## 项目简介

本项目是2026年春季学期计算机科学与技术专业综合实践项目。使用Python实现一个完整的命令行记账系统，涵盖OOP、数据结构、正则表达式、文件操作、SQLite数据库和matplotlib可视化等核心技术。

## 环境要求

- Python 3.8+
- 依赖安装：

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

## 功能特性

### 基本功能
- ✅ 收支记录管理（增删改查）
- ✅ 命令行菜单交互系统
- ✅ 日期和金额格式的正则校验
- ✅ JSON文件数据持久化
- ✅ SQLite数据库存储
- ✅ 月度收支饼图（分类占比）
- ✅ 月度收支趋势折线图

### 加分项
- ⭐ 异常消费检测：基于历史均值自动标记异常消费
- ⭐ 自然语言记账：输入"昨天午饭花了35元"自动解析

## 项目结构

```
SmartExpenseTracker/
├── main.py              # 程序入口 + 菜单交互
├── models.py            # OOP核心类 (Expense, Category, User)
├── validators.py        # 正则校验 + 自然语言解析
├── storage.py           # JSON文件读写
├── database.py          # SQLite数据库操作
├── charts.py            # matplotlib可视化
├── config.py            # 全局常量配置
├── requirements.txt     # 项目依赖
├── data/                # 数据存储目录
│   └── expenses.json    # 默认数据文件
└── charts_output/       # 图表输出目录
```

## 功能截图

（运行后补充截图）

## 作者

- rainy256 - OOP设计、菜单交互、异常消费检测
- [队友姓名] - SQLite数据库、matplotlib可视化、自然语言记账解析

## 技术栈

- Python 3.x
- matplotlib (数据可视化)
- SQLite3 (数据库)
- 正则表达式 (输入校验)
- JSON/CSV (文件操作)
