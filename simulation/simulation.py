import math


"""
Crow Letter
given two points returns the time it would take for a crow to fly between them
sender: center of senders land
recipient: center of recipients land
return: time crow would take to fly between the two
"""
def crow_letter(sender, recipient):
    speed = 44 # average speed of a crow is 44 km/h
    distance = math.dist(sender, recipient)
    return distance / speed # t = x / v


"""
Population Growth
"""
def population_growth():
    pass


"""
Generate Initial Values
"""
def generate_starting_values(num_factions):
    x, y = new_faction_position(num_factions)
    start_vals = {
        "x": x,
        "y": y,

        # TODO: balance starting values
        "population": 10,
        "soldiers": 5,
        "money": 20,
        "food": 3,
        "metals": 5,
    }
    return start_vals


"""
New Faction Position
returns the position of the capital of the new user
operates like a grid spiral search doing one iteration each time a new faction is created
source: https://medium.com/acrossthegalaxy/grid-spiral-search-formula-3b476bfdd2df
n: the number of factions that already exist (works like an index)
return: coordinates of faction capital
"""
def new_faction_position(n):
    k = math.ceil((math.sqrt(n) - 1) / 2)
    t = 2 * k
    m = (t + 1) ** 2

    if n >= m - t:
        return k - (m - n), -k
    else:
        m -= t

    if n >= m - t:
        return -k, -k + (m - n)
    else:
        m -= t

    if n >= m - t:
        return -k + (m - n), k
    else:
        return k, k - (m - n - t)