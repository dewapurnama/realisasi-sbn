import time
import os
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {"download.default_directory": "/tmp"})
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the webpage
        driver.get("https://www.djppr.kemenkeu.go.id/ringkasanhasilpenerbitan")
        
        # Wait for the page to load
        time.sleep(5)
        
        # Find all "View" buttons
        view_buttons = driver.find_elements(By.LINK_TEXT, "View")
        
        if view_buttons:
            # Click the first (most recent) "View" button
            driver.execute_script("arguments[0].click();", view_buttons[0])
            st.success("Clicked on the most recent 'View' button.")
        else:
            st.error("No 'View' buttons found on the page.")
            return
        
        # Wait for the file to download
        time.sleep(10)  # Adjust this time as needed
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return
    finally:
        driver.quit()

    # Upload to Google Drive
    drive = authenticate_drive()
    files = os.listdir("/tmp")
    excel_file = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
    if excel_file:
        file_drive = drive.CreateFile({'title': excel_file[0]})
        file_drive.SetContentFile(os.path.join("/tmp", excel_file[0]))
        file_drive.Upload()
        st.success(f"Uploaded {excel_file[0]} to Google Drive.")
    else:
        st.error("No Excel file found in the download directory.")

def main():
    st.title("Download and Upload Excel File to Google Drive")
    
    if st.button("Download and Upload"):
        with st.spinner("Downloading and uploading file..."):
            download_and_upload()

if __name__ == "__main__":
    main()
