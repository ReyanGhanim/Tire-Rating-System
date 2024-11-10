import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",         # database hostname
    user="root",              # MySQL username
    password="newpassword", 
    database="demo_db"        # the name of database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Define the SQL query to retrieve data from the table
query = "SELECT * FROM TireStoreInventory;"

# Execute the query
cursor.execute(query)

# Fetch all rows from the executed query
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
