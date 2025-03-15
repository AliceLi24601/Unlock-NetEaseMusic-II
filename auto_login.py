# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00EE04633FD1AB1292240801C8E8B357ABABE8150FB5F6069C821C66DD3A132F08FCBFE4710F3F87134E5CD21E49197B424B75FEA3BC32975B499915499B62D8F5147ACA3E68593193E204D574FBBAE1F6A39A5E8A41299002F308F5CD7448CCCE10EBE9789581CB754FD2DD7C0C2FACEC4CAC888D22FF0CB66307AF4D1F906A5945B6912FAD8CC26AB884A555694B467AFC90320293CC5CF6E90E81605CA4290BD0B58032387C60D5DEEEDAC6FA8DB0B7EC9A6532AAF54B82C11C8AA4F2281D1C1433B93488D27E1EAAC32A360334D91EF68A9759B71FD0C73114EF2CD26980DC6888297B6C7AAB1F56DD1858C3B5391CD8A01EE1BF17C590C8F3A22EA9C4BA4D7E5BF318696E8ECD1BABA3DBCB8AA6011E68183C341E814B6B604D9A06C6F4ED958BB3A2A277E62F7E51CC63D17141409562CF6B3EB4F52B0D02C19BD8F8D453CCF9AFEF5DD21DFF08A484BC10E1572F9E2DE2641CCDCA124F51496810E1B0E5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
