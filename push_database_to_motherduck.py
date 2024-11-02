import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MotherDuck
motherduck_token = os.getenv('MOTHERDUCK_TOKEN')
conn = duckdb.connect("md:post_codes")

# Attach local database
conn.execute("ATTACH '.\\db\\postcodes.duckdb' AS local")

# Copy tables (replace table_name with your actual table name)
conn.execute("""
    CREATE TABLE main.post_codes AS 
    SELECT * FROM local.postcodes_list
""")

conn.close()