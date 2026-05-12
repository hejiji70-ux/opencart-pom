"""
搜索结果页
"""
from pages.base_page import BasePage

class SearchPage(BasePage):
    # 定位器：商品列表中的商品标题链接
    # ".product-thumb h4 a" 是 CSS 选择器，表示取商品缩略图中标题的链接
    PRODUCT_LIST_TITLE = ".product-thumb h4 a" # 商品名称链接

    def __init__(self, page):
        super().__init__(page)

    def click_first_product(self):
        """点击第一个商品，进入详情页"""
        self.click(self.PRODUCT_LIST_TITLE)
        # 跳转后返回 ProductPage 对象（用于后续的链式调用）
        from pages.product_page import ProductPage
        return ProductPage(self.page)

    def click_product_by_name(self, product_name: str):
        """
        根据商品名称点击指定的商品
        例如：click_product_by_name("HTC Touch HD")
        """
        locator = f"//h4/a[contains(text(),'{product_name}')]"
        self.click(locator)
        # 跳转后返回 ProductPage 对象
        from pages.product_page import ProductPage
        return ProductPage(self.page)