from code.sql_operator import SqlOperator

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

# TODO add your code here (or in other files, at your discretion) to load the data



def main():
    # TODO invoke your code to load the data into the database
    operator = SqlOperator(connection_string)
    # first time setup
    operator.check_if_setup_needed(
            "/home/fangyu/Documents/compsci/Database_Systems/spring-2020-csci-4380/final-project/ERI.csv",
            "/home/fangyu/Documents/compsci/Database_Systems/spring-2020-csci-4380/final-project/ServiceRequests.csv")
    # print(operator.get_range("ERI", 40, 41, -75, -74))
    # print(operator.get_incident_union("ServiceRequests"))


if __name__ == "__main__":
    main()
