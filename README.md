# Retrieve Historical Daily Gridded PRISM Data from RCC ACIS

## Description
This module utilizes web services available through RCC ACIS (https://rcc-acis.org), a service of the Northeast Regional Climate Center at Cornell University (https://nrcc.cornell.edu). A series of coordinates are ingested from a user-provided CSV that contains latitude and longitude decimal coordinates anywhere in the continental United States (CONUS). The user is prompted to provide start and end dates between 01-01-1981 and present, in MM-DD-YYYY format, in the command line when the script runs. 4km resolution PRISM daily climate data  (https://prism.oregonstate.edu) are saved to a CSV  dataset in the local directory containing daily recordsets of max and min temperatures in Fahrenheit, as well as precipitation in inches.

## Installation

### Step 1
Create a subdirectory in the location where this script is saved called '.coordinates'

### Step 2
Create a subdirectory in the location where this script is saved called '.results'

### Step 3
Save a copy of your coordinates CSV file to the '.coordinates' folder. The filename does not matter but the first column must have the header 'id' to provide a unique alphanumberic id, the second column header must be'lat', and the third  column must have the header 'lon'.

### Double check
Make sure your 'lon' coordinates have a negative value. It is common to mislabel 'lon' and 'lat'. If this is the case you will get an error message in the command prompt.

### Step 4
Open the command prompt. Create your python envonment by running `python -m venv <env_name_here>`. Activate your new environment, then run `pip install -r requirements.txt`

### Step 5
From the command line, with your environment activated, run 'python retrieve_climate_data_from_prism.py' Follow the directions presented in the command line to complete a query.

### Special Note
Requests with large date ranges or long location lists  will require significant processing power and time, depending on your hardware or cloud computing resources. Please be patient.

## Authorship
Dan Olmstead | https://github.com/danolmstead