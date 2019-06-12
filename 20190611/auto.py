from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import quote
from PIL import Image, ImageEnhance
import pytesseract
import time

"""
自动集成测试   
"""


def get_auth_code(driver, codeEelement):
    '''获取验证码'''
    driver.save_screenshot('login.png')  # 截取登录页面
    imgSize = codeEelement.size  # 获取验证码图片的大小
    imgLocation = codeEelement.location  # 获取验证码元素坐标
    rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
              int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
    login = Image.open("login.png")
    frame4 = login.crop(rangle)  # 截取验证码图片
    frame4.save('authcode.png')
    authcodeImg = Image.open('authcode.png')
    # enh_bri = ImageEnhance.Brightness(authcodeImg)
    # image_brightrned = enh_bri.enhance(1.5)
    # enh_con = ImageEnhance.Contrast(authcodeImg)
    # image_contrasted = enh_con.enhance(1.5)
    # # 锐度增强
    # enh_sha = ImageEnhance.Sharpness(authcodeImg)
    # image_sharped = enh_sha.enhance(3.0)
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText


def pandarola_login(driver, account, passwd, authCode):
    '''登录pandarola系统'''
    driver.find_element_by_id('username').send_keys(account)
    driver.find_element_by_id('password').send_keys(passwd)
    driver.find_element_by_id('captcha').send_keys(authCode)
    button = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[2]/form/div[4]/div/div/div/div/span/div/div/div/span/button')
    button.click()
    time.sleep(2)
    # title = driver.find_element_by_id('menuName-h').text  # 获取登录的标题
    # '''验证是否登录成功'''
    # try:
    #     assert title == u'桌面'
    #     return '登录成功'
    # except AssertionError as e:
    #     return '登录失败'
    return 'success'


if __name__ == '__main__':
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get(url='http://10.1.5.23:16016/#/welcome-page')
    imgElement = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[2]/form/div[3]/div/div/div/div/div/span/div/img')
    authCodeText = get_auth_code(driver, imgElement)
    authCodeText =input('请更据下载下来的图片输入验证码:')
    pandarola_login(driver, 'admin', '123456a.', authCodeText)
