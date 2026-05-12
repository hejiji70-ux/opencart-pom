"""
浏览器驱动工厂
封装 Playwright 的启动和关闭，对外提供 page 对象
"""
import time
from playwright.sync_api import sync_playwright
from config.env import config

# 尝试导入 pyautogui，如果未安装则报错后继续（仅用于非无头模式）
try:
    import pyautogui
except ImportError:
    pyautogui = None

class DriverFactory:
    """管理浏览器实例的生命周期"""

    def __init__(self):
        self.playwright = sync_playwright().start()
        headless = config.get('browser_headless', False)

        # 使用启动参数让浏览器窗口尽可能大
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--start-maximized']  # 让浏览器窗口最大化（无效，可能被新版 Chrome/Chromium 忽略了）
        )

        # viewport 设为 None，让页面跟随窗口大小
        self.context = self.browser.new_context(
            viewport=None,  # 不限制视口，跟随窗口（无效，效果显示视口大小并未与浏览器大小相等）
            record_video_dir="videos/" if not headless else None,
        )

        self.page = self.context.new_page()

        # ***如果不是无头模式，用 pyautogui 强制最大化窗口（虽然可能会有被拦截的隐患，但是我只能想到这样做才能跑通了）
        if not headless and pyautogui:
            # 等待几秒确保浏览器窗口已经完全加载并获得焦点
            time.sleep(2)
            try:
                # 模拟按下 Win + 上箭头（Windows 下最大化窗口的快捷键）
                pyautogui.hotkey('win', 'up')
                print("已尝试通过系统快捷键最大化窗口。")
            except Exception as e:
                print(f"pyautogui 操作失败: {e}")

    def get_page(self):
        """返回当前 page 对象，供测试用例和页面对象使用"""
        return self.page

    def quit(self):
        """关闭浏览器上下文、浏览器和 Playwright，释放资源"""
        self.context.close()
        self.browser.close()
        self.playwright.stop()