UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/220px-Flag_of_Russia.svg.png' WHERE country_id='RU';

UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Flag_of_the_United_Kingdom.svg/220px-Flag_of_the_United_Kingdom.svg.png' WHERE country_id='GB';

UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png' WHERE country_id='US';


INSERT INTO Astronauts (name, gender, dob, status, country_id, 
						current_flight_start, first_flight_start, num_completed_flights, 
						duration_completed_flights,
						num_evas, duration_evas, photo, instagram)
	VALUES ('Scott Kelly', 'M', '1964.02.21',
			'Active','US', '2015.03.27', '1999.12.20',4, 
			'180 days 01 h 49 min 26 sec', 3, '18 h 20 min',
			'http://www.astronaut.ru/flights/foto/iss25/kelly.jpg', 
			'stationcdrkelly');

INSERT INTO Astronauts (name, gender, dob, status, country_id, 
						current_flight_start, first_flight_start, num_completed_flights, 
						duration_completed_flights,
						num_evas, duration_evas, photo)
	VALUES ('Mikhail Kornienko', 'M', '1960.04.15',
			'Active','RU', '2015.03.27', '2010.04.02', 1, 
			'176 days 01 h 18 min 13 sec', 2, '12 h 17 min',
			'http://www.astronaut.ru/flights/foto/iss43/kornienko.jpg');