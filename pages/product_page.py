"""
商品详情页
"""
from pages.base_page import BasePage

class ProductPage(BasePage):
    ADD_TO_CART_BTN = "#button-cart[type='submit']"
    ALERT_SUCCESS = ".alert-success"

    def __init__(self, page):
        super().__init__(page)

    def add_to_cart(self):
        """点击加入购物车，并等待成功提示"""
        self.click(self.ADD_TO_CART_BTN)
        self.wait_for_element(self.ALERT_SUCCESS)