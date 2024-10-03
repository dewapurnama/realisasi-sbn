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
filtered_df["Total Penawaran/ Incoming Bid"] = pd.to_numeric(filtered_df["Total Penawaran/ Incoming Bid"], errors='coerce')
incoming_by_series = filtered_df.groupby(by = ["Seri/Series"])["Total Penawaran/ Incoming Bid"].sum().reset_index()
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
  # Reverse the y-axis
  fig.update_layout(yaxis={'categoryorder':'total ascending'})
  st.plotly_chart(fig, use_container_width=True, height=200)

# Convert 'WAY Awarded' to numeric, forcing non-numeric values to NaN, then filling NaN with 0
filtered_df["WAY Awarded"] = pd.to_numeric(filtered_df["WAY Awarded"], errors='coerce')
filtered_df_way = filtered_df[filtered_df["WAY Awarded"] != 1]
way_by_series = filtered_df_way.groupby(by=["Seri/Series"])["WAY Awarded"].mean().reset_index()
way_by_series["WAY Awarded"] = pd.to_numeric(way_by_series["WAY Awarded"], errors='coerce')

# Sort the DataFrame by 'WAY Awarded' in ascending order
top10_way_by_series = way_by_series.sort_values(by="WAY Awarded", ascending=False).head(10)

#with col2:
    #st.subheader("WAY Awarded by Series")
    #fig = px.bar(
        #top10_way_by_series, 
        #x="WAY Awarded", 
        #y="Seri/Series", 
        #text=[f'{x:.4f}' for x in top10_way_by_series["WAY Awarded"]],
        #template="seaborn", 
        #orientation="h"
    #)
    
    #fig.update_layout(yaxis={'categoryorder':'total ascending'})
    #st.plotly_chart(fig, use_container_width=True, height=200)

import plotly.graph_objects as go

import plotly.graph_objects as go
import pandas as pd

# Ensure the date column is in datetime format
filtered_df['Tanggal Setelmen/Settlement Date'] = pd.to_datetime(filtered_df['Tanggal Setelmen/Settlement Date'], errors='coerce')

# Ensure both bid columns are numeric
filtered_df["Total Penawaran/ Incoming Bid"] = pd.to_numeric(filtered_df["Total Penawaran/ Incoming Bid"], errors='coerce')
filtered_df["Total Penawaran Diterima/ Awarded Bid"] = pd.to_numeric(filtered_df["Total Penawaran Diterima/ Awarded Bid"], errors='coerce')

# Group by month (ignoring year) and calculate the sum of both 'Incoming Bid' and 'Awarded Bid'
bids_by_month = filtered_df.groupby(filtered_df['Tanggal Setelmen/Settlement Date'].dt.month).agg({
    "Total Penawaran/ Incoming Bid": "sum",
    "Total Penawaran Diterima/ Awarded Bid": "sum"
}).reset_index()

# Rename the month column
bids_by_month = bids_by_month.rename(columns={'Tanggal Setelmen/Settlement Date': 'Month'})

# Sort by month
bids_by_month = bids_by_month.sort_values('Month')

# Create a list of month names for x-axis labels
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
bids_by_month['Month_Name'] = bids_by_month['Month'].apply(lambda x: month_names[x-1])

with col2:
  fig = go.Figure(data=[
    go.Bar(name='Incoming Bid', x=bids_by_month["Month_Name"], y=bids_by_month["Total Penawaran/ Incoming Bid"]),
    go.Bar(name='Awarded Bid', x=bids_by_month["Month_Name"], y=bids_by_month["Total Penawaran Diterima/ Awarded Bid"])
  ])
  # Change the bar mode and update layout
  fig.update_layout(
    barmode='group',
    title="Monthly Incoming vs Awarded Bids (Aggregated Across Years)",
    xaxis_title="Month",
    yaxis_title="Bid Amount",
    legend_title="Bid Type",
    height=500,  # Adjust this value to change the height of the chart
    xaxis={'categoryorder':'array', 'categoryarray':month_names},  # This ensures correct month order
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",  # Anchor the legend at the bottom of the space allocated to the legend
        y=1,  # Place it at the top (y=1 means top, y=0 is bottom)
        xanchor="center",  # Center the legend horizontally
        x=0.5  # Place it in the center of the x-axis
    )
  )
  # Add value labels on the bars
  for trace in fig.data:
    y_values = trace.y
    text_positions = ['top center' if y >= 0 else 'bottom center' for y in y_values]
    
    fig.add_traces(go.Scatter(
        x=trace.x, 
        y=y_values,
        mode='text',
        text=[f'{y:,.0f}' for y in y_values],
        textposition=text_positions,
        showlegend=False
    ))
  st.plotly_chart(fig, use_container_width=True)
  
# Display the DataFrame
#st.write(f"Menampilkan {min(len(df), 100)} baris pertama dari total {len(df)} baris.")
st.dataframe(bids_by_month.head(100))
st.dataframe(df.head(100))
st.dataframe(filtered_df.head(100))
