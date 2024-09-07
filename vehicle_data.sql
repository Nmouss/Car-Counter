-- cmd-shift-P "Run query"
SELECT * FROM vehicle_data;

SELECT vehicle_type, time FROM vehicle_data WHERE vehicle_type="car";

-- Select all the columns where time is greater than or equal to '22:13:50'
SELECT * FROM vehicle_data WHERE time >= '22:13:50';

SELECT COUNT(*) FROM vehicle_data WHERE time >= '22:13:50';
