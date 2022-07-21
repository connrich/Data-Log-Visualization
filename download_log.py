from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import os

from generate_plot import generate_plot


# HMI address
address = '192.168.0.102'
# Username for log in 
username = 'Administrator'
# Password for log in
password = 'admin'

# Names of files to download 
csv_names = ['System_Sensor_log0.csv', 'NMR_Flow0.csv']



def download_log(args):

    # Custom function for waiting for elements 
    def load_then_click(xpath):
        try:
            print('looking')
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
            print('clicked')
        except Exception as e:
            print(e)
    
    # Waits until all downloads are completed
    def wait_for_downloads():
        while any([filename.endswith(".crdownload") for filename in 
                os.listdir(download_path)]):
            time.sleep(2)

    # Downloads files to the current working directory
    download_path = os.getcwd()

    # Start a service using the Chrome driver
    service = Service(executable_path='chromedriver_win32/chromedriver.exe')

    # Options for the service 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    # Initialize web driver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to website
    driver.get(f'http://{address}')

    # Enter login name
    username_field = driver.find_element(By.NAME, 'Login')
    username_field.send_keys(username)

    # Enter password
    password_field = driver.find_element(By.NAME, 'Password')
    password_field.send_keys(password)

    # Click the login button
    load_then_click('/html/body/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td/form/table/tbody/tr[3]/td/input')

    # Click the file browser button 
    load_then_click('/html/body/table[2]/tbody/tr/td[1]/table/tbody/tr[11]/td[3]/a')

    # Click the USB storage button
    load_then_click('/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr[9]/td[2]/a/b/font')

    # Iterate through file names and click each download link
    for name in csv_names:
        load_then_click(f"//a[text()='{name}']")
    
    # Display downloads page
    driver.get("chrome://downloads/")

    # Used to wait until download is complete
    # paths = WebDriverWait(driver, 600, 1).until(finish_downloads)
    wait_for_downloads()

    # Ends the session by closing all windows and terminating the driver 
    driver.quit()

    # Create html plots
    for name in csv_names:
        generate_plot(['', name])

    


if __name__ == '__main__':
    download_log(sys.argv)