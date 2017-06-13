BEGIN TRANSACTION;

CREATE TABLE "Sensors"
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name INTEGER
);

INSERT INTO `Sensors` VALUES (1,'air_humidity');
INSERT INTO `Sensors` VALUES (2,'air_temperature');
INSERT INTO `Sensors` VALUES (3,'soil_temperature');
INSERT INTO `Sensors` VALUES (4,'soil_moisture');
INSERT INTO `Sensors` VALUES (5,'raindrop');

CREATE TABLE "Sensors_values"
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    sensor_id INTEGER,
    value REAL,
    CONSTRAINT Sensors_values_Sensors_id_fk FOREIGN KEY (sensor_id) REFERENCES Sensors (id)
);

CREATE TABLE "Traffic"
(
    Traffic_count INTEGER NOT NULL
);

INSERT INTO `Traffic` VALUES (0);

COMMIT;
