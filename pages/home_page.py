"""
首页
"""
from pages.base_page import BasePage
from config.env import config

class HomePage(BasePage):
    # 中文界面的定位器
    MY_ACCOUNT_BTN = "// span[contains(text(),'My Account')]"   # 顶部导航的"我的账户"
    REGISTER_LINK = "//a[contains(text(),'Register')]"          # 下拉菜单里的"注册"链接
    SEARCH_INPUT = "input[name='search']"                       # 搜索框
    SEARCH_BTN = "//button[@class='btn']"                       # 搜索按钮

    def __init__(self, page):
        # 调用父类 BasePage 的 __init__，把 page 传进去
        super().__init__(page)

    def go_to(self):
        """打开首页"""
        self.navigate_to(config['base_url'])

    def go_to_register(self):
        """点击我的账户，再点击注册然后跳转到用户注册页"""
        self.click(self.MY_ACCOUNT_BTN)        # 继承自 BasePage 的 click 方法
        self.click(self.REGISTER_LINK)

    def search_product(self, product_name: str):
        """搜索商品，并返回搜索结果页对象"""
        self.fill(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BTN)
        # 返回一个 SearchPage 对象，方便链式调用（可以继续接着进行后续操作）
        from pages.search_page import SearchPage
        return SearchPage(self.page)