import allure
from pages.home_page import HomePage
from pages.register_page import RegisterPage
# from pages.search_page import SearchPage
# from pages.product_page import ProductPage
from pages.cart_page import CartPage
# from pages.checkout_page import CheckoutPage
from config.env import config

@allure.feature("OpenCart 购物流程")
class TestPurchaseFlow:

    @allure.title("完整端到端：注册 -> 搜索 HTC Touch HD -> 下单成功")
    def test_complete_purchase_e2e(self, driver):
        # 1. 打开首页，导航到注册页
        home = HomePage(driver)
        home.go_to()
        home.go_to_register()

        # 2. 用随机邮箱注册新用户
        register = RegisterPage(driver)
        user_email = register.register(
            first_name=config['user']['first_name'],
            last_name=config['user']['last_name'],
            password=config['user']['password']
        )
        # 把返回的邮箱写到了 Allure 测试报告里，方便查看这次注册用了哪个邮箱
        allure.attach(user_email, name="注册邮箱", attachment_type=allure.attachment_type.TEXT)

        # 3. 等待跳转，若在成功页则点“继续”
        driver.wait_for_load_state("networkidle")
        if "account/success" in driver.url:
            driver.click("//a[contains(text(),'Continue')]")

        # 4. 搜索目标商品：HTC Touch HD
        home = HomePage(driver)
        search_page = home.search_product("HTC Touch HD")

        # 5. 点击进入商品详情页（按商品名点击）
        product_page = search_page.click_product_by_name("HTC Touch HD")

        # 6. 加入购物车
        product_page.add_to_cart()

        # 7. 前往购物车页面
        driver.wait_for_load_state("networkidle")
        driver.click("//button[@data-bs-toggle='dropdown']")  # 点击购物车下拉
        driver.click("//a[@class='btn btn-default']")         # 点击 View Cart
        cart = CartPage(driver)

        # 8. 点击“结账”
        checkout = cart.click_checkout()

        # 9. 完成全部结算流程
        checkout.complete_checkout()

        # 10. 最终断言
        assert checkout.is_order_placed(), "订单应该成功放置！"