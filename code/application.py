from code.map_operator import MapOperator
from code.database import SqlOperator

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

def __check_input(string, type):
    if type == "float":
        if isinstance(string, (float, int)) == False:
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
    operator = MapOperator(connection_string)
    while True:
        print("Input a command:")
        cmd = input()

        # Exit Command
        if cmd == "\\q":
            break
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
                # execute code
                # use if else if else to get relation needed
                # for both relations get both and use extend list
                print("code")
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
                print("code")
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
            if __check_input(lower_date, "date") == False or __check_input(upper_date, "float") == False or \
                    __check_input(relation, "relation"):
                correct_input = False
            # execute map op
            if correct_input:
                # do the same as range coordinate one
                print("code")
        elif cmd == "\\range date union":
            correct_input = True
            # get input
            print("Input first date(oldest):")
            lower_date = input()
            print("input second date(recent):")
            upper_date = input()
            # check input
            if __check_input(lower_date, "date") == False or __check_input(upper_date, "float") == False:
                correct_input = False
            # execute map op
            if correct_input:
                # execute range date on both relations and extend one of them
                print("code")
        elif cmd == "\\location coordinates":
            correct_input = True
            # get input
            print("Input Latitude:")
            latitude = input()
            print("Input Longitude:")
            longitude = input()
            # check input
            if __check_input(latitude, "float") == False or __check_input(longitude, "float") == False:
                correct_input = False
            # execute map op
            if correct_input:
                # execute input on both maps
                print("code")
        elif cmd == "\\union coordinates":
            print("code")
        elif cmd == "\\union date":
            print("code")
        elif cmd == "\\union coord_and_date":
            print("code")
        elif cmd == "\\incidents sum":
            print("code")
        elif cmd == "\\incidents recent":
            print("code")
        else:
            print("ERROR: Input not Valid.")


if __name__ == "__main__":
    main()