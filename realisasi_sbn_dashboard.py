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
import plotly.express as px

st.set_page_config(page_title="Realisasi SBN", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Dashboard Realisasi SBN DJPPR")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style', unsafe_allow_html=True)

# Replace the following URL with your own Google Drive file shareable link
url = 'https://drive.google.com/uc?id=17QpxMTET-d9JQCpgSTD1MT6AIPuGfopW'

# Download the file
output = 'realisasi_sbn_sampai_2023.xlsx'
gdown.download(url, output, quiet=False)

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(output)

#filter tanggal
col1, col2 = st.columns((2))
df["Tanggal Setelmen/Settlement Date"] = pd.to_datetime(df["Tanggal Setelmen/Settlement Date"])
startDate = pd.to_datetime('2023-01-01')
endDate = pd.to_datetime(df["Tanggal Setelmen/Settlement Date"]).max()

with col1:
  date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
  date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Tanggal Setelmen/Settlement Date"]>= date1) & (df["Tanggal Setelmen/Settlement Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
kategori  = st.sidebar.multiselect("Kategori", df["Kategori"].unique())
if not kategori:
  df2 = df.copy()
else:
  df2 = df[df["Kategori"].isin(kategori)]

series = st.sidebar.multiselect("Series", df2["Seri/Series"].unique())
if not series:
  df3 = df2.copy()
else:
  df3 = df2[df2["Seri/Series"].isin(series)]

if not kategori and not series:
  filtered_df = df
elif not series:
  filtered_df = df[df["Kategori"].isin(kategori)]
elif not kategori:
  filtered_df = df[df["Seri/Series"].isin(series)]
else:
  filtered_df = df3[df3["Kategori"].isin(kategori) & df3["Seri/Series"].isin(series)]

# Convert 'Total Penawaran/ Incoming Bid' to numeric, forcing non-numeric values to NaN, then filling NaN with 0
filtered_df["Total Penawaran/ Incoming Bid"] = pd.to_numeric(filtered_df["Total Penawaran/ Incoming Bid"], errors='coerce').fillna(0)
incoming_by_series = filtered_df.groupby(by = ["Seri/Series"], as_index = False)["Total Penawaran/ Incoming Bid"].sum()
incoming_by_series["Total Penawaran/ Incoming Bid"] = pd.to_numeric(incoming_by_series["Total Penawaran/ Incoming Bid"], errors='coerce')
# Sort the DataFrame by 'Total Penawaran/ Incoming Bid' in descending order and select the top 10
top10_incoming_by_series = incoming_by_series.sort_values(by="Total Penawaran/ Incoming Bid", ascending=False).head(10)

with col1:
  st.subheader("Incoming Bid by Series")
  fig = px.bar(
    top10_incoming_by_series, 
    x="Total Penawaran/ Incoming Bid", 
    y="Seri/Series", 
    text=[f'{x:,.2f}' for x in top10_incoming_by_series["Total Penawaran/ Incoming Bid"]],
    template="seaborn", orientation="h"
  )
  st.plotly_chart(fig, use_container_width=True, height=200)

# Display the DataFrame
#st.write(f"Menampilkan {min(len(df), 100)} baris pertama dari total {len(df)} baris.")
st.dataframe(df.head(100))
st.dataframe(filtered_df.head(100))
