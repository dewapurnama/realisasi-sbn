import gdown
import pandas as pd

# Replace the following URL with your own Google Drive file shareable link
url = 'https://drive.google.com/uc?id=1mtKjIYLvxmBClIx2qeZ7KGXW0dGcEFjU'

# Download the file
output = 'realisasi_sbn_hingga_2023.xlsx'
gdown.download(url, output, quiet=False)

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(output)

# Display the DataFrame
df
