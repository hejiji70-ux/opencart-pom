"""
购物车页
"""
from pages.base_page import BasePage

class CartPage(BasePage):
    CHECKOUT_BTN = "//a[contains(@class, 'btn-primary') and text()='Checkout']"  # Checkout 按钮

    def __init__(self, page):
        super().__init__(page)

    def click_checkout(self):
        """点击结账按钮，进入结算流程"""
        self.click(self.CHECKOUT_BTN)
        # 返回 CheckoutPage对象用于链式调用
        from pages.checkout_page import CheckoutPage
        # self.page 就是把当前浏览器标签页传给结算页面，让结算页面能够继续操作这个标签页
        return CheckoutPage(self.page)