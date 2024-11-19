import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
from tkcalendar import DateEntry

# Function to establish a database connection
def get_mysql_connection():
    return mysql.connector.connect(
        host='host',
        user='user',  # Replace with your MySQL username
        password='pwd',  # Replace with your MySQL password
        database='air_quality_data'
    )

# Function to fetch city names from the database
def fetch_cities():
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT City FROM cities")
    cities = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return cities

# Function to fetch a specific record based on city and date
def fetch_single_record(city, date):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    query = """
        SELECT c.city AS "CITY", aqm.Date AS "Date", aqm.PM25 AS "PM25", aqm.PM10 AS "PM10", aqm.NO AS "NO", aqm.NO2 AS "NO2", aqm.NOx AS "NOx", aqm.NH3 AS "NH3", aqm.CO AS "CO", aqm.SO2 AS "SO2", aqm.O3 AS "O3", aqm.Benzene AS "Benzene", aqm.Toluene AS "Toluene", aqm.Xylene AS "Xylene", aqi.AQI AS "AQI", aqi.AQI_Bucket AS "AQI_Bucket"
        FROM cities c
        JOIN airqualitymeasurements aqm ON aqm.CityID = c.CityID
        JOIN airqualityindex aqi ON aqi.MeasurementID = aqm.MeasurementID
        WHERE c.City = %s AND aqm.Date = %s
        ORDER BY c.City, aqm.Date
        LIMIT 1;
    """
    cursor.execute(query, (city, date))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result

# Function to update the table display in Section 3
def update_table():
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT distinct c.city AS "CITY", aqm.Date AS "Date", aqm.PM25 AS "PM25", aqm.PM10 AS "PM10", aqm.NO AS "NO", aqm.NO2 AS "NO2", aqm.NOx AS "NOx", aqm.NH3 AS "NH3", aqm.CO AS "CO", aqm.SO2 AS "SO2", aqm.O3 AS "O3", aqm.Benzene AS "Benzene", aqm.Toluene AS "Toluene", aqm.Xylene AS "Xylene", aqi.AQI AS "AQI", aqi.AQI_Bucket AS "AQI_Bucket"
                    FROM cities c
                    JOIN airqualitymeasurements aqm ON aqm.CityID = c.CityID
                    JOIN airqualityindex aqi ON aqi.MeasurementID = aqm.MeasurementID
                    ORDER BY c.City, aqm.Date""")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for record in records:
        tree.insert("", "end", values=record)

# Function to display a specific record in the GUI
def display_single_record(record):
    # Clear the Treeview before displaying the new record
    for row in tree_1.get_children():
        tree_1.delete(row)

    # Insert the new record into the Treeview (if record is not None)
    if record:
        tree_1.insert("", "end", values=record)

# Function to retrieve a record based on user input
def retrieve_record():
    city = city_combobox.get().strip()
    date = date_selector.get().strip()  # Get date from DateEntry
    
    # Validate date format (optional, as DateEntry usually provides valid dates)
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
        return
    
    record = fetch_single_record(city, date)
    if record:
        display_single_record(record)
    else:
        messagebox.showinfo("No Record", "No record found for the selected city and date.")

# Function to update a specific pollutant value in the database
def update_record():
    city = city_combobox.get().strip()
    date = date_selector.get().strip()
    pollutant = pollutant_combobox.get().strip()
    new_value = new_value_entry.get().strip()

    # Validate new value
    try:
        new_value = float(new_value)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the pollutant level.")
        return

    # Connect to database and call stored procedure
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('UpdatePollutantAndRecalculateAQI', [city, date, pollutant, new_value])
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully.")
        
        # Refresh the retrieved record and the full table
        retrieve_record()
        update_table()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to delete record
def delete_record():
    city = city_combobox.get()
    date = date_selector.get()

    if not city or not date:
        messagebox.showerror("Error", "Please select a city and enter a date.")
        return

    # Confirm deletion
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record for {city} on {date}?")
    if not confirm:
        return

    # Connect to database and call the procedure
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        # Call stored procedure to delete the record
        cursor.callproc('DeleteAirQualityRecord', [city, date])
        conn.commit()

        messagebox.showinfo("Success", "Record deleted successfully.")
        
        # Refresh table to display updated data after deletion
        update_table()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Main application window
root = tk.Tk()
root.title("Air Quality Dashboard")
root.config(bg="thistle")
#root.wm_resizable(False, False)

# heading 1
heading_label = tk.Label(root, text="Air Quality Analysis Using Database Concepts", font=("Times New Roman", 25, "bold"), bg="thistle")
heading_label.pack(pady=20)

heading_label2 = tk.Label(root, text="Fetch A Record to Update or Delete", font=("Times New Roman", 15, "bold"), bg="thistle")
heading_label2.pack(pady=15)
# Section 1 - Retrieve and Update Record
# Frame for inputs and buttons
frame1 = tk.Frame(root)
frame1.pack(pady=10)

# Row 1: City Entry, Date Entry, and Retrieve Record Button
# Frame setup for user input (e.g., for city and date)

# Dropdown selector for city (assuming city_combobox is already defined)
tk.Label(frame1, text="Select City:").grid(row=1, column=0, padx=5, pady=5)
city_combobox = ttk.Combobox(frame1, values=fetch_cities()) 
city_combobox.grid(row=1, column=1, padx=5, pady=5)

# Dropdown date selector
tk.Label(frame1, text="Select Date:").grid(row=1, column=2, padx=5, pady=5)
date_selector = DateEntry(frame1, width=12, background='darkblue', foreground='white', date_pattern='y-mm-dd')
date_selector.grid(row=1, column=3, padx=5, pady=5)

# Retrieve button
retrieve_button = tk.Button(frame1, text="Retrieve Record", command=retrieve_record)
retrieve_button.grid(row=1, column=4, padx=5, pady=5)

# delete button
delete_button = tk.Button(frame1, text="Delete Record", command=delete_record)
delete_button.grid(row=1, column=5, padx=5, pady=5)

# Row 2: Treeview to Display Retrieved Record as a Table
# Columns for Treeview based on labels for pollutants
labels = ["CITY", "Date", "PM25", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene", "AQI", "AQI_Bucket"]

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

# Create Treeview widget
tree_1 = ttk.Treeview(tree_frame, columns=labels, show="headings", height=1)
tree_1.grid(row=2, column=0)

# Define column headings for the Treeview
for col in labels:
    tree_1.heading(col, text=col)
    tree_1.column(col, width=80, anchor="center")

# Row 3: Pollutant Selection, New Value Entry, and Update Record Button
frame2 = tk.Frame(root)
frame2.pack(pady=10)

tk.Label(frame2, text="Select Pollutant to Update:").grid(row=0, column=0, padx=5, pady=5)
pollutant_combobox = ttk.Combobox(frame2, values=labels[2:])  # Pollutant options
pollutant_combobox.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame2, text="Enter New Value:").grid(row=0, column=2, padx=5, pady=5)
new_value_entry = tk.Entry(frame2)
new_value_entry.grid(row=0, column=3, padx=5, pady=5)

update_button = tk.Button(frame2, text="Update Record", command=update_record)
update_button.grid(row=0, column=4, padx=5, pady=5)

heading_label2 = tk.Label(root, text="Add a New Record", font=("Times New Roman", 15, "bold"), bg="thistle")
heading_label2.pack(pady=15)

# Second Section (CRUD Operations)
frame2 = tk.Frame(root)
frame2.pack(pady=10)

# Dropdown for CITY selection
tk.Label(frame2, text="Select City:").grid(row=0, column=0)
city_combobox_2 = ttk.Combobox(frame2, values=fetch_cities())
city_combobox_2.grid(row=1, column=0)

# Date Entry
tk.Label(frame2, text="Select Date").grid(row=0, column=1)
date_entry = DateEntry(frame2, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.grid(row=1, column=1)

# Pollutant Entries
pollutants = ["PM25", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"]
pollutant_entries = {}

for i, pollutant in enumerate(pollutants, start=2):
    tk.Label(frame2, text=f"{pollutant}:").grid(row=0, column=i)
    entry = tk.Entry(frame2, width=10)
    entry.grid(row=1, column=i)
    pollutant_entries[pollutant] = entry

# Function to create a new record
def create_record():
    # Get values from entries
    city = city_combobox_2.get()
    date = date_entry.get()
    pollutant_values = {pollutant: pollutant_entries[pollutant].get() for pollutant in pollutants}

    # Ensure all fields are filled
    if not city or not date or any(not value for value in pollutant_values.values()):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    # Connect to the database
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        # Calculate AQI and AQI_Bucket using stored procedure calculateAQI
        cursor.callproc('calculateAQI', [
            pollutant_values['PM25'],
            pollutant_values['PM10'],
            pollutant_values['CO'],
            pollutant_values['NO2'],
            pollutant_values['SO2'],
            pollutant_values['O3'],
            '@OverallAQI', '@AQIBucket'
        ])
        
        # Retrieve AQI and AQI_Bucket from session variables
        cursor.execute("SELECT @OverallAQI, @AQIBucket")
        aqi_result = cursor.fetchone()
        overall_aqi, aqi_bucket = aqi_result

        # Insert the full record with AQI using AddAirQualityRecord
        cursor.callproc('AddAirQualityRecord', [
            city, date,
            pollutant_values['PM25'], pollutant_values['PM10'], pollutant_values['NO'],
            pollutant_values['NO2'], pollutant_values['NOx'], pollutant_values['NH3'],
            pollutant_values['CO'], pollutant_values['SO2'], pollutant_values['O3'],
            pollutant_values['Benzene'], pollutant_values['Toluene'], pollutant_values['Xylene']
        ])
        
        conn.commit()
        messagebox.showinfo("Success", "Record created successfully.")

        # Refresh table to display the new record
        update_table()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Create Button
create_button = tk.Button(frame2, text="Create", command=create_record)
create_button.grid(row=1, column=15)


# Section 3 - Display All Records
frame3 = tk.Frame(root)
frame3.pack(pady=10)

tk.Label(frame3, text="Records:").pack()

columns = labels
tree = ttk.Treeview(frame3, columns=columns, show='headings', height=20)

# Function to adjust column width based on the longest entry
def adjust_column_width(tree, columns):
    for col in columns:
        max_width = max(len(str(tree.set(item, col))) for item in tree.get_children())  # Longest entry length
        tree.column(col, width=max_width * 10)  # Approximate pixel width (10 per character)

# Set up headers and column alignment
for col in columns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, anchor='center')

tree.pack(expand=True, fill='both')

# Load data initially
update_table()
adjust_column_width(tree, columns)

root.mainloop()
