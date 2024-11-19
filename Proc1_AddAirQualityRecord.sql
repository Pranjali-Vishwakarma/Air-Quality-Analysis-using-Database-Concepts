CREATE DEFINER=`root`@`localhost` PROCEDURE `AddAirQualityRecord`(
	IN p_city VARCHAR(255),
    IN p_date DATE,
    IN p_pm25 FLOAT,
    IN p_pm10 FLOAT,
    IN p_no FLOAT,
    IN p_no2 FLOAT,
    IN p_nox FLOAT,
    IN p_nh3 FLOAT,
    IN p_co FLOAT,
    IN p_so2 FLOAT,
    IN p_o3 FLOAT,
    IN p_benzene FLOAT,
    IN p_toluene FLOAT,
    IN p_xylene FLOAT
)
BEGIN
    DECLARE v_cityID INT;
    DECLARE v_measurementID INT;
    DECLARE v_aqi INT;
    DECLARE v_aqi_bucket VARCHAR(50);

    -- Step 1: Retrieve the CityID from the cities table
    SELECT CityID INTO v_cityID
    FROM cities
    WHERE City = p_city
    limit 1;

    -- Check if CityID is found, if not, raise an error
    IF v_cityID IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'City not found in cities table';
    END IF;

    -- Step 2: Calculate AQI and AQI_Bucket using the calculateAQI procedure
    CALL calculateAQI(p_pm25, p_pm10, p_co, p_no2, p_so2, p_o3, v_aqi, v_aqi_bucket);

    -- Step 3: Insert a new record into airqualitymeasurements table
    INSERT INTO airqualitymeasurements (
        CityID, Date, PM25, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene
    )
    VALUES (
        v_cityID, p_date, p_pm25, p_pm10, p_no, p_no2, p_nox, p_nh3, p_co, p_so2, p_o3, p_benzene, p_toluene, p_xylene
    );

    -- Get the auto-generated MeasurementID for the newly inserted record
    SET v_measurementID = LAST_INSERT_ID();

    -- Step 4: Insert a new record into airqualityindex table with the calculated AQI and AQI_Bucket
    INSERT INTO airqualityindex (
        MeasurementID, AQI, AQI_Bucket
    )
    VALUES (
        v_measurementID, v_aqi, v_aqi_bucket
    );
END