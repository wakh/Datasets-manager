import psycopg2


class SqlOperator:
    """
    # csv = ERI: [Incident Type, Location, Borough, Creation Date, Closed Date, Latitude, Longitude] (List)
    # Converted to Schema = ERI(incident, borough, creation_date, closed_date, latitude, longitude)
    # csv = ServiceRequests:
    #       [..., Created Date(1), Closed Date(2), ..., Complaint Type(5),
    #       ..., Borough(25), ..., Latitude(38), Longitude(39)] (List)
    # Converted to Schema = ServiceRequests(complaint_type, borough, creation_date, closed_date, latitude, longitude)
    # Each GET Function will return in the form of a list of tuples depending on how many attributes were selected
    # They will return all attributes unless specified otherwise
    """

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    # relative path in filepath/from code folder
    def __run_sql_file(self, filepath):
        # open and read sql file
        sql_file = open(filepath, 'r')
        command = sql_file.read()
        sql_file.close()
        # split the commands by semicolon
        sql_commands = command.split(';')
        cursor = self.conn.cursor()
        # execute the commands and omit newline at end
        for command in sql_commands:
            if command != '\n':
                cursor.execute(command)
                self.conn.commit()

    # runs schema.sql
    # need the path to csv from root/absolute path
    def __setup(self, sql_schema_file, path_to_csv, path_to_service_requests):
        self.__run_sql_file("schema.sql")
        cursor = self.conn.cursor()
        # copy the Emergency_Response_Incidents.csv to the table t
        f = open(path_to_csv, 'r')
        cursor.copy_expert("COPY t FROM stdin WITH CSV HEADER DELIMITER as ','", file=f)
        f.close()
        self.conn.commit()
        # insert table t to table ERI with specific columns only
        cursor.execute("INSERT INTO ERI SELECT x0 AS incident, x1 AS borough, "
                       "to_timestamp(x3, 'MM/DD/YYYY HH:MI:SS AM') AS creation_date, "
                       "to_timestamp(x4, 'MM/DD/YYYY HH:MI:SS AM') AS closed_date, "
                       "CAST(x5 AS NUMERIC(20,14)) AS latitude, CAST(x6 AS NUMERIC(20,14)) AS longitude FROM t "
                       "WHERE x0 IS NOT NULL AND x3 IS NOT NULL AND x5 IS NOT NULL AND x6 IS NOT NULL "
                       "ON CONFLICT DO NOTHING;")
        self.conn.commit()
        print("Halfway")
        # copy 311_Service_Requests_from_2010_to_Present.csv to table t2
        f = open(path_to_service_requests, 'r')
        cursor.copy_expert("COPY t2 FROM stdin WITH CSV HEADER DELIMITER as ','", file=f)
        f.close()
        self.conn.commit()
        # insert table t2 to table ServiceRequests with specific columns only
        cursor.execute("INSERT INTO ServiceRequests SELECT x5 AS complaint_type, x25 AS borough, "
                       "to_timestamp(x1, 'MM/DD/YYYY HH:MI:SS AM') AS creation_date, "
                       "to_timestamp(x2, 'MM/DD/YYYY HH:MI:SS AM') AS closed_date, "
                       "CAST(x38 AS NUMERIC(20,16)) AS latitude, CAST(x39 AS NUMERIC(20,16)) AS longitude FROM t2 "
                       "WHERE x5 IS NOT NULL AND x1 IS NOT NULL AND x38 IS NOT NULL AND x39 IS NOT NULL "
                       "ON CONFLICT DO NOTHING;")
        self.conn.commit()
        # delete pre-processing tables
        cursor.execute("DROP TABLE t; DROP TABLE t2")
        self.conn.commit()
        # make indices for tables
        self.__run_sql_file("db-indices.sql")

    def check_if_setup_needed(self, path_to_csv, path_to_service_requests):
        cursor = self.conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_tables WHERE tablename = 'eri')")
        eri_sample = cursor.fetchall()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_tables WHERE tablename = 'servicerequests')")
        service_sample = cursor.fetchall()
        if eri_sample[0][0] == False or service_sample[0][0] == False:
            self.__setup("schema.sql", path_to_csv, path_to_service_requests)

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_range_coords(self, relation, lower_lat, upper_lat, lower_long, upper_long):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + relation + " WHERE latitude >= " + str(lower_lat) + " AND latitude < "
                       + str(upper_lat) + " AND longitude >= " + str(lower_long) + "AND longitude < " +
                       str(upper_long) )
        return cursor.fetchall()

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_range_date(self, relation, lower_date, upper_date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + relation + " WHERE date >= to_timestamp(" + lower_date + ""
                            ", \'MM/DD/YYYY HH:MI:SS AM\') AND date < to_timestamp(" + upper_date + ", \'MM/DD/YYYY HH:MI:SS AM\'")
        return cursor.fetchall()

    # returns all points in the latitude and longitude
    def get_coords(self, relation, latitude, longitude):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + relation + " WHERE latitude = " + str(latitude) +
                       " AND longitude = " + str(longitude))
        return cursor.fetchall()

    # gets the union of creation_date
    def get_time_union(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT ERI.incident, ServiceRequests.complaint_type ERI.borough, "
            "ERI.creation_date, ERI.closed_date, ERI.latitude, ERI.longitude "
            "FROM ERI, ServiceRequests WHERE ERI.creation_date = ServiceRequests.creation_date")
        return cursor.fetchall()

    def get_coords_union(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT ERI.incident, ServiceRequests.complaint_type ERI.borough, "
            "ERI.creation_date, ERI.closed_date, ERI.latitude, ERI.longitude "
            "FROM ERI, ServiceRequests WHERE ERI.latitude = ServiceRequests.latitude AND "
            "ERI.longitude = ServiceRequests.longitude")
        return cursor.fetchall()

    # gets the union of creation_date and coordinates
    def get_time_and_coords_union(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ERI.incident, ServiceRequests.complaint_type ERI.borough, "
                       "ERI.creation_date, ERI.closed_date, ERI.latitude, ERI.longitude "
                       "FROM ERI, ServiceRequests WHERE ERI.creation_date = ServiceRequests.creation_date AND "
                       "ERI.latitude = ServiceRequests.latitude AND "
                       "ERI.longitude = ServiceRequests.longitude")
        return cursor.fetchall()

    # returns the the sum of the grouped up incidents
    # returns with tuples in the form of (complaint_type, count(complaint_type))
    def get_incidents_group_sum(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT incident, COUNT(incident) FROM ERI GROUP BY incident")
        incident_list = cursor.fetchall()
        cursor.execute("SELECT complaint_type, COUNT(complaint_type) FROM ServiceRequests GROUP BY complaint_type")
        incident_list.extend(cursor.fetchall())
        return incident_list

    # returns the most recent of each incident
    # returns with tuples in the form of (complaint_type, max(creation_date))
    def get_incidents_most_recent(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT incident, MAX(creation_date) FROM ERI GROUP BY incident")
        incident_list = cursor.fetchall()
        cursor.execute("SELECT complaint_type, MAX(creation_date) FROM ServiceRequests GROUP BY complaint_type")
        incident_list.extend(cursor.fetchall())
        return incident_list




