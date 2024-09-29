import streamlit as st
import requests
import tempfile
import os
import pandas as pd
from io import BytesIO

def download_file():
    url = "https://www.djppr.kemenkeu.go.id/ringkasanhasilpenerbitan"
    
    try:
        # First, get the main page
        response = requests.get(url)
        response.raise_for_status()

        # You might need to parse the HTML to find the actual download link
        # For this example, let's assume the download link is directly available
        # You may need to adjust this part based on the actual structure of the webpage
        download_url = "https://www.djppr.kemenkeu.go.id/uploads/files/dmo_realisasi/2024/RHPSBNReguler2024.xlsx"

        # Download the file
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_file.write(file_response.content)
            return temp_file.name

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("File Downloader and Viewer")

    if st.button("Download and Display File"):
        with st.spinner("Downloading file..."):
            file_path = download_file()
        
        if file_path:
            st.success("File downloaded successfully!")
            
            # Read and display Excel file
            try:
                df = pd.read_excel(file_path)
                st.write("Excel file content (first few rows):")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Error reading the Excel file: {e}")
            
            # Option to download the file
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download file",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Failed to download the file.")

if __name__ == "__main__":
    main()
