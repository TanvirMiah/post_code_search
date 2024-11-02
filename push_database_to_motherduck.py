import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MotherDuck
motherduck_token = os.getenv('MOTHERDUCK_TOKEN')
# Create database on Motherduck first called 'postcodes'
conn = duckdb.connect("md:postcodes")
print("Connected to Motherduck.")

# Attach local database
conn.execute("ATTACH './db/postcodes.duckdb' AS local")

# Copy tables 
print("Updating postcodes into Motherduck postcodes db...")
conn.execute("""
    CREATE TABLE IF NOT EXISTS main.post_codes AS 
    SELECT * FROM local.postcodes_list
""")
print("Done. Moving on to constituencies...")

print("Updating constiuency database...")
conn.execute("""
        CREATE TABLE IF NOT EXISTS main.constituency AS
        SELECT * FROM local.constituency
            """)
print("Done.")

conn.close()