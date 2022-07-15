import requests
import sys

address = '192.168.0.102'
username = 'Administrator'
password = 'admin'

csv_names = ['System_Sensor_log0.csv']

download_link = f'http://{address}/StorageCardUSB/{csv_names[0]}?UP=TRUE&FORCEBROWSE'

def download_log(args):
    # Start a session, this should keep cookies between requests
    with requests.Session() as s:
        
        # Try to login using the Login fields
        p = s.post(f'http://{address}/Templates/Loginpage.html?', data={'Login': username, 'Password': password})

        # Save response to a file to view the returned data
        with open("response1.html", "wb") as f:
            f.write(p.content)

        # Try to download the file csv file
        r = s.get(download_link)

        # Save response to a file to view the returned data
        with open("response2.html", "wb") as f:
            f.write(r.content)

        print(p.text)
        

if __name__ == '__main__':
    download_log(sys.argv)