from code.database import SqlOperator

class MapOperator:

    def __init__(self, sql_op):
        self.operator = sql_op

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_range_coords(self, relation, lower_lat, upper_lat, lower_long, upper_long):
        print("")

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_range_date(self, relation, lower_date, upper_date):
        print("")

    # returns all points in the latitude and longitude
    def get_coords(self, relation, latitude, longitude):
        print("")

    # gets the union of creation_date
    def get_time_union(self):
        print("")

    # gets the union of latitude and longitude
    def get_coords_union(self):
        print("")

    # gets the union of creation_date and coordinates
    def get_time_and_coords_union(self):
        print("")

    # returns the the sum of the grouped up incidents
    # returns with tuples in the form of (complaint_type, count(complaint_type))
    def get_incidents_group_sum(self):
        print("")

    # returns the most recent of each incident
    # returns with tuples in the form of (complaint_type, max(creation_date))
    def get_incidents_most_recent(self):
        print("")