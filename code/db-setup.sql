DROP DATABASE IF EXISTS dbms_final_project;
CREATE DATABASE dbms_final_project;

DROP USER IF EXISTS dbms_project_user;
CREATE USER dbms_project_user WITH PASSWORD 'dbms_password';

GRANT ALL PRIVILEGES ON DATABASE dbms_final_project TO dbms_project_user;