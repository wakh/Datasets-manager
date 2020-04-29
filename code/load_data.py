from code.database import SqlOperator
import os

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

# TODO add your code here (or in other files, at your discretion) to load the data



def main():
    # TODO invoke your code to load the data into the database
    operator = SqlOperator(connection_string)
    # first time setup
    dir_path = os.path.dirname(os.path.realpath(__file__))
    operator.check_if_setup_needed(
            dir_path + "/datasets/Emergency_Response_Incidents.csv",
            dir_path + "/datasets/311_Service_Requests_from_2010_to_Present.csv")
    # print(operator.get_incident_union("ServiceRequests"))


if __name__ == "__main__":
    main()
