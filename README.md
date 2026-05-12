# OpenCart 电商系统 Web 自动化测试 (POM 模式)

## 项目简介
基于 Python + Playwright + Pytest + Allure 的 OpenCart 电商系统 UI 自动化测试框架。
采用 Page Object Model 设计模式，实现测试逻辑与页面元素的分离，覆盖注册、搜索、购物车、结算全链路。

## 技术栈
- **Python 3.11**
- **Playwright**：浏览器自动化
- **Pytest**：测试框架 + fixture
- **Allure**：可视化测试报告
- **PyAutoGUI**：辅助窗口最大化（解决特定视口遮挡问题）
- **GitHub Actions**：持续集成

## 项目结构
opencart_pom/
├── pages/                  # 页面对象层 (POM)
│   ├── base_page.py        # 基类，封装通用操作
│   ├── home_page.py        # 首页
│   ├── register_page.py    # 注册页
│   ├── search_page.py      # 搜索结果页
│   ├── product_page.py     # 商品详情页
│   ├── cart_page.py        # 购物车页
│   └── checkout_page.py    # 结算页（多步骤）
├── tests/                  # 测试用例
│   ├── conftest.py         # fixture，失败截图
│   └── test_purchase.py    # 端到端购物流程
├── utils/                  # 工具类
│   └── driver_factory.py   # 浏览器工厂
├── config/                 # 配置
│   ├── config.yaml.example # 配置模板
│   └── env.py              # 配置加载器
├── reports/                # 测试报告数据
├── videos/                 # 录屏（可选）
├── run.py                  # 一键运行入口
└── requirements.txt

## 快速开始

### 1. 安装依赖
pip install -r requirements.txt
playwright install chromium

### 2. 配置环境
复制 `config/config.yaml.example` 为 `config/config.yaml`，根据需要修改其中值。

### 3. 运行测试
python run.py

### 4. 查看报告
allure serve ./reports

## 测试覆盖
- 端到端购物流程：注册 → 搜索商品 → 加入购物车 → 结算 → 下单成功
- 页面对象模式：封装 7 个页面类，定位器与业务逻辑分离
- 失败自动截图：通过 Pytest 钩子实现用例失败时自动截图

## GitHub Actions 持续集成
本项目配置了 GitHub Actions，推送代码后自动运行测试（需设置 Secret 或直接提交 config.yaml）。
