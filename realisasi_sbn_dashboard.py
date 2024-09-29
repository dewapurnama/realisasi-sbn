import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates a local webserver for authentication
    drive = GoogleDrive(gauth)
    return drive

def download_and_upload():
    # Initialize the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {"download.default_directory": "/tmp"})
    driver = webdriver.Chrome(options=options)
    
    # Navigate to the webpage
    driver.get("https://www.djppr.kemenkeu.go.id/ringkasanhasilpenerbitan")
    
    # Wait for the "View" button to be clickable
    wait = WebDriverWait(driver, 10)
    view_button = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "View")))
    driver.execute_script("arguments[0].click();", view_button)

    # Wait for the file to download
    time.sleep(5)  # Adjust as necessary
    driver.quit()

    # Upload to Google Drive
    drive = authenticate_drive()
    files = os.listdir("/tmp")
    excel_file = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]

    if excel_file:
        file_drive = drive.CreateFile({'title': excel_file[0]})
        file_drive.SetContentFile(os.path.join("/tmp", excel_file[0]))
        file_drive.Upload()
        print(f"Uploaded {excel_file[0]} to Google Drive.")
    else:
        print("No Excel file found in the download directory.")

def main():
    st.title("Download and Upload Excel File to Google Drive")
    
    if st.button("Download and Upload"):
        download_and_upload()
        st.success("File downloaded and uploaded to Google Drive!")

if __name__ == "__main__":
    main()
