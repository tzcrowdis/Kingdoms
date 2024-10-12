import math
import numpy as np
import datetime
from django.utils import timezone


"""
Crow Letter
given two points returns the time it would take for a crow to fly between them
sender: center of senders land
recipient: center of recipients land
return: time crow would take to fly between the two
"""
def crow_letter(sender, recipient):
    speed = 44 # average speed of a crow is 44 km/hr
    distance = math.dist(sender, recipient)
    return distance / speed # t = x / v


"""
Scout
Determines how many grid coordinates the scout will reach before returning
start: coordinate scout starts in
direction: the cardinal direction the scout is moving in as a 2D vector (x, y)
total_time: length of journey as designated by user [hrs] 
dist_mod: distance modifier set by world that defines distance in km btwn two grid points [km]
return: list of coordinates scout will come in contact with and time they reach them [[(x, y), t], ...]
"""
def scouting(start, direction, total_time, dist_mod): # TODO total time should be halfed to take into account traveling back?
    speed = 5.1 # avg human walk speed in km/hr
    speed /= dist_mod # normalize speed

    # convert to numpy arrays and normalize direction
    direction = np.array(direction)
    direction = direction / np.linalg.norm(direction)
    start = np.array(start)

    end = speed * direction * total_time + start # x = c * u * t + x_0  (v = c * u)
    end_point = [math.floor(num) if num > 0 else math.ceil(num) for num in end]

    # changes direction and start point of range
    x_adjuster = 1 if start[0] < end_point[0] else -1
    y_adjuster = 1 if start[1] < end_point[1] else -1

    # gets all integers between the start and end points
    x_range = list(range(start[0] + x_adjuster, end_point[0] + x_adjuster, x_adjuster)) # +- 1 to be (,]
    y_range = list(range(start[1] + y_adjuster, end_point[1] + y_adjuster, y_adjuster))

    # build the path
    path = []
    if len(x_range) == len(y_range):
        for i in range(len(x_range)): # along a diagonal so each iteration matches up
            path.append((x_range[i], y_range[i]))
    elif len(x_range) > len(y_range):
        path = [(x, start[1]) for x in x_range] # horizontal
    else:
        path = [(start[0], y) for y in y_range] # vertical
    
    # insert time it would take for scout to reach each point on path
    scout_itinerary = []
    for i in range(len(path)):
        if i == 0: # from start
            scout_itinerary.append([path[i], math.dist(path[i], start) / speed])
        else: # in the middle
            scout_itinerary.append([path[i], math.dist(path[i], path[i - 1]) / speed])
    # from last node to end (not necessarily a point)
    scout_itinerary.append([end, math.dist(end, path[-1]) / speed])

    return scout_itinerary


"""
Population Growth
"""
def population_growth():
    pass


"""
Generate Initial Values for a New Faction
"""
def generate_starting_values(num_factions):

    # TODO search algorithm here to determine new start position NEEDS ALL LAND DATA
    # still use spiral search, just go until you find free land
    x, y = new_faction_position(num_factions)


    start_vals = {
        # TODO rework for land model
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
TODO rewrite as this will only be picking next land to search
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
    


def get_real_timedelta(start, duration, time_mod):
    """
    Given a real time it converts a sim time duration to real time and adds it to it
    start: real datetime
    duration: amount to add to start time in sim time [hrs]
    return: the real datetime
    """
    return start + datetime.timedelta(hours = duration * time_mod)


def get_sim_time(world, time):
    """
    Given a real datetime, returns the simulations datetime
    time: real datetime
    return: sim datetime
    """
    # TODO 
    # (datetime.now(tz=timezone.utc) - world.creation_time).total_seconds() * world.time_modifier
    # from that make year, month, day...? 
    # NOTE opportunity to make unique calendar system
    pass


# TODO if this is to be more sophisticated we need to get the inverse of population growth, etc
def land_snapshot(land, time):
    """
    shows the population, soldiers, resources, battles etc of a land point at a given time
    rolls back time to view the land
    land: land object
    time: real time land was visited
    return: dictionary of data
    """
    return {
        "faction": land.owner.name,
        "resource": land.get_resource(),
        "time_visited": get_sim_time(land.world, time),
    }