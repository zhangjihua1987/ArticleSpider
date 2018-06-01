from selenium import webdriver
from scrapy.selector import Selector


browser = webdriver.Edge(executable_path='E:/temp/MicrosoftWebDriver.exe')
# browser.get('https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.19.5b0b2a68YdfcBu&id=566605082411&skuId=3643811076933&user_id=2838892713&cat_id=2&is_b=1&rn=7369366e2cc5da70e8f90ade996c802f')
#
# t_selector = Selector(text=browser.page_source)
# price = t_selector.css('div.tm-promo-price span.tm-price::text').extract()
# print(price)
browser.get('https://www.zhihu.com/signup?next=%2F')
browser.find_element_by_css_selector('div.SignContainer-switch span').click()
browser.find_element_by_css_selector('input[name="username"]').send_keys('13730897717')
browser.find_element_by_css_selector('input[name="password"]').send_keys('xuecheng871144')
browser.find_element_by_css_selector('button.SignFlow-submitButton').click()

# browser.quit()
