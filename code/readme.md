# Database Systems Final Group Project Instructions

## What's in the Application
`application.py`: The bulk of our code. Runs an infinite loop reading user input and running the appropriate commands

`database.py`: Contains SQL functions

`datasets.txt`: The two datasets we are working with

`db-indices.sql`: Creates indices for the database

`db-setup.sql`: Creates the database and the psql user. Grants database permissions to that user.

`load_data.py`: Loads data from the datasets

`map_operator.py`: Collection of usable functions on the map

`requirements.txt`: Contains necessary dependencies

`schema.sql`: Creates the table skeletons for the database


## Setup
All manually run files are located in the `code` subdirectory.

`requirements.txt` includes wget for "" and psycopg2 for python-to-sql code to work.

Run `db-setup.sql` first to inititate the database `dbms_final_project` and the user `dbms_project_user` with granted access to the database.

Then run `retrieve_data.py` to download the datasets into a new `datasets` directory within `code`. While downloading `Emergency_Response_Incidents.csv` takes a few seconds, `311_Service_Requests_from_2010_to_Present.csv` is a very large dataset (12gb) and may take up to 30 minutes. Download speed will depend on your personal download speed.

Finally, run `load_data.py` to load data from `datasets` to your database. This may take around the same amount of time as `retrieve_data.py`.


## Application
After running `application.py`, you can input any of the given commands to select a query to run (use \help to bring up a list of possible commands).

### Function and Usage for Each Command
`\range coordinates`: this command is used to get all incidents/complaints within a range of coordinates in the database(s) specified by users. 
Usage: 
```
[Input which database to select from (ERI, Service Requests, both):]
ERI
[Input Lower Latitude:]
40.82853407669855
[Input Upper Latitude:]
41
[Input Lower Longitude:]
-73.90436001541751
[Input Upper Longitude:]
-73
```

`\range coordinates union`: this command is used to get all incidents/complaints within a range of coordinates in the two datasets ERI and ServiceRequests
Usage: 
```
[Input Lower Latitude:]
40.82853407669855
[Input Upper Latitude:]
41
[Input Lower Longitude:]
-73.90436001541751
[Input Upper Longitude:]
-73
```

`\range date`: this command is used to get all incidents/complaints within a range of dates in database(s) specified by users
Usage: 
```
[Input which database to select from (ERI, Service Requests, both):]
ERI
[Input Date as MM/DD/YYYY HH:MI:SS AM.]
[Input first date(oldest):]
05/10/2011 12:51:22 AM
[input second date(recent):]
05/11/2011 11:45:22 AM
```

`\range date union`: this command is used to get all incidents/complaints within a range of dates in the two datasets ERI and ServiceRequests
Usage: 
```
[Input Date as MM/DD/YYYY HH:MI:SS AM.]
[Input first date(oldest):]
05/10/2011 12:51:22 AM
[input second date(recent):]
05/11/2011 11:45:22 AM
```

`\location coordinates`: this command is used to get all incidents/complaints with specific coordinates in the two datasets ERI and ServiceRequests
Usage:
```
[Input Latitude:]
40.82853407669855
[Input Longitude:]
-73.90436001541751
```

`\incidents borough`: this command is used to get all incidents/complaints in the same borough
Usage:
```
[Input borough name:]
```

`\union date`:  this command is used to get all incidents/complaints with the same datetime in the two datasets ERI and ServiceRequests

`\incidents sum`: #this command is used to get the the sum of the grouped up incidents/complaints in both datasets

`\incidents recent`: #this command is used to returns the most recent one in each group of incident/complaints in the two datasets
