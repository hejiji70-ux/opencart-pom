"""
用户注册页
"""
from pages.base_page import BasePage
import random, time

class RegisterPage(BasePage):
    # 定位器：注册表单的每个输入框
    FIRST_NAME_INPUT = "#input-firstname"
    LAST_NAME_INPUT = "#input-lastname"
    EMAIL_INPUT = "#input-email"
    # TELEPHONE_INPUT = "#input-telephone"
    PASSWORD_INPUT = "#input-password"
    # PASSWORD_CONFIRM_INPUT = "#input-confirm"
    PRIVACY_CHECKBOX = "input[name='agree']"
    CONTINUE_BTN = "button[type='submit']"

    def __init__(self, page):
        super().__init__(page)

    def register(self, first_name: str, last_name: str, email: str = None, password: str = "123456", telephone: str = "13800138000"):
        """填写注册表单，返回注册邮箱"""
        # 如果没有指定邮箱，生成一个唯一的随机邮箱（避免重复注册报错）
        if email is None:
            random_num = random.randint(1000, 9999)
            timestamp = int(time.time())
            # 例如：test1746951234999@example.com
            email = f"test{timestamp}{random_num}@example.com"
        # 逐字段填写
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        # self.fill(self.TELEPHONE_INPUT, telephone)
        self.fill(self.PASSWORD_INPUT, password)
        # self.fill(self.PASSWORD_CONFIRM_INPUT, password)
        # 勾选隐私政策（必须勾才能继续）
        self.click(self.PRIVACY_CHECKBOX)
        # 点击"Continue"提交
        self.click(self.CONTINUE_BTN)
        # 返回用于确认邮箱（方便后续的邮箱登录或验证）
        return email