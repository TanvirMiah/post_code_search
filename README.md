Simple app to detect what constituency a postcode is in, as well as the MP, party and ward in the UK. This is a project made to learn the functionality of DuckDB.

*This is accurate as of 2024.* 

If there are any issues or glitches, please let me know!

# Libraries/tech used
- Flask
- Duckdb
- Motherduck (Optional)

# Get started
1. Copy or download the repo.
2. Create a virtual environment and install the requrements txt.
3. Run ```python initial_loading.py```. This creates the DuckDB file in your './db' folder and loads all the data from the CSVs into the relevant tables. 
4. Run ```flask --app app run```. This should run the app off your personal computer.

## Pushing data to MotherDuck
If you want to have an online version of the database, perform the following: 
1. Create an account on Motherduck.
2. Create the database in Motherduck by running the SQL command ```CREATE DATABASE postcodes``` in a notebook.
3. Run ```python push_database_to_motherduck.py```. You will be prompted to authorise your session. 

You can also get a token from MotherDuck and use environment variables to perform this. 

# Things I'd like to add
- Rather than generating a very long list when searching an incomplete postcode like 'SW1', contain the results into a window and show the first 10 rows before needing to scroll
- Generate a map using leaflet js to put pinpoints on all the postcodes in a constituency
- Create other ways to search other things, such as all postcodes in a constituency
