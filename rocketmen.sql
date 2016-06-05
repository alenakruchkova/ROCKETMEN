CREATE TABLE Countries (
    country_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    flag VARCHAR(400)
    );


CREATE TABLE Astronauts(
	astronaut_id SERIAL PRIMARY KEY,
	name VARCHAR(300) NOT NULL,
	gender VARCHAR(1),
	dob VARCHAR(10),
	status VARCHAR(300),
	country_id VARCHAR(10) REFERENCES Countries,
	first_flight_start VARCHAR(100) NOT NULL,
	second_flight_start VARCHAR(100),
	third_flight_start VARCHAR(100),
	fourth_flight_start VARCHAR(100),
	fifth_flight_start VARCHAR(100),
	sixth_flight_start VARCHAR(100),
	seventh_flight_start VARCHAR(100),
	current_flight_start VARCHAR(100),
	current_flight_spacecraft VARCHAR(100),
	num_completed_flights INTEGER,
	duration_completed_flights VARCHAR(100),
	num_evas INTEGER,
	duration_evas VARCHAR(100),
	photo VARCHAR(400),
	twitter VARCHAR(80),
	widget VARCHAR(40)
	);


CREATE TABLE Users(
	user_id SERIAL PRIMARY KEY,
	user_phone VARCHAR(15) NOT NULL

);



