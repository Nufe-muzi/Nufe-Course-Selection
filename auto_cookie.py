from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
import os
import sys
from selenium import webdriver
# =======================================
# 这个函数用来方便打包不报错的
def get_executable_directory():
    # 获取当前执行的 .exe 文件的路径
    if getattr(sys, 'frozen', False):
        # 如果程序是通过 PyInstaller 打包的
        executable_path = sys.executable
    else:
        # 如果是普通的 Python 脚本
        executable_path = os.path.abspath(__file__)
    
    # 获取 .exe 文件所在的目录
    executable_directory = os.path.dirname(executable_path)
    
    return executable_directory
# ===========================================
# 启动 WebDriver（这里以 Chrome 为例）
def get_cookie(username,password):
    # chrome_driver_path = resource_path(os.path.join('chrome-win64', 'chromedriver.exe'))
    exe_directory = get_executable_directory()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 无界面模式
    # chrome_options.add_argument('--disable-gpu')  # 禁用 GPU 加速
    chrome_driver_path = os.path.join(exe_directory, 'chrome-win64', 'chromedriver.exe')
    # chrome_driver_path = '/chrome-win64/chromedriver.exe'  # 将此路径替换为你的实际 chromedriver 路径

    # 使用 Service 类来启动 WebDriver
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    # 打开登录页面
    driver.get('https://jwxt.nufe.edu.cn/student/sso/login')
    time.sleep(3)
    # 输入用户名和密码
    username_box = driver.find_element(By.NAME, 'username')  # 定位用户名输入框
    password_box = driver.find_element(By.ID, 'password')  # 定位密码输入框

    username_box.send_keys(username)  # 替换为你的实际用户名
    password_box.send_keys(password)  # 替换为你的实际密码

    # 模拟点击登录按钮
    login_button = driver.find_element(By.ID, 'login_submit')  # 找到登录按钮的元素
    login_button.click()

    # 等待页面加载
    time.sleep(3)

    # 获取登录后的 Cookie
    driver.get('https://jwxt.nufe.edu.cn/student/for-std/course-select')
    time.sleep(3)

    cookies = driver.get_cookies()
    return cookies[0].get('value')
