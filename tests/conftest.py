"""
Pytest 配置和 fixture 定义
"""
import pytest
from utils.driver_factory import DriverFactory
import allure,time

# fixture：每个测试函数运行前，创建一个新的浏览器实例(function = 每个测试函数都独立)
@pytest.fixture(scope="function")
def driver():
    """浏览器驱动 fixture"""
    factory = DriverFactory()
    page = factory.get_page()

    # yield：把 page 对象交给测试用例使用
    yield page

    # 测试用例结束后执行：如果用例失败，自动截图
    if hasattr(page, '_test_failed') and page._test_failed:
        screenshot_path = f"screenshots/failed_{int(time.time())}.png"
        page.screenshot(path=screenshot_path)
        # 把截图附加到 Allure 报告中
        allure.attach.file(
            screenshot_path,
            name="失败截图",
            attachment_type=allure.attachment_type.PNG
        )

    # 关闭浏览器
    factory.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子函数：在每条用例执行完毕后调用
    用于检测用例是否失败，并在 page 对象上标记
    """
    # yield：暂停钩子函数，让 pytest 继续执行测试用例
    outcome = yield
    # 获取测试报告对象 rep
    rep = outcome.get_result()
    # 保存报告到测试用例
    # item：当前测试用例对象
    # rep.when：执行阶段，可以是 "setup"、"call"、"teardown"
    # setattr(item, "rep_call", rep)：相当于 item.rep_call = rep
    setattr(item, "rep_" + rep.when, rep)

    # 如果用例执行阶段失败（call 阶段），标记 page._test_failed = True
    if rep.when == "call" and rep.failed:
        # item.funcargs：测试用例中所有 fixture 参数的字典
        # 获取名为 driver 的 fixture 值（即 WebDriver 对象）
        page = item.funcargs.get("driver", None)
        if page is not None:
            page._test_failed = True