CREATE DEFINER=`root`@`localhost` PROCEDURE `CalculateAQI`(
	IN PM25 FLOAT,
    IN PM10 FLOAT,
    IN CO FLOAT,
    IN NO2 FLOAT,
    IN SO2 FLOAT,
    IN O3 FLOAT,
    OUT OverallAQI INT,
    OUT AQIBucket VARCHAR(50)
)
BEGIN
    DECLARE AQI_PM25 INT DEFAULT 0;
    DECLARE AQI_PM10 INT DEFAULT 0;
    DECLARE AQI_CO INT DEFAULT 0;
    DECLARE AQI_NO2 INT DEFAULT 0;
    DECLARE AQI_SO2 INT DEFAULT 0;
    DECLARE AQI_O3 INT DEFAULT 0;

    -- AQI Calculation for PM2.5
    IF PM25 BETWEEN 0 AND 12 THEN
        SET AQI_PM25 = (50 - 0) / (12 - 0) * (PM25 - 0) + 0;
    ELSEIF PM25 BETWEEN 12.1 AND 35.4 THEN
        SET AQI_PM25 = (100 - 51) / (35.4 - 12.1) * (PM25 - 12.1) + 51;
    ELSEIF PM25 BETWEEN 35.5 AND 55.4 THEN
        SET AQI_PM25 = (150 - 101) / (55.4 - 35.5) * (PM25 - 35.5) + 101;
    ELSEIF PM25 BETWEEN 55.5 AND 150.4 THEN
        SET AQI_PM25 = (200 - 151) / (150.4 - 55.5) * (PM25 - 55.5) + 151;
    ELSEIF PM25 BETWEEN 150.5 AND 250.4 THEN
        SET AQI_PM25 = (300 - 201) / (250.4 - 150.5) * (PM25 - 150.5) + 201;
    ELSEIF PM25 BETWEEN 250.5 AND 350.4 THEN
        SET AQI_PM25 = (400 - 301) / (350.4 - 250.5) * (PM25 - 250.5) + 301;
    ELSEIF PM25 > 350.4 THEN
        SET AQI_PM25 = 500;
    END IF;

    -- AQI Calculation for PM10
    IF PM10 BETWEEN 0 AND 54 THEN
        SET AQI_PM10 = (50 - 0) / (54 - 0) * (PM10 - 0) + 0;
    ELSEIF PM10 BETWEEN 55 AND 154 THEN
        SET AQI_PM10 = (100 - 51) / (154 - 55) * (PM10 - 55) + 51;
    ELSEIF PM10 BETWEEN 155 AND 254 THEN
        SET AQI_PM10 = (150 - 101) / (254 - 155) * (PM10 - 155) + 101;
    ELSEIF PM10 BETWEEN 255 AND 354 THEN
        SET AQI_PM10 = (200 - 151) / (354 - 255) * (PM10 - 255) + 151;
    ELSEIF PM10 BETWEEN 355 AND 424 THEN
        SET AQI_PM10 = (300 - 201) / (424 - 355) * (PM10 - 355) + 201;
    ELSEIF PM10 BETWEEN 425 AND 504 THEN
        SET AQI_PM10 = (400 - 301) / (504 - 425) * (PM10 - 425) + 301;
    ELSEIF PM10 > 504 THEN
        SET AQI_PM10 = 500;
    END IF;

    -- AQI Calculation for CO
    IF CO BETWEEN 0 AND 4.4 THEN
        SET AQI_CO = (50 - 0) / (4.4 - 0) * (CO - 0) + 0;
    ELSEIF CO BETWEEN 4.5 AND 9.4 THEN
        SET AQI_CO = (100 - 51) / (9.4 - 4.5) * (CO - 4.5) + 51;
    ELSEIF CO BETWEEN 9.5 AND 12.4 THEN
        SET AQI_CO = (150 - 101) / (12.4 - 9.5) * (CO - 9.5) + 101;
    ELSEIF CO BETWEEN 12.5 AND 15.4 THEN
        SET AQI_CO = (200 - 151) / (15.4 - 12.5) * (CO - 12.5) + 151;
    ELSEIF CO BETWEEN 15.5 AND 30.4 THEN
        SET AQI_CO = (300 - 201) / (30.4 - 15.5) * (CO - 15.5) + 201;
    ELSEIF CO BETWEEN 30.5 AND 40.4 THEN
        SET AQI_CO = (400 - 301) / (40.4 - 30.5) * (CO - 30.5) + 301;
    ELSEIF CO > 40.4 THEN
        SET AQI_CO = 500;
    END IF;

    -- AQI Calculation for NO2
    IF NO2 BETWEEN 0 AND 53 THEN
        SET AQI_NO2 = (50 - 0) / (53 - 0) * (NO2 - 0) + 0;
    ELSEIF NO2 BETWEEN 54 AND 100 THEN
        SET AQI_NO2 = (100 - 51) / (100 - 54) * (NO2 - 54) + 51;
    ELSEIF NO2 BETWEEN 101 AND 360 THEN
        SET AQI_NO2 = (150 - 101) / (360 - 101) * (NO2 - 101) + 101;
    ELSEIF NO2 BETWEEN 361 AND 649 THEN
        SET AQI_NO2 = (200 - 151) / (649 - 361) * (NO2 - 361) + 151;
    ELSEIF NO2 BETWEEN 650 AND 1249 THEN
        SET AQI_NO2 = (300 - 201) / (1249 - 650) * (NO2 - 650) + 201;
    ELSEIF NO2 BETWEEN 1250 AND 1649 THEN
        SET AQI_NO2 = (400 - 301) / (1649 - 1250) * (NO2 - 1250) + 301;
    ELSEIF NO2 > 1649 THEN
        SET AQI_NO2 = 500;
    END IF;

    -- AQI Calculation for SO2
    IF SO2 BETWEEN 0 AND 35 THEN
        SET AQI_SO2 = (50 - 0) / (35 - 0) * (SO2 - 0) + 0;
    ELSEIF SO2 BETWEEN 36 AND 75 THEN
        SET AQI_SO2 = (100 - 51) / (75 - 36) * (SO2 - 36) + 51;
    ELSEIF SO2 BETWEEN 76 AND 185 THEN
        SET AQI_SO2 = (150 - 101) / (185 - 76) * (SO2 - 76) + 101;
    ELSEIF SO2 BETWEEN 186 AND 304 THEN
        SET AQI_SO2 = (200 - 151) / (304 - 186) * (SO2 - 186) + 151;
    ELSEIF SO2 BETWEEN 305 AND 604 THEN
        SET AQI_SO2 = (300 - 201) / (604 - 305) * (SO2 - 305) + 201;
    ELSEIF SO2 BETWEEN 605 AND 804 THEN
        SET AQI_SO2 = (400 - 301) / (804 - 605) * (SO2 - 605) + 301;
    ELSEIF SO2 > 804 THEN
        SET AQI_SO2 = 500;
    END IF;

    -- AQI Calculation for O3
    IF O3 BETWEEN 0 AND 54 THEN
        SET AQI_O3 = (50 - 0) / (54 - 0) * (O3 - 0) + 0;
    ELSEIF O3 BETWEEN 55 AND 70 THEN
        SET AQI_O3 = (100 - 51) / (70 - 55) * (O3 - 55) + 51;
    ELSEIF O3 BETWEEN 71 AND 85 THEN
        SET AQI_O3 = (150 - 101) / (85 - 71) * (O3 - 71) + 101;
    ELSEIF O3 BETWEEN 86 AND 105 THEN
        SET AQI_O3 = (200 - 151) / (105 - 86) * (O3 - 86) + 151;
    ELSEIF O3 BETWEEN 106 AND 200 THEN
        SET AQI_O3 = (300 - 201) / (200 - 106) * (O3 - 106) + 201;
    ELSEIF O3 > 200 THEN
        SET AQI_O3 = 500;
    END IF;

    -- Determine the overall AQI as the maximum value
    SET OverallAQI = GREATEST(AQI_PM25, AQI_PM10, AQI_CO, AQI_NO2, AQI_SO2, AQI_O3);

    -- Set AQI Bucket based on OverallAQI
    IF OverallAQI BETWEEN 0 AND 50 THEN
        SET AQIBucket = 'Good';
    ELSEIF OverallAQI BETWEEN 51 AND 100 THEN
        SET AQIBucket = 'Moderate';
    ELSEIF OverallAQI BETWEEN 101 AND 150 THEN
        SET AQIBucket = 'Unhealthy for Sensitive Groups';
    ELSEIF OverallAQI BETWEEN 151 AND 200 THEN
        SET AQIBucket = 'Unhealthy';
    ELSEIF OverallAQI BETWEEN 201 AND 300 THEN
        SET AQIBucket = 'Very Unhealthy';
    ELSEIF OverallAQI > 300 THEN
        SET AQIBucket = 'Hazardous';
    END IF;
END