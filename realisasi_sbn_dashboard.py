import time
import os
import pandas as pd
import streamlit as st
import gdown
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

st.set_page_config(page_title="Realisasi SBN", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Dashboard Realisasi SBN DJPPR")
st.markdown('<style>div.block-container{padding-top:1rem;}</style', unsafe_allow_html=True)

# Replace the following URL with your own Google Drive file shareable link
url = 'https://drive.google.com/uc?id=1mtKjIYLvxmBClIx2qeZ7KGXW0dGcEFjU'

# Download the file
output = 'realisasi_sbn_hingga_2023.xlsx'
gdown.download(url, output, quiet=False)

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(output)

#filter tanggal
col1, col2 = st.columns((2))
df["Tanggal Setelmen/Settlement Date"] = pd.to_datetime(df["Tanggal Setelmen/Settlement Date"])
startDate = pd.to_datetime('2024-01-01')
endDate = pd.to_datetime(df["Tanggal Setelmen/Settlement Date"]).max()

with col1:
  date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
  date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Tanggal Setelmen/Settlement Date"]>= date1) & (df["Tanggal Setelmen/Settlement Date"] <= date2)].copy()

# Display the DataFrame
#st.write(f"Menampilkan {min(len(df), 100)} baris pertama dari total {len(df)} baris.")
st.dataframe(df.head(100))
