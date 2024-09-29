import time
import os
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver with download options
options = webdriver.ChromeOptions()
download_path = "C:/Users/User/Downloads/"  # Change this to your download path
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Navigate to the webpage
driver.get("https://www.djppr.kemenkeu.go.id/ringkasanhasilpenerbitan")

# Wait for the "View" button to be clickable
try:
    wait = WebDriverWait(driver, 10)
    view_button = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "View")))
    driver.execute_script("arguments[0].click();", view_button)

    print("The 'View' button was clicked successfully using JavaScript.")

    # Wait for the file to download
    time.sleep(5)  # Adjust the time as necessary based on file size

    # Load the downloaded Excel file
    files = os.listdir(download_path)
    excel_file = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]

    if excel_file:
        df = pd.read_excel(os.path.join(download_path, excel_file[0]), sheet_name="SBN", header=2) 
    else:
        print("No Excel file found in the download directory.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

st.dataframe(df.head(100))
