-- cmd-shift-P "Run query"
SELECT * FROM vehicle_data;

SELECT vehicle_type, time FROM vehicle_data WHERE vehicle_type="car";

SELECT * FROM vehicle_data WHERE time >= '22:13:50';
