import pandas as pd

# Load the dataset Dr. Andreas sent
file_path = "decisions-snapshots_pivot-filtered_20260122-130352.csv" # Ensure the filename matches!

try:
    df = pd.read_csv(file_path)
    
    print("--- E313 Dataset Exploration ---")
    print(f"Total Records found: {len(df)}")
    print("\nAvailable Data Columns (Features):")
    print(df.columns.tolist())
    
    print("\nFirst 5 Rows of Data:")
    print(df.head())
    
    print("\nStatistical Summary (Latency & Energy):")
    # We focus on what Dr. Andreas mentioned: Latency and Energy
    print(df.describe())

except Exception as e:
    print(f"Error reading the file: {e}")