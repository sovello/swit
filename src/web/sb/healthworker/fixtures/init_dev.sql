delete from healthworker_healthworker;
delete from healthworker_specialty;
delete from healthworker_facility;
delete from healthworker_facilitytype;
delete from healthworker_region;
delete from healthworker_regiontype;

copy healthworker_regiontype from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/region_types.csv' with csv header;
copy healthworker_region from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/regions.csv' with csv header;

copy healthworker_facilitytype from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/facility_types.csv' with csv header;
copy healthworker_facility from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/facilities.csv' with csv header;

copy healthworker_specialty from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/specialties.csv' with csv header;

copy healthworker_healthworker from '/var/apps/switchboard/current/src/web/sb/healthworker/fixtures/healthworkers_sample.csv' with csv header;
