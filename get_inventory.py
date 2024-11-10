import mysql.connector 
from distance_calc import store_addresses 

def main(size):

    # establish connection with db
    connection = mysql.connector.connect(host="localhost", user="root", 
                                password="newpassword", database="demo_db") 
    
    # close connection to clear any active queries (this fixed this issue: InternalError("Unread result found") )
    connection.close()

    # Establish connection with db again
    connection = mysql.connector.connect(host="localhost", user="root", 
                                password="newpassword", database="demo_db")

    # Create a cursor object
    cursor = connection.cursor(buffered=True)

    # displaying database to termiinal (this is just so I can verify the algorithm's results)
    query = """SELECT * FROM TireStoreInventory"""
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.nextset()

    # Find how many tires of x size are in stock at a location
    query = """
    SELECT Quantity 
    FROM TireStoreInventory 
    WHERE StoreName = %s AND TireSize = %s
    """
    
    # initialize dictionary to store inventory for each store
    inventory = {}

    # check inventory at each store, add store as key and stock as value in "inventory" dictionary. If a store
    # is out of stock, don't include it in "inventory" dictionary
    for stores in store_addresses:

        # Execute the query
        cursor.execute(query, (stores, size))


        # Fetch the result
        result = str(cursor.fetchone())

        # modify the result so it can be treated as an integer and added to the dictionary
        result = result.strip(",()")
        print(result)
        
        # if the stock is not 0, add the stock to the inventory dictionary
        if result != "None":
            result = int(result)
            inventory.update({stores:result})
        

    # printing inventory for debugging purposes
    print(f"Inventory: {inventory}")
    return(inventory)

if __name__ == "__main__":
    main()