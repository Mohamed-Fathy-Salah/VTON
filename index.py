import time
import email
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.binary_location = "/../../usr/bin/google-chrome"
driver = webdriver.Chrome(
    executable_path="/../../usr/bin/chromedriver", options=chrome_options)

#email and password
email = "ahmadyasser2814@gmail.com"
password = "zQ.!2Ac_#E-wM8!"

# login
driver.get('https://www.zara.com/eg/en/logon?forward')
# driver.delete_all_cookies()
email_element = driver.find_element_by_name('logonId')
email_element.send_keys(email)

email_element = driver.find_element_by_name('password')
email_element.send_keys(password)

time.sleep(2)

login_button = driver.find_element_by_xpath(
    '//*[@id="main"]/article/div/div[2]/div[1]/section/form/div[2]/button')
login_button.click()

time.sleep(2)

# GO TO PRODUCT

driver.get(
    'https://www.zara.com/eg/en/knit-colour-block-t-shirt-p03284407.html?v1=148602456&v2=2032069')


find_mysize_button = driver.find_element_by_xpath(
    '//*[@id="product-detail-size-selector-product-detail-product-size-selector-148602456-menu"]/div/div/button[1]')

driver.implicitly_wait(10)  # seconds
find_mysize_button.click()


driver.implicitly_wait(10)  # seconds


def input_data(w, h):
    height = driver.find_element_by_id('uclw_form_height')
    height.send_keys(0)
    height.send_keys(h)
    weight = driver.find_element_by_id('uclw_form_weight')
    weight.clear()
    time.sleep(2)
    weight.send_keys(w)
    time.sleep(2)
    fit_pereferences = driver.find_element_by_xpath(
        '//*[@id="uclw_block_fit"]/div[2]/div[2]/div[3]')
    fit_pereferences.click()
    fit_pereferences.click()
    fit_pereferences.click()
    # driver.execute_script(
    #     "document.getElementsByClassName('uclw_noUi-origin uclw_noUi-connect')[2].style.left = '100%'")
    # time.sleep(2)
    find_size = driver.find_element_by_xpath(
        '//*[@id="uclw_save_info_button"]')
    find_size.click()

# Get Results


def get_results():
    result_labels = driver.find_elements_by_class_name('uclw_label')
    time.sleep(2)
    print(result_labels[0].text, driver.find_elements(
        By.CLASS_NAME, 'uclw_bar_right')[0].get_attribute("textContent"))
    print(result_labels[1].text, driver.find_elements(
        By.CLASS_NAME, 'uclw_bar_right')[1].get_attribute("textContent"))


try:
    input_data()
    time.sleep(2)
    get_results()
except:
    start_over = driver.find_element_by_xpath(
        '//*[@id="uclw_animate_results"]/div[4]/div')
    start_over.click()
    time.sleep(2)
    input_data()
    time.sleep(2)
    get_results()


'''
login

loop
Read from csv
output to csv


'''
