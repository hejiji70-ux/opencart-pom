"""
结算页（单页模式：智能填写地址 → 选择配送方式 → 选择支付方式 → 确认下单）
"""
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # ===== 步骤区域标题 (确保页面该模块已加载出来)=====
    STEP_SHIPPING = "//legend[contains(text(),'Shipping Address')]"
    STEP_SHIPPING_METHOD = "//legend[contains(text(),'Shipping Method')]"
    STEP_PAYMENT_METHOD = "//legend[contains(text(),'Payment Method')]"

    # ===== 配送地址表单字段 =====
    FIRST_NAME_INPUT = "#input-shipping-firstname"
    LAST_NAME_INPUT = "#input-shipping-lastname"
    COMPANY_INPUT = "#input-shipping-company"
    ADDRESS1_INPUT = "#input-shipping-address-1"
    ADDRESS2_INPUT = "#input-shipping-address-2"
    CITY_INPUT = "#input-shipping-city"
    POSTCODE_INPUT = "#input-shipping-postcode[name='postcode']"
    COUNTRY_SELECT = "#input-shipping-country[name='country_id']"       # 国家下拉框
    REGION_SELECT = "#input-shipping-zone[name='zone_id']"           # 省/州下拉框
    ADDRESS_CONTINUE_BTN = "#button-shipping-address[type='submit']"

    # ===== 配送方式 =====
    SHIPPING_CHOOSE_BTN = "//button[@id='button-shipping-methods']"
    SHIPPING_RADIO = "//input[@type='radio' and @name='shipping_method']"
    SHIPPING_CONTINUE_BTN = "//button[@id='button-shipping-method']"

    # ===== 支付方式 =====
    PAYMENT_CHOOSE_BTN = "//button[@id='button-payment-methods']"
    PAYMENT_RADIO = "//input[@type='radio' and @name='payment_method']"
    PAYMENT_CONTINUE_BTN = "//button[@id='button-payment-method']"

    # ===== "确认订单"操作按钮 =====
    CONFIRM_BTN = "//button[contains(text(),'Confirm Order')]"

    # ===== 成功消息 =====
    SUCCESS_MSG = "//h1[text()='Your order has been placed!']"

    def __init__(self, page):
        super().__init__(page)

    def is_address_filled(self):
        """
        检查配送地址是否已经预填。
        已填的地址会以摘要形式显示，例如：
        "he jc, 222, 333, 444, Aberdeen, United Kingdom"
        可以通过检测页面是否包含 "I want to use an existing address" 这一文本来判断。
        """
        try:
            # 已填地址的页面会显示这个 radio 选项的标签文字
            existing_address_hint = "//label[contains(text(),'I want to use an existing address')]"
            self.page.wait_for_selector(existing_address_hint, state="visible", timeout=5000)
            return True
        except:
            return False

    def fill_shipping_address(self, first_name="张", last_name="三",
                              company="test", address1="测试地址123号",
                              address2="456号", city="广州",
                              postcode="100000"):
        """手动填充完整的配送地址表单"""
        print("检测到地址为空，开始自动填充...")
        self.wait_for_element(self.STEP_SHIPPING, timeout=15000)

        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.COMPANY_INPUT, company)      # 公司选填
        self.fill(self.ADDRESS1_INPUT, address1)
        self.fill(self.ADDRESS2_INPUT, address2)    # 地址二选填
        self.fill(self.CITY_INPUT, city)
        self.fill(self.POSTCODE_INPUT, postcode)

        # 选择国家，触发地区下拉框加载
        # 使用 select_option 方法，根据 value 属性选中 "China" (value="44")
        self.page.select_option(self.COUNTRY_SELECT, value="44")
        self.page.wait_for_load_state("networkidle") # 等待地区下拉框更新（网络请求）

        # 选择省/州，选中第一个可用选项 "Guangdong" (value="689")
        self.page.select_option(self.REGION_SELECT, value="689")
        self.page.wait_for_load_state("networkidle")
        # 点击"Continue"提交表单
        self.page.click(self.ADDRESS_CONTINUE_BTN)

    def select_shipping_method(self):
        """选择配送方式，并确保弹窗关闭。"""
        print("开始选择配送方式...")
        self.wait_for_element(self.STEP_SHIPPING_METHOD, timeout=10000)
        self.click(self.SHIPPING_CHOOSE_BTN)

        # 等待弹窗内的 radio 可见
        shipping_radio = self.page.locator(self.SHIPPING_RADIO)
        shipping_radio.wait_for(state="visible", timeout=5000)
        # 用 check() 确保选中
        shipping_radio.check()
        # 点击 Continue 按钮
        self.page.click(self.SHIPPING_CONTINUE_BTN)
        # 等待配送方式弹窗关闭 (隐藏或脱离)
        self.page.wait_for_selector("#modal-shipping", state="hidden", timeout=10000)

    def select_payment_method(self):
        """选择支付方式，并确保弹窗关闭。"""
        print("开始选择支付方式...")
        self.wait_for_element(self.STEP_PAYMENT_METHOD, timeout=10000)
        self.click(self.PAYMENT_CHOOSE_BTN)
        # 等待弹窗内的 radio 可见
        payment_radio = self.page.locator(self.PAYMENT_RADIO)
        payment_radio.wait_for(state="visible", timeout=5000)
        # 用 check() 确保选中
        payment_radio.check()
        # 点击 Continue 按钮
        self.page.click(self.PAYMENT_CONTINUE_BTN)
        # 等待支付方式弹窗关闭
        self.page.wait_for_selector("#modal-payment", state="hidden", timeout=10000)

    def confirm_order(self):
        """点击确认订单按钮，下单前等待按钮变为可用状态。"""
        print("确认订单...")
        # 等待 "确认订单" 按钮变为可用状态，最多等 15 秒
        # 使用 wait_for_selector 等待一个匹配 "未禁用" 状态的定位器出现
        self.page.wait_for_selector(
            "//button[contains(text(),'Confirm Order') and not(@disabled)]",
            timeout=15000
        )
        # 此时按钮已可用，直接点击
        self.page.click("//button[contains(text(),'Confirm Order')]")

    def complete_checkout(self):
        """完整的结算流程，增加地址表单提交后的等待，解决弹窗问题。"""
        # 步骤1：地址处理
        if not self.is_address_filled():
            self.fill_shipping_address()
            # 【关键】地址表单提交后，页面会刷新配送方式区域，
            # 必须等待网络空闲和配送方式标题重新出现，才能继续操作。
            print("地址填充完成，等待页面更新...")
            self.page.wait_for_load_state("networkidle")
            self.wait_for_element(self.STEP_SHIPPING_METHOD, timeout=15000)
        else:
            print("检测到地址已预填，跳过填充步骤。")
        # 步骤2：选择配送方式（必须在页面完全刷新后）
        self.select_shipping_method()
        # 步骤3：选择支付方式
        self.select_payment_method()
        # 等待页面上的支付方式单选按钮区域稳定下来
        self.page.wait_for_load_state("networkidle")
        # 再次确保支付方式区域的标题可见（表示加载已完成）
        self.wait_for_element(self.STEP_PAYMENT_METHOD, timeout=10000)
        # 步骤4：确认下单
        self.confirm_order()

    def is_order_placed(self) -> bool:
        """验证是否成功下单。"""
        return self.is_visible(self.SUCCESS_MSG, timeout=10000)