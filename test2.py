import time
import email
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np


# CHROME Driver
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.binary_location = "/../../usr/bin/google-chrome"
driver = webdriver.Chrome(
    executable_path="/../../usr/bin/chromedriver", options=chrome_options)

# LOGIN

#email and password
email = "ahmadyasser2814@gmail.com"
password = "zQ.!2Ac_#E-wM8!"

driver.get('https://www.zara.com/eg/en/logon?forward')

email_element = driver.find_element_by_name('logonId')
email_element.send_keys(email)

email_element = driver.find_element_by_name('password')
email_element.send_keys(password)

time.sleep(2)

login_button = driver.find_element_by_xpath(
    '//*[@id="main"]/article/div/div[2]/div[1]/section/form/div[2]/button')
login_button.click()

time.sleep(2)
##########################################
'''
 GO TO PRODUCT 
 INPUT 
 FIND MY SIZE
'''
items = [
    'https://www.zara.com/eg/en/basic-slim-fit-t-shirt-p05584411.html?v1=157954762&v2=2032069',
    'https://www.zara.com/eg/en/basic-heavy-weight-t-shirt-p00526411.html?v1=174103357&v2=2032069',
    'https://www.zara.com/eg/en/knit-colour-block-t-shirt-p03284407.html?v1=148602456&v2=2032069',
    'https://www.zara.com/eg/en/basic-medium-weight-t-shirt-p01887401.html?v1=158099447',
    'https://www.zara.com/eg/en/knit-t-shirt-p04231410.html?v1=169542509&v2=2032069',
    'https://www.zara.com/eg/en/contrast-print-t-shirt-p00495431.html?v1=144410078&v2=2032069',
    'https://www.zara.com/eg/en/geometric-print-technical-t-shirt-p06224421.html?v1=157493299&v2=2032069',
    'https://www.zara.com/eg/en/long-length-t-shirt-p01887420.html?v1=144435377&v2=2032069',
    'https://www.zara.com/eg/en/textured-piqu--polo-shirt-p09240450.html?v1=164457785&v2=2032362',
    'https://www.zara.com/eg/en/basic-slim-fit-t-shirt-p05584340.html?v1=153714218&v2=2032069',
]
users = pd.read_csv('users-dataset.csv')
users_arr = users.to_numpy()

interactions_arr = np.zeros((len(users_arr), 9), dtype=object)


def input_data(h, w, f):
    height = driver.find_element_by_id('uclw_form_height')
    height.clear()
    time.sleep(0.5)
    height.send_keys(h)
    weight = driver.find_element_by_id('uclw_form_weight')
    weight.clear()
    time.sleep(0.5)
    weight.send_keys(w)
    time.sleep(1)
    loose = driver.find_element_by_xpath(
        '//*[@id="uclw_block_fit"]/div[2]/div[2]/div[3]')
    tight = driver.find_element_by_xpath(
        '//*[@id="uclw_block_fit"]/div[2]/div[2]/div[1]')
    if f == 'looser':
        loose.click()
        loose.click()
        loose.click()
    elif f == 'tighter':
        tight.click()
        tight.click()
        tight.click()

    find_size = driver.find_element_by_xpath(
        '//*[@id="uclw_save_info_button"]')
    find_size.click()


def get_results():
    result_labels = driver.find_elements_by_class_name('uclw_label')
    time.sleep(2)
    size1 = result_labels[0].text
    percentage_1 = driver.find_elements(
        By.CLASS_NAME, 'uclw_bar_right')[0].get_attribute("textContent")
    size2 = result_labels[1].text
    percentage_2 = driver.find_elements(
        By.CLASS_NAME, 'uclw_bar_right')[1].get_attribute("textContent")
    return size1, percentage_1, size2, percentage_2


count = 11
while True:
    try:
        for user in range(count, 13):
            count += 1
            # product_id = np.random.randint(0, len(items))
            product_id = 2
            driver.get(items[product_id])
            h = users_arr[user][4]
            w = users_arr[user][5]
            f = users_arr[user][3]
            try:
                find_mysize_button = driver.find_element_by_xpath(
                    '//*[@id="product-detail-size-selector-product-detail-product-size-selector-148602456-menu"]/div/div/button[1]')

                driver.implicitly_wait(10)  # seconds
                find_mysize_button.click()
                input_data(h, w, f)
                time.sleep(2)

            except:
                start_over = driver.find_element_by_xpath(
                    '//*[@id="uclw_animate_results"]/div[4]/div')
                start_over.click()
                time.sleep(2)
                input_data(h, w, f)
                time.sleep(2)
            try:
                size_1, percentage_1, size_2, percentage_2 = get_results()
            except:
                continue

            ############################################
            interactions_arr[users_arr[user][0]-1][1] = product_id
            interactions_arr[users_arr[user][0] -
                             1][2] = users_arr[user][3]  # fit_prefrence
            interactions_arr[users_arr[user][0] -
                             1][0] = users_arr[user][0]  # id
            interactions_arr[users_arr[user][0] -
                             1][3] = users_arr[user][4]  # weight
            interactions_arr[users_arr[user][0] -
                             1][4] = users_arr[user][5]  # height
            interactions_arr[users_arr[user][0]-1][5] = size_1
            interactions_arr[users_arr[user][0]-1][6] = percentage_1
            interactions_arr[users_arr[user][0]-1][7] = size_2
            interactions_arr[users_arr[user][0]-1][8] = percentage_2

            print(f"user {count} finished")

    except:
        continue
    break


interactions = pd.DataFrame(interactions_arr, columns=[
    'user_id', 'product_id', 'fit_preferences', 'weight', 'height', 'size_1', 'presentage_1', 'size_2', 'presentage_2'])
pd.DataFrame.to_csv(interactions, 'interactions-dataset.csv',
                    mode='a', index=False)
