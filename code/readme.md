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
