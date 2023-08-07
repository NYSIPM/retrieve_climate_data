"""
RETRIEVE HISTORICAL DAILY GRIDDED PRISM DATA

This module utilizes web services available through RCC ACIS (https://rcc-acis.org),
a service of the Northeast Regional Climate Center at Cornell University
(https://nrcc.cornell.edu). A series of coordinates are ingested from a user-provided
CSV that contains latitude and longitude decimal coordinates anywhere in the
continental United States (CONUS). The user is prompted to provide start and
end dates between 01-01-1981 and present, in MM-DD-YYYY format, in the command line
when the script runs. 4km resolution PRISM daily climate data 
(https://prism.oregonstate.edu) are saved to a CSV  dataset in the local directory
containing daily recordsets of max and min temperatures in Fahrenheit, as well as
precipitation in inches.

Author: Dan Olmstead
Created: 08-03-2023
Updated: 08-07-2023
"""
# INSTRUCTIONS

# STEP 1. Create a subdirectory in the location where this script is saved
# called '.coordinates'

# STEP 2. Create a subdirectory in the location where this script is saved
# called '.results'

# STEP 3. Save a copy of your coordinates CSV file to the '.coordinates'
# folder. The filename does not matter but the first column must have the
# header 'id' to provide a unique alphanumberic id, the second column header
# must be'lat', and the third  column must have the header 'lon'.

# DOUBLE CHECK. Make sure your 'lon' coordinates have a negative value.
# It is common to mislabel 'lon' and 'lat'. If this is the case you will
# get an error message in the command prompt.

# STEP 4. Open the command prompt. Create your python envonment by running
# `python -m venv <env_name_here>`. Activate your new environment, then run
# `pip install -r requirements.txt`

# STEP 5. From the command line, with your environment activated, run 'python
# retrieve_climate_data_from_prism.py' Follow the directions presented in the
# command line to complete a query.

# Requests with large date ranges or long location lists  will require
# significant processing power and time, depending on your hardware or
# cloud computing resources. Please be patient.

# Import required packages
import re
import csv
import os
import requests
import datetime

def get_start_date_input():
    """Ask user for start date."""
    while True:
        user_input = input("Start date (YYYY-MM-DD): ")
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', user_input):
            return user_input
        else:
            print("Incorrect format. Please make sure to follow the YYYY-MM-DD pattern.")

def get_end_date_input():
    """Ask user for end date."""
    while True:
        user_input = input("End date (YYYY-MM-DD): ")
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', user_input):
            return user_input
        else:
            print("Incorrect format. Please make sure to follow the YYYY-MM-DD pattern.")

def import_coordinates():
    """
    Import latitude and longitude coordinates to a python dictionary.
    """
    directory_path = '.coordinates'
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)

                # Open and read the CSV file
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    csv_data_as_dict = [row for row in reader]
    except FileNotFoundError:
        print(f"Directory {directory_path} not found.")
    except PermissionError:
        print(f"No permission to read directory {directory_path}.")
    return csv_data_as_dict

def fetch_prism_daily_data():
    """
    Retrieve a daily record of max temp F, min temp F, and precip inches
    for each imported coordinate
    """
    # Set the variables
    url = 'http://data.rcc-acis.org/GridData'
    sdate = get_start_date_input()
    edate = get_end_date_input()
    grid = 21 # PRISM
    elems = "maxt,mint,pcpn"
    coordinates = import_coordinates()

    # CSV file headers
    headers = ['id','date','maxt_F','mint_F','pcpn_inches']

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = f'.results/output_{timestamp}.csv'
    dir_path = os.path.dirname(file_path)

    # Create directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Check if the file is empty
    file_is_empty = not os.path.exists(file_path) or os.stat(file_path).st_size == 0

    # Open a CSV file to write the data
    with open(file_path, 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the headers only if the file is empty
        if file_is_empty:
            writer.writerow(headers)

        for entry in coordinates:
            lat = entry['lat']
            lon = entry['lon']
            id = entry['id']
            params = {
                'loc': f"{lon},{lat}",
                'sdate': sdate,
                'edate': edate,
                'grid': grid,
                'elems': elems
            }
            response = requests.post(url, params, timeout=60)
            if response.status_code == 200:
                json_data = response.json()
                for row in json_data['data']:
                    writer.writerow([str(id)] + row) # Write the rows
                print(f"Fetching data for id {id}...")
            else:
                print(f"Error for coordinates {lon}, {lat}: {response.status_code}, {response.text}")
        print("\nTask complete. Check the '.results' subdirectory for CSV output.\n")

fetch_prism_daily_data()

# Define  the variables

URL = "http://data.rcc-acis.org/GridData"

# Execute the request
# Convert the response to CSV
# Save CSV to the local directory
