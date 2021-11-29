# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import sys


def phadsys():
    if sys.platform.startswith('win'):
        return "./thirdparty/chrome/chromedriver-win.exe"
    elif sys.platform.startswith('linux'):
        return "./thirdparty/chrome/chromedriver-linux"
    else:
        print("unsupportable system")
        sys.exit(0)

def dvwasetsecurity(driver,security):
    driver.get(driver.current_url[:-9]+"security.php")
    select =Select(driver.find_element(By.XPATH,"//select[@name='security']"))
    select.select_by_visible_text(security)
    driver.find_element(By.XPATH,"//input[@name='seclev_submit']").click()


def dvwalogin(driver):
    username="admin"
    password="password"
    inputers = driver.find_elements(By.XPATH,"//input")
    for inpu in inputers[:]:
        nowtype = inpu.get_attribute("type")
        if nowtype == "hidden":
            pass
        elif nowtype == "text" or nowtype == "password":
            if inpu.get_attribute("name")=="username":
                inpu.send_keys(username)
            elif inpu.get_attribute("name")=="password":
                inpu.send_keys(password+Keys.ENTER)
                break

def attkdvwa(driver):
    dvwalogin(driver)
    security=["Low","Medium","High","Impossible"]
    dvwasetsecurity(driver,security[0])     

def driver_settings():
    chrome_opt = webdriver.ChromeOptions()

    # chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--disable-gpu')
    chrome_opt.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29"')
    chrome_opt.add_experimental_option("excludeSwitches",["enable-automation"])
    chrome_opt.add_experimental_option("useAutomationExtension",'False')
    return chrome_opt


def main():
    server = Service(phadsys())
    target = []
    submitbtn = []
    payload="test"
    Ourl = 'http://10.122.232.130:81/'
    driver = webdriver.Chrome(service=server, options=driver_settings())
    driver.implicitly_wait(10)

    driver.get(Ourl)
    title=driver.title

    if title.find("DVWA"):
        attkdvwa(driver)
    else:
        print("不是DVWA")
    # inputers = driver.find_elements(By.XPATH,"//input")
    # for inpu in inputers[:]:
    #     nowtype = inpu.get_attribute("type")
    #     if nowtype == "hidden":
    #         inputers.remove(inpu)
    #     elif nowtype == "text" or nowtype == "password":
    #         target.append(inpu)
    #     elif nowtype == "submit":
    #         submitbtn.append(inpu)

    # for attck in target:
    #     attck.send_keys(payload)
    # target[-1].send_keys(Keys.ENTER)
    # for inpu in submitbtn:
    #     print(inpu.get_attribute("type"))

    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()
