from map_operator import MapOperator
from database import SqlOperator

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"


# checks if date1 is more recent than date2
def __compare_date(date1, date2):
    date1_nums = [int(date1[0] + date1[1]), int(date1[3] + date1[4]), int(date1[6] + date1[7] + date1[8] + date1[9]),
                  int(date1[11] + date1[12]), int(date1[14] + date1[15]), int(date1[17] + date1[18])]
    date2_nums = [int(date2[0] + date2[1]), int(date2[3] + date2[4]), int(date2[6] + date2[7] + date2[8] + date2[9]),
                  int(date2[11] + date2[12]), int(date2[14] + date2[15]), int(date2[17] + date2[18])]
    return date1_nums[2] > date2_nums[2] or date1_nums[0] > date2_nums[0] or date1_nums[1] > date2_nums[1] or \
        date1[20] < date2[20] or date1_nums[3] > date2_nums[3] or date1_nums[4] > date2_nums[4] or \
           date1_nums[5] > date2_nums[5]


def __check_input(string, type):
    if type == "float":
        try:
            float(string)
        except ValueError:
            print("ERROR: Type Mismatch")
            return False
        return True
    elif type == "date":
        if len(string) == 22:
            if string[2] == '/' and string[5] == '/' and string[10] == ' ' and string[13] == ':' and string[16] == ':' and string[19] == ' ':
                return True
        print("ERROR: Improper Date Format")
        return False
    elif type == "relation":
        if string != "ERI" and string != "Service Requests" and string != "both":
            print("ERROR: Relation " + string + " does not exist.")
            return False
        return True
    else:
        print("INTERNAL CODE ERROR: Type Mismatch.")


def main():
    print("Welcome to the 311 Service Requests and Emergency Response Incident Map for New York City")
    print("For a list of commands input the command \\help")
    print("To quit the program input the command \\q")
    operator = MapOperator(connection_string)
    
    while True:
        print("Input a command:")
        cmd = input()

        # Exit Command
        if cmd == "\\q":
            break
        elif cmd == "\\help":
            print("COMMAND LIST =======================================")
            print("\\q")
            print("\\range coordinates")
            print("\\range coordinates union")
            print("\\range date")
            print("\\range date union")
            print("\\location coordinates")
            print("\\union coordinates")
            print("\\union date")
            print("\\union coord_and_date")
            print("\\incidents sum")
            print("\\incidents recent")
            print("====================================================")
        #this command is used to get all incidents/complaints within a range of coordinates in  database(s) specified by users
        elif cmd == "\\range coordinates":
            correct_input = True
            # get range for coordinates
            print("Input which database to select from (ERI, Service Requests, both)")
            relation = input()
            print("Input Lower Latitude:")
            lower_lat = float(input())
            print("Input Upper Latitude:")
            upper_lat = float(input())
            print("Input Lower Longitude:")
            lower_long = float(input())
            print("Input Upper Longitude:")
            upper_long = float(input())

            # check input
            if __check_input(lower_lat, "float") == False or __check_input(upper_lat, "float") == False or \
                    __check_input(lower_long, "float") == False or __check_input(upper_long, "float") == False or \
                    __check_input(relation, "relation") == False:
                correct_input = False
            elif lower_lat >= upper_lat or lower_long >= upper_long:
                print("ERROR: Bounds are mismatched")

            # execute map op
            if correct_input:
                if relation != "both":
                    operator.get_coords_range_one(relation,lower_lat,\
                    upper_lat, lower_long,upper_long)
                else:
                    operator.get_coords_range_union(lower_lat,\
                    upper_lat, lower_long,upper_long)
                # execute code
                # use if else if else to get relation needed
                # for both relations get both and use extend list
                print("code")
                
        #this command is used to get all incidents/complaints within a range of coordinates in the two datasets ERI and ServiceRequests
        elif cmd == "\\range coordinates union":
            correct_input = True
            # get range for coordinates
            print("Input Lower Latitude:")
            lower_lat = float(input())
            print("Input Upper Latitude:")
            upper_lat = float(input())
            print("Input Lower Longitude:")
            lower_long = float(input())
            print("Input Upper Longitude:")
            upper_long = float(input())

            # check input
            if __check_input(lower_lat, "float") == False or __check_input(upper_lat, "float") == False or \
                    __check_input(lower_long, "float") == False or __check_input(upper_long, "float") == False:
                correct_input = False
            elif lower_lat >= upper_lat or lower_long >= upper_long:
                print("ERROR: Bounds are mismatched")

            # execute map op
            if correct_input:
                # execute code and get both relations range
                operator.get_coords_range_union(lower_lat,\
                upper_lat, lower_long,upper_long)
                print("code")
        
        #this command is used to get all incidents/complaints within a range of dates in database(s) specified by users
        elif cmd == "\\range date":
            correct_input = True
            # get input
            print("Input which database to select from (ERI, Service Requests, both)")
            relation = input()
            print("Input Date as MM/DD/YYYY HH:MI:SS AM.")
            print("Input first date(oldest):")
            lower_date = input()
            print("input second date(recent):")
            upper_date = input()

            # check input
            if __check_input(lower_date, "date") == False or __check_input(upper_date, "date") == False or \
                    __check_input(relation, "relation"):
                correct_input = False
            if __compare_date(upper_date, lower_date) == False:
                print("ERROR: Date bounds have negative distance")
                correct_input = False

            # execute map op
            if correct_input:
                # do the same as range coordinate one
                if relation != "both":
                    operator.get_date_range_one(relation,lower_date,upper_date)
                else:
                    operator.get_date_range_union(lower_date,upper_date)
                print("code")
                
        #this command is used to get all incidents/complaints within a range of dates in the two datasets ERI and ServiceRequests
        elif cmd == "\\range date union":
            correct_input = True
            # get input
            print("Input Date as MM/DD/YYYY HH:MI:SS AM.")
            print("Input first date(oldest):")
            lower_date = input()
            print("input second date(recent):")
            upper_date = input()

            # check input
            if __check_input(lower_date, "date") == False or __check_input(upper_date, "date") == False:
                correct_input = False
            if __compare_date(upper_date, lower_date) == False:
                print("ERROR: Date bounds have negative distance")
                correct_input = False

            # execute map op
            if correct_input:
                # execute range date on both relations and extend one of them
                operator.get_date_range_union(lower_date,upper_date)
                print("code")
                
         #this command is used to get all incidents/complaints with specific coordinates in the two datasets ERI and ServiceRequests
        elif cmd == "\\location coordinates":
            correct_input = True
            # get input
            print("Input Latitude:")
            latitude = input()
            print("Input Longitude:")
            longitude = input()

            # check input
            if __check_input(latitude, "float") == False:
                correct_input = False
                print("ERROR: Latitude was not a float")
            if __check_input(longitude, "float") == False:
                correct_input = False
                print("ERROR: Longitude was not a float")

            # execute map op
            if correct_input:
                # execute input on both maps
                operator.get_coords_union_one(latitude,longitude)
                print("code")
                
         #this command is used to get all incidents/complaints with the same coordinates in the two datasets ERI and ServiceRequests
        elif cmd == "\\union coordinates":
            operator.get_same_coords()
            print("code")
            
        #this command is used to get all incidents/complaints with the same datetime in the two datasets ERI and ServiceRequests
        elif cmd == "\\union date":
            operator.get_same_time()
            print("code")
            
         #this command is used to get all incidents and complaints with the same coordinates and date in the two datasets ERI and ServiceRequests
        elif cmd == "\\union coord_and_date":
            operator.get_same_time_and_coords()
            print("code")
            
        elif cmd == "\\incidents sum":
            operator.get_incidents_group_sum()
            print("code")
        elif cmd == "\\incidents recent":
            operator.get_incidents_most_recent()
            print("code")
        else:
            print("ERROR: Input not Valid.")


if __name__ == "__main__":
    main()
