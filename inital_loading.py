import duckdb
from dotenv import load_dotenv
import re
import os
import glob
import pandas as pd
from datetime import datetime

load_dotenv()

# Initialize connection
conn = duckdb.connect('.\\db\\postcodes.duckdb')

directory = os.fsdecode('.\\data\\constituency_postcodes')
pattern = r'^(.*?)\s+postcodes'

print("Connected. Creating constituencies database.")
conn.sql("CREATE TABLE IF NOT EXISTS constituency AS SELECT * FROM '.\\data\\UK constituency postcodes 2024.csv'")
print("Constituency database created successfully.")
print("Creating and inserting postcode database.")

def convert_datetime(date_str):
    if pd.isna(date_str):
        return None
    try:
        # Parse the date string and convert to ISO format
        return pd.to_datetime(date_str).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return None

def load_postcode_csvs(directory, connection):
    cons_df = pd.read_csv('.\\data\\UK constituency postcodes 2024.csv')
    print("creating table")
    
    # Create table using the connection object
    connection.sql("""
        CREATE TABLE IF NOT EXISTS postcodes_list (
            postcode VARCHAR,
            in_use BOOLEAN,
            latitude INT,
            longitude INT,
            easting BIGINT,
            northing BIGINT,
            grid_ref VARCHAR,
            altitude BIGINT,
            population BIGINT,
            households BIGINT,
            nearest_station VARCHAR,
            distance_to_station DOUBLE,
            built_up_area VARCHAR,
            water_company VARCHAR,
            sewage_company VARCHAR,
            district VARCHAR,
            ward VARCHAR,
            county_electoral_division VARCHAR,
            code VARCHAR
        )
    """)
   
    print("Table initialized.")
    print("inserting rows")
    
    csv_files = glob.glob(os.path.join(directory, '*csv'))
    for file in csv_files:
        print(f"Processing file: {file}")
        constituency_name = os.path.basename(file).split('.')[0]
        
        # Read CSV and convert date columns
        df = pd.read_csv(file).drop(columns=['Introduced', 'Terminated'])

        # Convert datetime columns to correct format
        if 'introduced' in df.columns:
            df['introduced'] = df['introduced'].apply(convert_datetime)
        if 'terminated' in df.columns:
            df['terminated'] = df['terminated'].apply(convert_datetime)
        
        # Replace any remaining NaT values with NULL
        df = df.replace({pd.NaT: None})
        
        # Error handling for constituency name matching
        match = re.search(pattern, constituency_name)
        if not match:
            print(f"Warning: Could not extract constituency name from {constituency_name}")
            continue
            
        cons_code = match.group(1)
        matching_rows = cons_df[cons_df['Constituency'] == cons_code]
        
        if matching_rows.empty:
            print(f"Warning: No matching constituency found for {cons_code}")
            continue
            
        df['code'] = matching_rows.iloc[0,0]
        
        try:
            # Use the connection object to insert data
            connection.sql("INSERT INTO postcodes_list SELECT * FROM df")
            print(f"Inserted data for {constituency_name}")
        except Exception as e:
            print(f"Error inserting data for {constituency_name}: {str(e)}")
            # Optionally, you might want to continue with the next file
            continue

    print("All files processed")

try:
    load_postcode_csvs(directory, conn)
    print("Data loading completed successfully")
except Exception as e:
    print(f"Error occurred: {str(e)}")
finally:
    conn.close()
    print("Connection closed")