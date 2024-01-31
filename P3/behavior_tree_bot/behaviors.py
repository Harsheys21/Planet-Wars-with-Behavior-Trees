import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


"""
Here is where you will implement your functions for action nodes, typically issuing orders. 
Each function should only take the game state as a parameter. There are two actions already 
implemented here as examples: attack_weakest_enemy_planet and spread_to_weakest_neutral_planet.
"""

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)



# Spread from spread bot. 
def spread(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

# From spread bot. 
def attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

# From Production Bot 
def take_turn(state):
    
    if not state.my_planets():
        # Handle the case when there are no planets owned by the player
        return False

    closest = float('inf')
    closest_target = None

    neutral_planets = state.neutral_planets()
    i = 0  # Initialize counter for while loop

    # Use while loop to iterate through neutral planets
    while i < len(neutral_planets):
        planet = neutral_planets[i]
        distance = state.distance(state.my_planets()[0].ID, planet.ID)

        if distance < closest:
            ships_needed = planet.num_ships + 1
            if state.my_planets()[0].num_ships > ships_needed:
                closest = distance
                closest_target = planet

        i += 1  # Increment counter

    if closest_target:
        return issue_order(state, state.my_planets()[0].ID, closest_target.ID, ships_needed)
    
    return False

    
def defend(state):

    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return False  # Defense not possible

    def strength(p):
        return p.num_ships + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if not weak_planets or not strong_planets:
        return False  # Defense not possible

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    weak_planet = next(weak_planets, None)
    strong_planet = next(strong_planets, None)
    if strong_planet is None or weak_planet is None:
        return False

    need = int(avg - strength(weak_planet))
    have = int(strength(strong_planet) - avg)

    if have >= need > 0:
        return issue_order(state, strong_planet.ID, weak_planet.ID, need)
    else:
        return issue_order(state, strong_planet.ID, weak_planet.ID, have)import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


"""
Here is where you will implement your functions for action nodes, typically issuing orders. 
Each function should only take the game state as a parameter. There are two actions already 
implemented here as examples: attack_weakest_enemy_planet and spread_to_weakest_neutral_planet.
"""

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)



# Spread from spread bot. 
def spread(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

# From spread bot. 
def attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

# From Production Bot 
def take_turn(state):
    
    if not state.my_planets():
        # Handle the case when there are no planets owned by the player
        return False

    closest = float('inf')
    closest_target = None

    neutral_planets = state.neutral_planets()
    i = 0  # Initialize counter for while loop

    # Use while loop to iterate through neutral planets
    while i < len(neutral_planets):
        planet = neutral_planets[i]
        distance = state.distance(state.my_planets()[0].ID, planet.ID)

        if distance < closest:
            ships_needed = planet.num_ships + 1
            if state.my_planets()[0].num_ships > ships_needed:
                closest = distance
                closest_target = planet

        i += 1  # Increment counter

    if closest_target:
        return issue_order(state, state.my_planets()[0].ID, closest_target.ID, ships_needed)
    
    return False

    
def defend(state):

    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return False  # Defense not possible

    def strength(p):
        return p.num_ships + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if not weak_planets or not strong_planets:
        return False  # Defense not possible

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    weak_planet = next(weak_planets, None)
    strong_planet = next(strong_planets, None)
    if strong_planet is None or weak_planet is None:
        return False

    need = int(avg - strength(weak_planet))
    have = int(strength(strong_planet) - avg)

    if have >= need > 0:
        return issue_order(state, strong_planet.ID, weak_planet.ID, need)
    else:
        return issue_order(state, strong_planet.ID, weak_planet.ID, have)