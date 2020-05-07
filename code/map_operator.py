from database import SqlOperator

class MapOperator:

    def __init__(self, conn_string):
        self.operator = SqlOperator(conn_string)

    # Range Queries ====================================================================================================

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_coords_range_one(self, relation, lower_lat, upper_lat, lower_long, upper_long):
        print("coords range one")

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_date_range_one(self, relation, lower_date, upper_date):
        print("coords range one")

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_coords_range_union(self, lower_lat, upper_lat, lower_long, upper_long):
        # should use get_coords_range for both relations and extend one list
        print("coords range union")

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_date_range_union(self, lower_date, upper_date):
        # should use get_date_range for both relations and extend one list
        print("date range union")

    # Lone Union Queries ===============================================================================================

    # returns all points in the latitude and longitude in the union of the relations
    def get_coords_union_one(self, latitude, longitude):
        # should use get_coords on both relations and extend one list
        print("coords union one")

    # gets the union of creation_date
    def get_time_union(self):
        # use function of same name
        print("time union")

    # gets all coords of the union of latitude and longitude
    def get_coords_union_all(self):
        # use function of same name
        print("coords union all")

    # gets the union of creation_date and coordinates
    def get_time_and_coords_union(self):
        # use function of same name
        print("time and coords union")

    # Grouping Queries =================================================================================================

    # returns the the sum of the grouped up incidents
    # returns with tuples in the form of (complaint_type, count(complaint_type))
    def get_incidents_group_sum(self):
        # use function of same name
        print("incidents group sum")

    # returns the most recent of each incident
    # returns with tuples in the form of (complaint_type, max(creation_date))
    def get_incidents_most_recent(self):
        # use function of same name
        print("incidents most recent")