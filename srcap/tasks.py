from celery import shared_task
from django.core.management.base import BaseCommand
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


@shared_task
def scrapping():
    driver_path = '/usr/local/bin/chromedriver'

    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://app.cosmosid.com/sign-in')
    time.sleep(2)

    close_button = driver.find_element(By.ID, 'new-features-dialog--close')
    close_button.click()

    username_field = driver.find_element(By.ID, 'sign-in-form--email')
    password_field = driver.find_element(By.ID, 'sign-in-form--password')

    username_field.send_keys('demo_estee2@cosmosid.com')
    password_field.send_keys('xyzfg321')
    password_field.send_keys(Keys.RETURN)

    login_button = driver.find_element(By.ID, 'sign-in-form--submit') # Replace with the actual ID

    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(3)
    close_button = driver.find_element(By.ID, 'intro-tour--functional-2-tour--close-button')
    close_button.click()

    wait = WebDriverWait(driver, 10)

    csv_filename = "folder_path.csv"

    csv_header = [["path", "folder_name"]]


    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_header)

    for i in range(1,5):

        links = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[{i}]//td[2]//a")))

        root_folder_name = 'srcap/scrapy_data/' + str(links.text) + '/'

        os.makedirs(root_folder_name, exist_ok=True)

        links.click()
        time.sleep(3)

        table = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody")  # or use another selector

        rows = table.find_elements(By.TAG_NAME, 'tr')
        for i in range(1,len(rows)+1):

            links = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[{i}]//td[2]//a")))

            links_text = links.text

            folder_name = root_folder_name + str(links_text) + '/'
            os.makedirs(folder_name, exist_ok=True)

            csv_data = [os.getcwd() + '/' + folder_name, links_text]

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csv_data)

            links.click()
            time.sleep(2)

            buttons = driver.find_elements(By.TAG_NAME, 'button')

            for button in buttons:
                if button.text == 'Taxonomy switcher':
                    print('button =============== ')
                    button.click()
                    break

            time.sleep(2)

            buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if button.text == 'Taxonomy switcher':
                    print('button =============== ')
                    button.click()
                    break

            time.sleep(2)


            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div/div")
            element.click()
            time.sleep(2)


            element = driver.find_element(By.CSS_SELECTOR, "[data-value='kingdom']")
            element.click()
            time.sleep(2)

            buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                print('button.text ========================= ', button.text)
                if button.text == 'EXPORT CURRENT RESULTS':
                    print('button =============== ', button.text)
                    button.click()
                    break

            time.sleep(1)

            driver.back()
            time.sleep(2)

    time.sleep(5)
    driver.quit()
