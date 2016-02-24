CREATE TABLE Countries (
    country_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    flag VARCHAR(400)
    );


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
	twitter VARCHAR(80)
	);






