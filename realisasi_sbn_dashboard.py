import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import os
import time

def download_file():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up the download path
    download_path = tempfile.mkdtemp()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the webpage
        driver.get("https://www.djppr.kemenkeu.go.id/ringkasanhasilpenerbitan")
        
        # Wait for the "View" button to be clickable
        wait = WebDriverWait(driver, 10)
        view_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View")))
        
        # Click the button
        view_button.click()
        
        # Wait for the file to be downloaded (adjust the time if needed)
        time.sleep(5)
        
        # Find the downloaded file
        downloaded_files = os.listdir(download_path)
        if downloaded_files:
            file_path = os.path.join(download_path, downloaded_files[0])
            return file_path
        else:
            return None
    finally:
        driver.quit()

def main():
    st.title("File Downloader and Viewer")

    if st.button("Download and Display File"):
        with st.spinner("Downloading file..."):
            file_path = download_file()
        
        if file_path:
            st.success("File downloaded successfully!")
            
            # Determine file type and display accordingly
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension in ['.xlsx', '.xls']:
                st.write("Excel file detected. Displaying first few rows:")
                import pandas as pd
                df = pd.read_excel(file_path)
                st.dataframe(df.head())
            elif file_extension == '.pdf':
                st.write("PDF file detected. Displaying file info:")
                st.write(f"File path: {file_path}")
                st.write(f"File size: {os.path.getsize(file_path)} bytes")
            else:
                st.write("File downloaded. Unable to display content.")
            
            # Option to download the file
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download file",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream"
                )
        else:
            st.error("Failed to download the file.")

if __name__ == "__main__":
    main()
