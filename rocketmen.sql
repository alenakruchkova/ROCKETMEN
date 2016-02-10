CREATE TABLE Countries (
    country_id VARCHAR(2) PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    flag VARCHAR(400) NOT NULL
    );

INSERT INTO Countries (country_id, name, flag)
	VALUES ('RU', 'Russian Federation', 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/220px-Flag_of_Russia.svg.png');

INSERT INTO Countries (country_id, name, flag)
	VALUES ('GB', 'United Kingdom', 'https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Flag_of_the_United_Kingdom.svg/220px-Flag_of_the_United_Kingdom.svg.png');

INSERT INTO Countries (country_id, name, flag)
	VALUES ('US', 'United States', 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png');

CREATE TABLE Astronauts(
	-- astonaut_id INTEGER AUTO_INCREMENT PRIMARY KEY,
	astronaut_id SERIAL PRIMARY KEY,
	name VARCHAR(300) NOT NULL,
	gender VARCHAR(1),
	dob VARCHAR(10),
	status VARCHAR(300),
	country_id VARCHAR(2) REFERENCES Countries,
	first_flight_start VARCHAR(100) NOT NULL,
	current_flight_start VARCHAR(100),
	current_flight_spacecraft VARCHAR(100),
	num_completed_flights INTEGER,
	duration_completed_flights VARCHAR(100),
	num_evas INTEGER,
	duration_evas VARCHAR(100),
	photo VARCHAR(400),
	twitter VARCHAR(80),
	instagram VARCHAR(400)
	);

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




