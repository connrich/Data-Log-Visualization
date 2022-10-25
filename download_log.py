from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv, find_dotenv
import sys
import time
import os

# Custom library imports
from data_object import Data



# Load hidden variables
load_dotenv(find_dotenv())

# VPN log in page
stridelinx_address = 'www.stridelinx.com/portal/login?next=%2Fdevices'
# Username for StridLinx account
stridelinx_username = os.getenv('stridelinx_username')
# Password for StrideLinx account
stridelinx_password = os.getenv('stridelinx_password')


# HMI address
hmi_address = '192.168.0.102'
# Username for log in
hmi_username = os.getenv('HMI_USERNAME')
# Password for log in
hmi_password = os.getenv('HMI_PASSWORD')


# Names of files to download
csv_names = ['System_Sensor_log0.csv']



def download_log(args):
    # Custom function for waiting for elements to load 
    def load_then_click(xpath):
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
        except Exception as e:
            print(e)

    # Waits until all downloads are completed
    # File names will have '.crdownload' file type until download is fully complete
    def wait_for_downloads():
        while any([filename.endswith(".crdownload") for filename in
                os.listdir(download_path)]):
            time.sleep(2)

    # Download files to the current working directory
    download_path = os.getcwd()

    # Start a service using the Chrome driver
    service = Service(executable_path='chromedriver_win32/chromedriver.exe')

    # Options for the service
    # Sets the Chrome download path
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    # Initialize web driver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to VPN page
    driver.get(f'http://{stridelinx_address}')

    username_field = driver.find_element(By.XPATH("//input[@name='emailAddress' and @placeholder='E-mail address']"))
    username_field.send_keys(stridelinx_username)

    password_field = driver.find_element(By.NAME, 'Password')
    password_field.send_keys(stridelinx_password)


    # Navigate to HMI webserver
    driver.get(f'http://{hmi_address}')

    # Enter login name
    username_field = driver.find_element(By.NAME, 'Login')
    username_field.send_keys(hmi_username)

    # Enter password
    password_field = driver.find_element(By.NAME, 'Password')
    password_field.send_keys(hmi_password)

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

    # Merge the downloaded data into the database
    file = Data(607)
    file.merge(csv_names[0])



if __name__ == '__main__':

    download_log(sys.argv)
    print(stridelinx_username)
    print(stridelinx_password)
    print(hmi_username)
    print(hmi_password)