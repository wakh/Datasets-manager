from database import SqlOperator
from mapAPI import MainFrame
import pandas


class MapOperator:

    def __init__(self, conn_string):
        self.operator = SqlOperator(conn_string)

    # Range Queries ====================================================================================================

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_coords_range_one(self, relation, lower_lat, upper_lat, lower_long, upper_long):
        results = self.operator.get_coords_range_one(relation, lower_lat, upper_lat, lower_long, upper_long)
        app = MainFrame(results)
        app.mainloop()
       

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_date_range_one(self, relation, lower_date, upper_date):
        results = self.operator.get_date_range_one(relation, lower_date, upper_date)
        app = MainFrame(results)
        app.mainloop()
        

    # [inclusive lower, exclusive upper)
    # upper is always the larger number: ex. -74 < -73 and 2 > 1
    def get_coords_range_union(self, lower_lat, upper_lat, lower_long, upper_long):
        # should use get_coords_range for both relations and extend one list
        results = self.operator.get_coords_range_union(lower_lat, upper_lat, lower_long, upper_long)
        app = MainFrame(results)
        app.mainloop()
        

    # [inclusive lower, exclusive upper)
    # upper date is the more recent date
    # Use date format MM/DD/YYYY HH:MI:SS AM
    def get_date_range_union(self, lower_date, upper_date):
        # should use get_date_range for both relations and extend one list
        results = self.operator.get_date_range_union(lower_date, upper_date)
        app = MainFrame(results)
        app.mainloop()
        

    # Lone Union Queries ===============================================================================================

    # returns all points in the latitude and longitude in the union of the relations
    def get_coords_union_one(self, latitude, longitude):
        # should use get_coords on both relations and extend one list
        results = self.operator.get_coords_union_one(latitude, longitude)
        app = MainFrame(results)
        app.mainloop()
       

    # maybe not used in our project
    def get_date_union_one(self, date):
        results = self.operator.get_date_union_one(date)
        app = MainFrame(results)
        app.mainloop()
        

    # gets the union of creation_date
    def get_same_time(self):
        # use function of same name
        results = self.operator.get_same_time()
        app = MainFrame(results)
        app.mainloop()
        

    # gets the incidents/complaints of the same borough
    def get_incidents_in_borough(self, borough):
        # use function of same name
        results = self.operator.get_incidents_in_borough(borough)
        app = MainFrame(results)
        app.mainloop()
        

    # Grouping Queries =================================================================================================

    # returns the the sum of the grouped up incidents
    # returns with tuples in the form of (complaint_type, count(complaint_type))
    def get_incidents_group_sum(self):
        # use function of same name
        results = self.operator.get_incidents_group_sum()
        app = MainFrame(results)
        app.mainloop()

    # returns the most recent of each incident
    # returns with tuples in the form of (complaint_type, max(creation_date))
    def get_incidents_most_recent(self):
        # use function of same name
        results = self.operator.get_incidents_most_recent()
        app = MainFrame(results)
        app.mainloop()
