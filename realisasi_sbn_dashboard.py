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

# Replace the following URL with your own Google Drive file shareable link
url = 'https://drive.google.com/uc?id=1mtKjIYLvxmBClIx2qeZ7KGXW0dGcEFjU'

# Download the file
output = 'realisasi_sbn_hingga_2023.xlsx'
gdown.download(url, output, quiet=False)

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(output)

# Display the DataFrame
st.write(f"Menampilkan {min(len(df), 100)} baris pertama dari total {len(df)} baris.")
st.dataframe(df.head(100))
