UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/220px-Flag_of_Russia.svg.png' WHERE country_id='RU';

UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Flag_of_the_United_Kingdom.svg/220px-Flag_of_the_United_Kingdom.svg.png' WHERE country_id='GB';

UPDATE Countries SET flag='https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png' WHERE country_id='US';

INSERT INTO Countries (country_id, name, flag)
	VALUES ('SU', 'USSR','https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/220px-Flag_of_the_Soviet_Union.svg.png');

UPDATE Astronauts SET dob='1964.02.21', status='Active', country_id='US', 
						current_flight_start='2015.03.27', num_completed_flights=4, 
						duration_completed_flights='180 days 01 h 49 min 26 sec',
						num_evas=3, duration_evas='18 h 20 min', 
						twitter='StationCDRKelly',
						widget='702656916627935232',
						photo='http://www.astronaut.ru/flights/foto/iss25/kelly.jpg'
						WHERE name='Scott Kelly';

UPDATE Astronauts SET name='Mikhail Kornienko', dob='1960.04.15', status='Active', country_id='RU', 
						current_flight_start='2015.03.27', num_completed_flights=1, 
						duration_completed_flights='176 days 01 h 18 min 13 sec',
						num_evas=2, duration_evas='12 h 17 min', 
						photo='http://www.astronaut.ru/flights/foto/iss43/kornienko.jpg' 
						WHERE name='Mikhail Korniyenko';

UPDATE Astronauts SET name='Timothy Peake',country_id='GB', current_flight_start='2015.12.15',
						photo='http://www.astronaut.ru/flights/foto/iss46/peake.jpg',
						twitter='astro_timpeake',
						widget='702673016488984577'
						WHERE name='Tim Peake';

UPDATE Astronauts SET country_id='US', current_flight_start='2015.12.15',
						photo='http://www.astronaut.ru/flights/foto/iss46/kopra.jpg',
						twitter='astro_tim',
						widget='702673368529547264'
				 		WHERE name='Timothy Kopra';

UPDATE Astronauts SET country_id='RU', current_flight_start='2015.09.02',
						photo='http://www.astronaut.ru/as_rusia/vvs/foto/volkov2.jpg',
						twitter='Volkov_ISS',
						widget='702668791914696704'
						WHERE name='Sergey Volkov';

UPDATE Astronauts SET country_id='RU', current_flight_start='2015.12.15',
						photo='http://www.astronaut.ru/as_rusia/vvs/foto/malenchenko2.jpg' 
						WHERE name='Yuri Malenchenko';