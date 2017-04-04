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
INSERT INTO `Sensors` (id,name) VALUES (1,'humidity');
INSERT INTO `Sensors` (id,name) VALUES (2,'soil_temperature');
INSERT INTO `Sensors` (id,name) VALUES (3,'soil_moisture');
INSERT INTO `Sensors` (id,name) VALUES (4,'raindrop');