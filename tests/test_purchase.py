"""
端到端测试：注册 → 搜索商品 → 加入购物车 → 结算
支持多用户数据驱动
"""
import allure
import pytest
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.cart_page import CartPage
from config.env import config


@allure.feature("OpenCart 购物流程")
class TestPurchaseFlow:

    @allure.title("完整端到端：注册 -> 搜索 HTC Touch HD -> 下单成功")
    # 参数化：从 config 里读取用户列表，每个用户跑一次
    @pytest.mark.parametrize(
        "user_data",
        config['user'],
        ids=[f"用户{u['last_name']}" for u in config['user']]
        # ids 会在终端显示"用户三"、"用户四"、"用户五"
    )
    def test_complete_purchase_e2e(self, driver, user_data):
        # 1. 打开首页，导航到注册页
        home = HomePage(driver)
        home.go_to()
        home.go_to_register()

        # 2. 用当前用户数据注册（邮箱自动随机生成）
        register = RegisterPage(driver)
        user_email = register.register(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password']
        )
        allure.attach(user_email, name="注册邮箱", attachment_type=allure.attachment_type.TEXT)

        # 3. 等待跳转，若在成功页则点"继续"
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

        # 8. 点击"结账"
        checkout = cart.click_checkout()

        # 9. 完成全部结算流程，传入当前用户的地址数据
        address_data = user_data.get('address', {})
        print(f"传入的地址数据: {address_data}")
        checkout.complete_checkout(address_data)

        # 10. 最终断言
        assert checkout.is_order_placed(), "订单应该成功放置！"