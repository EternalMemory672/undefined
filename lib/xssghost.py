# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.relative_locator import *
import time
import sys


class Xssreport:
    InjectionPoint = ""
    XSStype = ""
    InjectPosition = ""
    Payload = ""

    def __init__(self) -> None:
        pass

    def __init__(self, point, xsstype, payload, hint="[*] No hint about this."):
        self.InjectionPoint = point
        self.InjectPosition = hint
        self.XSStype = xsstype
        self.Payload = payload


class Xsstask:
    url = ""
    submits = []
    report = []

    def __init__(self) -> None:
        pass

    def __init__(self):
        pass


def aftersubmit(driver):
    try:
        alert = WebDriverWait(driver, 0.00001).until(
            expected_conditions.alert_is_present())
        print(alert.text)
        if alert.text.find("XSS") != -1:
            alert.accept()
            return True
        else:
            alert.accept()
            return False
    except:
        return False


def phadsys():
    if sys.platform.startswith('win'):
        return "./thirdparty/chrome/chromedriver-win.exe"
    elif sys.platform.startswith('linux'):
        return "./thirdparty/chrome/chromedriver-linux"
    else:
        print("unsupportable system")
        sys.exit(0)


def dvwasetsecurity(driver, security):
    driver.get(driver.current_url[:-9]+"security.php")
    select = Select(driver.find_element(
        By.XPATH, "//select[@name='security']"))
    select.select_by_visible_text(security)
    driver.find_element(By.XPATH, "//input[@name='seclev_submit']").click()


def dvwalogin(driver):
    username = "admin"
    password = "password"
    inputers = driver.find_elements(By.XPATH, "//input")
    for inpu in inputers[:]:
        nowtype = inpu.get_attribute("type")
        if nowtype == "hidden":
            pass
        elif nowtype == "text" or nowtype == "password":
            if inpu.get_attribute("name") == "username":
                inpu.send_keys(username)
            elif inpu.get_attribute("name") == "password":
                inpu.send_keys(password+Keys.ENTER)
                break


def attkdvwa(driver, securitynum=0):
    url = driver.current_url[:-9]
    dictionary = open("./wordlists/attack/XSS.txt", mode="r")
    payload = dictionary.readlines()

    dvwalogin(driver)
    security = ["Low", "Medium", "High", "Impossible"]
    XSStarget = ["vulnerabilities/xss_r/", "vulnerabilities/xss_s/"]
    dvwasetsecurity(driver, security[securitynum])
    for xsstarget in XSStarget:
        driver.get(url+xsstarget)

        for nowpayload in payload:
            print(nowpayload[:-1])

            submitbtn = driver.find_element(
                By.XPATH, "//input[@type='submit']")
            try:
                inputs=driver.find_elements(with_tag_name("input").above(submitbtn))
                inputs.extend(driver.find_elements(with_tag_name("input").near(submitbtn)))
                inputs.extend(driver.find_elements(with_tag_name("textarea").above(submitbtn)))
            except:
                pass
            for inpu in inputs:
                print(len(inputs))
                print(inpu.get_attribute("type"))
                if inpu.get_attribute("type")=="text" or inpu.get_attribute("type")=="password" or inpu.tag_name=="textarea":
                    inpu.send_keys(nowpayload[:-1])
            submitbtn.click()

            if aftersubmit(driver):

                print('??????URL:  "'+url+xsstarget+'"')
                print("XSS??????????????????")
                print('PAYLOAD = "'+nowpayload[:-1]+'"')
                try:
                    submitbtn = driver.find_element(
                        By.XPATH, "//input[@type='submit']")
                    text = driver.find_element(
                        with_tag_name("p").near(submitbtn)).text
                    print('??????????????? "'+text+'" ??????')
                except:
                    print("????????????????????????????????????")
                finally:
                    print()
                    break


def driver_settings():
    chrome_opt = webdriver.ChromeOptions()

    # chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--disable-gpu')
    chrome_opt.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29"')
    chrome_opt.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_opt.add_experimental_option("useAutomationExtension", 'False')
    return chrome_opt


def main():
    server = Service(phadsys())
    target = []
    submitbtn = []
    payload = "test"
    Ourl = 'http://10.122.232.130:81/'
    driver = webdriver.Chrome(service=server, options=driver_settings())
    driver.implicitly_wait(10)

    driver.get(Ourl)
    title = driver.title

    if title.find("DVWA") != -1:
        attkdvwa(driver)
    else:
        print("Not DVWA")
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
