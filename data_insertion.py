import mysql.connector
import pandas as pd
import numpy as np

# Step 1: Load dataset from CSV
file_path = r"C:\Users\your\file\path\preprocessed_city_day.csv"  
data = pd.read_csv(file_path)

# Ensure Date is in proper format
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d', errors='coerce')

# Rename columns to remove dots (e.g., 'PM2.5' to 'PM25')
data.columns = data.columns.str.replace('.', '', regex=False)

# Step 2: Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="host",        
        user="user",             
        password="pwd",   
        database="air_quality_data"  
    )
    cursor = conn.cursor()

    cursor.execute('USE air_quality_data')

    # Step 3: Create Tables (if not already created)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cities (
        CityID INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(255)
    );
    ''')
    print("Cities table created or already exists.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AirQualityMeasurements (
        MeasurementID INT AUTO_INCREMENT PRIMARY KEY,
        CityID INT,
        Date DATE,
        PM25 FLOAT,
        PM10 FLOAT,
        NO FLOAT,
        NO2 FLOAT,
        NOx FLOAT,
        NH3 FLOAT,
        CO FLOAT,
        SO2 FLOAT,
        O3 FLOAT,
        Benzene FLOAT,
        Toluene FLOAT,
        Xylene FLOAT,
        FOREIGN KEY (CityID) REFERENCES Cities(CityID)
    );
    ''')
    print("AirQualityMeasurements table created or already exists.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AirQualityIndex (
        AQIID INT AUTO_INCREMENT PRIMARY KEY,
        MeasurementID INT,
        AQI INT,
        AQI_Bucket VARCHAR(50),
        FOREIGN KEY (MeasurementID) REFERENCES AirQualityMeasurements(MeasurementID)
    );
    ''')
    print("AirQualityIndex table created or already exists.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pollutants (
        PollutantID INT AUTO_INCREMENT PRIMARY KEY,
        PollutantName VARCHAR(255),
        PollutantDescription TEXT
    );
    ''')
    print("Pollutants table created or already exists.")

    # Step 4: Insert Cities into the 'Cities' Table
    cities = data['City'].unique()
    city_ids = {}

    for city in cities:
        cursor.execute("INSERT INTO Cities (City) VALUES (%s)", (city,))
        city_ids[city] = cursor.lastrowid  # Store the CityID for future reference
    conn.commit()
    print(f"{len(cities)} cities inserted into Cities table.")

    # Step 5: Insert Air Quality Measurements into 'AirQualityMeasurements' Table
    measurements_inserted = 0
    for index, row in data.iterrows():
        try:
            city_id = city_ids.get(row['City'])  
            
            if city_id is None:
                print(f"Skipping row {index} due to missing city ID")
                continue

            row = row.replace({np.nan: None})

            cursor.execute('''
                INSERT INTO AirQualityMeasurements (
                    CityID, Date, PM25, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                city_id, row['Date'], row['PM25'], row['PM10'], row['NO'], row['NO2'], row['NOx'], 
                row['NH3'], row['CO'], row['SO2'], row['O3'], row['Benzene'], row['Toluene'], row['Xylene']
            ))
            measurements_inserted += 1

        except mysql.connector.Error as e:
            print(f"Error inserting row {index}: {e}")
            continue  

    conn.commit()
    print(f"{measurements_inserted} rows inserted into AirQualityMeasurements table.")

    # Step 6: Insert Air Quality Index into 'AirQualityIndex' Table
    aqi_inserted = 0
    for index, row in data.iterrows():
        try:
            measurement_id = cursor.lastrowid  

            if pd.notna(row['AQI']) and pd.notna(row['AQI_Bucket']):
                cursor.execute('''
                    INSERT INTO AirQualityIndex (MeasurementID, AQI, AQI_Bucket)
                    VALUES (%s, %s, %s)
                ''', (measurement_id, row['AQI'], row['AQI_Bucket']))
                aqi_inserted += 1

        except mysql.connector.Error as e:
            print(f"Error inserting AQI row {index}: {e}")
            continue

    conn.commit()
    print(f"{aqi_inserted} rows inserted into AirQualityIndex table.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()
    print("MySQL connection closed.")
