CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePollutantAndRecalculateAQI`(
	IN p_city VARCHAR(255),
    IN p_date DATE,
    IN p_pollutant_name VARCHAR(20),
    IN p_pollutant_value FLOAT
)
BEGIN
    DECLARE measurement_id INT;
    DECLARE city_id INT;
    DECLARE overallAQI INT;
    DECLARE aqiBucket VARCHAR(50);

    -- Get the CityID for the specified city
    SELECT CityID INTO city_id FROM cities WHERE City = p_city LIMIT 1;

    -- Check if city_id exists
    IF city_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'City not found in cities table';
    END IF;

    -- Get the MeasurementID for the specified city and date
    SELECT MeasurementID INTO measurement_id
    FROM airqualitymeasurements
    WHERE CityID = city_id AND Date = p_date
    LIMIT 1;

    -- Check if the measurement record exists
    IF measurement_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Measurement record not found for the given city and date';
    END IF;

    -- Update only the specified pollutant in the airqualitymeasurements table
    IF p_pollutant_name = 'PM25' THEN
        UPDATE airqualitymeasurements SET PM25 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'PM10' THEN
        UPDATE airqualitymeasurements SET PM10 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'NO' THEN
        UPDATE airqualitymeasurements SET `NO` = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'NO2' THEN
        UPDATE airqualitymeasurements SET NO2 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'NOx' THEN
        UPDATE airqualitymeasurements SET NOx = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'NH3' THEN
        UPDATE airqualitymeasurements SET NH3 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'CO' THEN
        UPDATE airqualitymeasurements SET CO = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'SO2' THEN
        UPDATE airqualitymeasurements SET SO2 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'O3' THEN
        UPDATE airqualitymeasurements SET O3 = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'Benzene' THEN
        UPDATE airqualitymeasurements SET Benzene = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'Toluene' THEN
        UPDATE airqualitymeasurements SET Toluene = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSEIF p_pollutant_name = 'Xylene' THEN
        UPDATE airqualitymeasurements SET Xylene = p_pollutant_value WHERE MeasurementID = measurement_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid pollutant name';
    END IF;

    -- Call CalculateAQI with the desired values
    CALL CalculateAQI(35.0, 60.0, 0.3, 25.0, 15.0, 120.0, @OverallAQI, @AQIBucket);

    -- Retrieve the AQI and AQI Bucket values
    SELECT @OverallAQI, @AQIBucket INTO overallAQI, aqiBucket;

    -- Update the airqualityindex table with the recalculated AQI and AQI Bucket
    UPDATE airqualityindex
    SET AQI = overallAQI, AQI_Bucket = aqiBucket
    WHERE MeasurementID = measurement_id;
END