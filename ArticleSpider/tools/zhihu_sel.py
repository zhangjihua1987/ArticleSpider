from selenium import webdriver
from http import cookiejar
import requests


session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')


try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie加载错误')


def login(username, password):
    browser = webdriver.Edge(executable_path='E:/temp/MicrosoftWebDriver.exe')
    browser.get('https://www.zhihu.com/signup?next=%2F')

    # 利用selenium模拟操作登录
    # 使用selenium的css选择器选择登录时所需要的操作的元素并进行操作
    browser.find_element_by_css_selector('div.SignContainer-switch span').click()
    browser.find_element_by_css_selector('input[name="username"]').send_keys(username)
    browser.find_element_by_css_selector('input[name="password"]').send_keys(password)
    browser.find_element_by_css_selector('button.SignFlow-submitButton').click()

    # 登陆后等待10秒获取cookies
    import time
    time.sleep(10)
    cookies = browser.get_cookies()
    cookie_dict = dict()

    # 将遍历cookies的信息并dump到本地
    import pickle
    for cookie in cookies:
        with open('E:/spider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb') as f:
            pickle.dump(cookie, f)

        # 将cookies的信息放到cookie_dict中
        cookie_dict[cookie['name']] = cookie['value']
    browser.close()
    return cookie_dict


def is_login():
    try_url = 'https://www.zhihu.com/settings/profile'
    response = session.get(url=try_url)
    pass


if __name__ == '__main__':
    login('13730897717', 'xuecheng871144')
