DROP INDEX IF EXISTS ERIIncidents CASCADE;
DROP INDEX IF EXISTS ERIBoroughs CASCADE;
DROP INDEX IF EXISTS ERIDates CASCADE;
DROP INDEX IF EXISTS ERICoordinates CASCADE;
DROP INDEX IF EXISTS ServiceComplaints CASCADE;
DROP INDEX IF EXISTS ServiceBoroughs CASCADE;
DROP INDEX IF EXISTS ServiceDates CASCADE;
DROP INDEX IF EXISTS ServiceCoordinates CASCADE;
CREATE INDEX ERIIncidents ON ERI(incident);
CREATE INDEX ERIBoroughs ON ERI(borough DESC NULLS LAST);
CREATE INDEX ERIDates ON ERI(creation_date, closed_date DESC NULLS LAST);
CREATE INDEX ERICoordinates ON ERI(latitude, longitude);
CREATE INDEX ServiceComplaints ON ServiceRequests(complaint_type);
CREATE INDEX ServiceBoroughs ON ServiceRequests(borough DESC NULLS LAST);
CREATE INDEX ServiceDates ON ServiceRequests(creation_date, closed_date DESC NULLS LAST);
CREATE INDEX ServiceCoordinates ON ServiceRequests(latitude, longitude);
