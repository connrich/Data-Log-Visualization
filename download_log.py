from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

from generate_plot import generate_plot


# TODO 
# Create wait functions for elements in case of server latency
# Add ability to select file to download using the file name 
#           files = ['data.csv', 'data_log.csv']
# Add functionality to wait until all downloads are complete 
#           https://stackoverflow.com/questions/48263317/selenium-python-waiting-for-a-download-process-to-complete-using-chrome-web
# Add ability to select download location 
#           File path to download location based on where scripts are saved 


address = '192.168.0.102'
username = 'Administrator'
password = 'admin'

csv_names = ['System_Sensor_log0.csv']

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
    
    def finish_downloads(driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            return document.querySelector('downloads-manager')
            .shadowRoot.querySelector('#downloadsList')
            .items.filter(e => e.state === 'COMPLETE')
            .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
            """)

    # Start a service using the Chrome driver
    service = Service(executable_path='chromedriver_win32/chromedriver.exe')

    # Options for the service 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    prefs = {"download.default_directory": r"C:\Users\Quantum\Desktop\Data Log Visualization\\"}
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

    # Click the download button
    # Current just set to download the third item in the USB list 
    load_then_click('/html/body/table[2]/tbody/tr/td[3]/div/font/table/tbody/tr[5]/td[2]/a')

    # Used to wait until download is complete
    # Will be replaced by better functionality in the future

    paths = WebDriverWait(driver, 600, 1).until(finish_downloads)
    
    # Ends the session by closing all windows and terminating the driver 
    driver.quit()

    generate_plot(['', 'System_Sensor_log0.csv'])

    


if __name__ == '__main__':
    download_log(sys.argv)