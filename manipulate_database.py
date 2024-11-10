import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",          # database's hostname
    user="root",       #  MySQL username
    password="newpassword",   #  MySQL password
    database="demo_db"          #  name of database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Define  SQL INSERT query
query = """
INSERT INTO TireStoreInventory (StoreName, TireSize, Quantity)
VALUES (%s, %s, %s);
"""

# Data to insert (change this in the future so it prompts the user to dynamically input what they want to add to inventory)
data = [
    ('Bedford', '225/65R17', 10),
    ('Pipeline', '225/65R17', 2),
    ('Euless', '225/65R17', 5),
]

# Execute the INSERT query with the data
cursor.executemany(query, data)

# create a temporary table that sums multiple instances of the same location|size combination
#
# Old table:
# 225/60R16 at bedford: 2
# 225/60R16 at bedford: 4
#
# New table:
# 225/60R16 at bedford: 6
cursor.execute("""
            CREATE TEMPORARY TABLE CombinedTireInventory AS
            SELECT StoreName, TireSize, SUM(Quantity) AS TotalQuantity
            FROM TireStoreInventory
            GROUP BY StoreName, TireSize;
        """)

# Delete all rows from the original table
cursor.execute("DELETE FROM TireStoreInventory;")

# Insert the combined data back into the original table
cursor.execute("""
    INSERT INTO TireStoreInventory (StoreName, TireSize, Quantity)
    SELECT StoreName, TireSize, TotalQuantity
    FROM CombinedTireInventory;
""")

# Drop the temporary table
cursor.execute("DROP TEMPORARY TABLE CombinedTireInventory;")

# Commit the changes
connection.commit()

# close cursor and connection
cursor.close()
connection.close()

print("Inventory successfully updated with combined data.")
