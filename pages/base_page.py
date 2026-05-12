"""
BasePage 基类
封装通用的页面操作方法
"""
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        # 每个页面对象都持有一个 page（浏览器标签页）
        self.page = page
        self.timeout = 10000

    def navigate_to(self, url: str):
        """打开指定 URL"""
        self.page.goto(url)

    def wait_for_element(self, selector: str, timeout: int = None):
        """等待元素可见"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def click(self, selector, timeout=None):
        """点击元素，先等待元素可见，再等待元素可点击（解决遮挡或未完全加载的问题）"""
        timeout = timeout or self.timeout
        # 第一步：等待元素在页面上可见
        # self.wait_for_element(selector, timeout)
        # 第二步：等待元素处于可点击状态（已启用、未被遮挡）
        element = self.page.locator(selector)
        # wait_for 默认 state="visible"，确保元素在 DOM 中且可见
        element.wait_for(state="visible", timeout=timeout)
        element.click()  # Playwright 的 locator.click() 内部会自动等待可点击

    def fill(self, selector: str, text: str, timeout: int = None):
        """在输入框中填写文本"""
        self.wait_for_element(selector, timeout)
        self.page.fill(selector, text)

    def get_text(self, selector: str, timeout: int = None):
        """获取元素对应文本"""
        self.wait_for_element(selector, timeout)
        return self.page.text_content(selector).strip()

    def is_visible(self, selector: str, timeout: int = None):
        """检查元素是否可见"""
        timeout = timeout or 3000
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False

    def select_option(self, selector: str, value: str = None, label: str = None):
        """定位下拉框元素"""
        self.wait_for_element(selector)
        if value:
            self.page.select_option(selector, value=value)
        elif label:
            self.page.select_option(selector, label=label)