
# function that scores each store for its stock and distance from the receiving store
def get_scores(distances, inventory):

    # initialize a dictionary to store scores
    scores = {}

    # iterate through each location in the inventory dictionary. only calculate score if the location is not 
    # the receiving location (this prevents division by 0)
    for location in inventory:
        if location in distances:
            
            # calculate score
            score = (.7*(inventory[location] / max(inventory.values()))) + .3*(min(distances.values()) / (distances[location]))
            
            # store score in scores dictionary
            scores[location] = score

    """
    There's a ton of potential for this scoring algorithm. This is just what I came up with off the top of my head.
    A few other things it can take into consideration in the future: Availability of employees at each store, how much a
    store tends to sell a specific tire size based on past sales rates, etc.
    """

    return scores
