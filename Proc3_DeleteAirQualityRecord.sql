CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteAirQualityRecord`(IN input_city VARCHAR(255), IN input_date DATE)
BEGIN
    -- Delete related records from the airqualityindex table using JOIN
    DELETE aqi
    FROM airqualityindex aqi
    JOIN airqualitymeasurements aqm ON aqm.MeasurementID = aqi.MeasurementID
    WHERE aqm.CityID IN (SELECT CityID FROM cities WHERE City = input_city)
    AND aqm.Date = input_date;

    -- Delete records from the airqualitymeasurements table
    DELETE FROM airqualitymeasurements
    WHERE CityID IN (SELECT CityID FROM cities WHERE City = input_city)
    AND Date = input_date;
END