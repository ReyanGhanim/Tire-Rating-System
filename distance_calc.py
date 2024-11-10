import requests

# Store addresses dictionary
store_addresses = {
    "Bedford": "3928 E Harwood Rd, Bedford, TX 76021", 
    "Pipeline": "2025 Pipeline Rd E, Bedford, TX 76022", 
    "Euless": "4001 South FM 157, Euless, TX 76040",
    "Coppell": "825 S MacArthur Blvd, Coppell, TX 75019", 
    "Saginaw": "108 Anderson St, Saginaw, TX 76179"
}

# function that calculates the drive time between stores
def calculate_distances(receiving_store, check):

    # Check if the receiving store is valid
    if receiving_store not in store_addresses:
        return "Invalid store selection"
    
    # Creating variable to store address of store
    receiving_store_address = store_addresses[receiving_store]

    # initializing drive_time dictionary
    drive_times = {}
    
    # Iterate over each store in the check list
    for store in check:
        if store == receiving_store:
            continue  # Skip if the store is the receiving store (drive time will be 0)
        
        # Retrieve address for sending store, geocode receiving and sending store addresses
        sending_store_address = store_addresses[store]
        geocoded_receiving = geocode_address(receiving_store_address)
        geocoded_sending = geocode_address(sending_store_address)

        # if a geocoded receiving and sending address exist, 
        if geocoded_receiving and geocoded_sending:
            # Get drive time between geocoded coordinates
            delivery_time = get_drive_time(geocoded_sending, geocoded_receiving)

            # store each store's drive time in the "drive_times" dictionary
            drive_times[store] = delivery_time
        else:
            # if the geocoding API call fails, imply that in dictionary
            drive_times[store] = "Geocode failed"

    # print drive times for debugging purposes
    print(f"Drive Time (min): {drive_times}")
    return drive_times

# function that geocodes the address
def geocode_address(address):
    # specify API url
    url = "https://nominatim.openstreetmap.org/search"

    # initialize parameters
    params = {
        # query = address
        'q': address,
        'format': 'json',

        # just one return
        'limit': 1
    }

    # provide a user-agent to the api
    headers = {
        'User-Agent': 'ReyansDistanceCalc (reyanghanim@utexas.edu)' 
    }

    # call api, set api's return to "response"
    response = requests.get(url, params=params, headers=headers)

    # parse the JSON content returned in the HTTP response and convert it into a Python dictionary
    data = response.json()

    # if api pull was successful, pull latitude and longitude data
    # return a comma separated string of longtitude and latitude
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return f"{lon},{lat}"
    else:
        return None

# functin that find the drive time between the geocoded addresses
def get_drive_time(start_coords, end_coords):

    # specify API url
    url = f"http://router.project-osrm.org/route/v1/driving/{start_coords};{end_coords}"

    # set API parameters
    params = {'overview': 'false'}

    # store API's returned data
    response = requests.get(url, params=params)

    # parse the JSON content returned in the HTTP response and convert it into a Python dictionary
    data = response.json()

    try:
        # pull duration from data
        duration_seconds = data['routes'][0]['duration']

        # API returns time in seconds; convert seconds to minutes
        duration_minutes = duration_seconds / 60
        return round(duration_minutes, 2)
    
    # if there is an index or key error, return that drive time isn't available
    except (IndexError, KeyError):
        return "Drive time not available"