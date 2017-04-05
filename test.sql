CREATE TABLE `Sensors_values` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`sensor_id`	INTEGER,
	`timestamp`	INTEGER,
	`value`	REAL
);
CREATE TABLE `Sensors` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT
);
INSERT INTO `Sensors` (id,name) VALUES (1,'air_humidity');
INSERT INTO `Sensors` (id,name) VALUES (2,'air_temperature');
INSERT INTO `Sensors` (id,name) VALUES (3,'air_humidity');
INSERT INTO `Sensors` (id,name) VALUES (4,'soil_temperature');
INSERT INTO `Sensors` (id,name) VALUES (5,'soil_moisture');
INSERT INTO `Sensors` (id,name) VALUES (6,'raindrop');