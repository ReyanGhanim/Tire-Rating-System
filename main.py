import distance_calc
import get_inventory
import calculate_scores

# Prompt user to input receiving store and tire size needed
receiving_store = input("Which store needs tires? ")
size = input("Tire Size: ")


# Get the inventory. Pass size through get_inventory function. This function will return a dictionary with the 
# inventory of that size at each store. 
inventory = get_inventory.main(size)

# Loop through the inventory, if a store's stock is less than 5, that store isn't a candidate to send tires
for stock in inventory:
    if (inventory[stock] < 5):
        inventory.pop(stock)

# Calculate drive times from each store to the receiving store. Inventory is passed so we don't needlessly check
# the distance from a store that doesn't have 5 or more tires in stock
distances = distance_calc.calculate_distances(receiving_store, inventory)

# Pass distances from each store and their inventory into an algorithm that "scores" each store. Highest "score"
# is most optimal
scores = calculate_scores.get_scores(distances, inventory)
optimal_store = max(scores, key=scores.get)
print(f"Optimal store to request {size} from: {optimal_store}")





