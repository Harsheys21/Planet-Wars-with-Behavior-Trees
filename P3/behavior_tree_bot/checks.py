
import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the game state as a parameter. There are two
conditional checks already implemented here as examples: if_neutral_planet_available 
and have_largest_fleet.
"""

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def few_planets(state):

    total_num_planets = len(state.not_my_planets()) + len(state.my_planets())

    if len(state.my_planets()) <= round(0.25*total_num_planets):
        return True
    
def have_largest_fleet(state):
    
    my_ships = sum(planet.num_ships for planet in state.my_planets()) \
               + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets()) \
                  + sum(fleet.num_ships for fleet in state.enemy_fleets())

    # Adjust for growth rates
    my_growth_rate = sum(planet.growth_rate for planet in state.my_planets())
    enemy_growth_rate = sum(planet.growth_rate for planet in state.enemy_planets())
    future_my_ships = my_ships + my_growth_rate
    future_enemy_ships = enemy_ships + enemy_growth_rate

    return future_my_ships > future_enemy_ships 
