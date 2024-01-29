#!/usr/bin/env python
#

"""
// This is where you impement your overall strategy to play the game. 
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # The start sequence will run the production bot to take over the cloest
    # planets from its starting planet. The production bot's
    # strategy fits our needs for this. This will only run until a certain
    # number of planets have been taken over. 
    starting_strategy = Sequence(name="Starting Strategy")
    few_planets_check = Check(few_planets)
    start_spread = Action(take_turn)
    starting_strategy.child_nodes = [few_planets_check, start_spread]

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    aggressive_attack = Action(attack)
    offensive_plan.child_nodes = [largest_fleet_check, aggressive_attack]

    spread_plan = Sequence(name='Spread Strategy')
    spread_action = Action(spread)
    spread_plan.child_nodes = [spread_action]

    defensive_plan = Sequence(name='Defensive Strategy')
    defend_action = Action(defend)
    defensive_plan.child_nodes = [defend_action]

    root.child_nodes = [starting_strategy, offensive_plan, spread_plan, defensive_plan]

    logging.info('\n' + root.tree_to_string())
    return root



# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")

