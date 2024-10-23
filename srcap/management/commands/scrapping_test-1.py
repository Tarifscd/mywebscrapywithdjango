from django.core.management.base import BaseCommand
import time
import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run():
    # Path to your WebDriver (download the appropriate driver for your browser)
    driver_path = '/usr/local/bin/chromedriver'

    # print('asdfgh ===============================', driver_path)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # Initialize the WebDriver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)
    # Open the webpage
    driver.get('https://app.cosmosid.com/sign-in')
    print('here ===============================', )

    # Wait for the page to load (you may need to adjust this based on site loading speed)
    time.sleep(2)

    # Example: Interact with the site (e.g., find a login button or search field)

    close_button = driver.find_element(By.ID, 'new-features-dialog--close')
    close_button.click()

    # You can also send login information if required:
    username_field = driver.find_element(By.ID, 'sign-in-form--email')  # Adjust selector
    password_field = driver.find_element(By.ID, 'sign-in-form--password')  # Adjust selector
    print('username_field ===============================', username_field)
    print('password_field ===============================', password_field)

    username_field.send_keys('demo_estee2@cosmosid.com')
    password_field.send_keys('xyzfg321')
    password_field.send_keys(Keys.RETURN)

    login_button = driver.find_element(By.ID, 'sign-in-form--submit') # Replace with the actual ID
    # login_button.click()
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(3)
    close_button = driver.find_element(By.ID, 'intro-tour--functional-2-tour--close-button')
    close_button.click()

    # button = driver.find_element_by_xpath("//*[@id='sign-in-form--submit']")
    # driver.get('https://app.cosmosid.com/search')
    wait = WebDriverWait(driver, 10)
    for i in range(1,5):

        links = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[{i}]//td[2]//a")))

        root_folder_name = 'srcap/management/commands/' + str(links.text) + '/'

        os.makedirs(root_folder_name, exist_ok=True)

        links.click()
        time.sleep(2)

        table = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody")  # or use another selector

        rows = table.find_elements(By.TAG_NAME, 'tr')
        for i in range(1,len(rows)+1):

            links = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[{i}]//td[2]//a")))

            links_text = links.text

            folder_name = root_folder_name + str(links_text) + '/'
            os.makedirs(folder_name, exist_ok=True)

            links.click()
            time.sleep(2)

            # element = driver.find_element(By.XPATH, "//*[text()='Export current results']")
            # element.click()

            buttons = driver.find_elements(By.TAG_NAME, 'button')

            for button in buttons:
                print('button.text ========================= ', button.text)
                if button.text == 'Taxonomy switcher':
                    print('button =============== ')
                    button.click()
                    break

            time.sleep(2)

            buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                print('button.text ========================= ', button.text)
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
                    print('button =============== ')
                    button.click()
                    break

            time.sleep(1)
            downloads_path = '/home/tarif/Downloads/'

            print('links_text =================== ', links_text)
            downloads_folder = os.path.expanduser('~/Downloads')
            print('downloads_folder =================== ', downloads_folder)
            file_name = [f for f in os.listdir(downloads_path) if f.startswith(str(links_text))]
            if file_name:
                file_name = file_name[0]
                print('file_name =================== ', file_name)

                current_directory = os.getcwd() + '/' + folder_name
                print('current_directory ================ ', current_directory)

                source_file = os.path.join(downloads_folder, file_name)
                destination_file = os.path.join(current_directory, file_name)

                shutil.move(source_file, destination_file)

            driver.back()

    # export_dropdn = driver.find_element(By.ID, 'more-actions')
    # driver.execute_script("arguments[0].click();", export_dropdn)
    #
    # data_testid = driver.find_element(By.CLASS_NAME, 'MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-2aj19w')
    # print('data_testid =========================== ', data_testid)
    # driver.execute_script("arguments[0].click();", data_testid)

    # links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    # print(links)
    # def a(links):
    #     for link in links:
    #         yield link
    # l = a(links)
    # print('lllllllll ============== ', next(l))
    # next(l).click()
    time.sleep(5)
    # After login or navigating, you can scrape or download files
    # You might need to find elements dynamically and interact with them

    # Example: Close the browser after you're done
    driver.quit()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        run()


