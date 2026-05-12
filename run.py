"""
项目入口文件：一键运行测试并输出 Allure 原始数据
使用方法：python run.py
查看报告：allure serve ./reports
"""

import pytest
import os
import shutil

if __name__ == '__main__':
    # ========== 第1步：清空上次的测试数据 ==========
    # reports/ 目录存放 Allure 原始数据（JSON、TXT 等中间文件）
    report_dir = './reports'

    # 如果 reports 文件夹已存在，递归删除里面的所有文件和子文件夹
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)

    # 重新创建一个空的 reports 文件夹
    os.makedirs(report_dir)

    # ========== 第2步：保留 .gitkeep 文件 ==========
    # 确保空目录也能被 Git 追踪
    with open(os.path.join(report_dir, '.gitkeep'), 'w', encoding='utf-8') as f:
        pass  # 不写入任何内容，只创建一个空文件

    # ========== 第3步：运行 Pytest 测试 ==========
    # -v：详细模式，终端显示每条用例的名称和 PASSED/FAILED 状态
    # --alluredir=./reports：测试结果保存到 reports/ 目录
    # --capture=no：不截获控制台输出，方便调试时看到 print 和 log
    pytest.main([
        '-v',
        '--alluredir=./reports',
        '--capture=no',
        './tests/'
    ])

    # ========== 第4步：提示用户如何查看报告 ==========
    print("\n 测试完成！运行以下命令查看 Allure 报告：")
    print("   allure serve ./reports")