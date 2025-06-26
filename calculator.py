#!/usr/bin/python
##-------------------------------##
## Assembly Lane: Calculator     ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import math
from typing import Any
from pathlib import Path

## Constants
MACHINES: dict[str, float] = {
    'starter1': 0.25,
    'starter2': 0.5,
    'wire': 1.0,
    'cable': 1.0,
    'cutter': 1.0,
    'furnace': 1.0,
    'press': 1.0,
    'crafter1': 1.0,
    'crafter2': 1.0,
    'crafter3': 1.0,
    'crafter4': 1.0,
    'crafter5': 1.0,
    'refinery': 1.0,
}
RECIPES: dict[str, Any] = {}


## Functions
def generate_base_recipes() -> None:
    """Generates all the base item recipes"""
    global MACHINES, RECIPES
    for machine in ('starter1', 'wire', 'cable', 'cutter', 'furnace', 'press'):
        for element in ('aluminium', 'copper', 'diamond', 'gold', 'iron'):
            recipe = { 'machine': machine }
            if machine == 'starter1':
                RECIPES[element] = recipe
            else:
                name: str = f"{element}_"
                if machine == 'cutter':
                    name += "gear"
                elif machine == 'furnace':
                    name += "liquid"
                elif machine == 'press':
                    name += "plate"
                else:
                    name += machine
                if machine == 'cable':
                    recipe['inputs'] = { f'{element}_wire': 3 }
                else:
                    recipe['inputs'] = { element: 1 }
                RECIPES[name] = recipe
    for machine in ('starter2', 'wire', 'cable', 'refinery'):
        for element in ('plutonium', 'uranium'):
            recipe = { 'machine': machine }
            if machine == 'starter2':
                RECIPES[element] = recipe
            else:
                name: str = f"{element}_{machine}" 
                if machine == 'cable':
                    recipe['inputs'] = { f'{element}_wire': 3 }
                else:
                    recipe['inputs'] = { element: 1 }


def add_recipe(output: str, machine: str, **inputs: int) -> None:
    """Adds a recipe and checks to make sure all predecessor items and machines are available"""
    global MACHINES, RECIPES
    if machine not in MACHINES:
        raise KeyError(f"Machine '{machine}' not valid")
    item_stack = list(inputs.keys())
    while item_stack:
        item = item_stack.pop(0)
        item_recipe = RECIPES.get(item, None)
        if item_recipe is None:
            raise KeyError(f"Item '{item}' not valid")
        if item_recipe['machine'] not in ('starter1', 'starter2'):
            item_stack.extend(item_recipe['inputs'].keys())
    # -Valid Item
    RECIPES[output] = {'machine': machine, 'inputs': inputs }
    return output


def get_machine_count(item: str, per_second: float = 1.0) -> dict[str, Any]:
    """Gets total number of machines to produce a certain item/per second"""
    global MACHINES, RECIPES
    recipe = RECIPES[item]
    base_machines = per_second * MACHINES[recipe['machine']]
    machines: dict[str, Any] = {
        'recipe': item,
        'count': base_machines,
    }
    # -Starter found
    if 'inputs' not in recipe:
        return machines
    children = []
    for input_item, input_count in recipe['inputs'].items():
        child = get_machine_count(input_item, input_count * base_machines)
        children.append(child)
    machines['children'] = children
    return machines


def get_starter_count(machine_data: dict[str, Any]) -> float:
    """
    """
    global MACHINES, RECIPES
    starter_count: float = 0
    if not 'children' in machine_data:
        return machine_data['count']
    for child in machine_data['children']:
        starter_count += get_starter_count(child)
    return starter_count


def generate_machine_graph(machine_data: dict[str, Any], file_name: str, format: str = 'png') -> None:
    """
    """
    # -Internal Variables
    import graphviz
    global MACHINES, RECIPES
    _id = 0
    graph = graphviz.Digraph()
    # -Internal Functions
    def _generate_machine_graph(machine_data: dict[str, Any], level=0) -> list[str]:
        '''
        '''
        nonlocal _id
        item = machine_data['recipe']
        count = machine_data['count']
        recipe = RECIPES[item]
        machine = recipe['machine']
        label = ' '.join(n.capitalize() for n in item.split('_'))
        # --Shape:
        # ---Starter=Triangle
        if machine in ('starter1', 'starter2'):
            name = "st"
            shape = "invtriangle"
        # ---Crafter1=Pentagon
        elif machine == 'crafter1':
            name = "c1"
            shape = "pentagon"
        # ---Crafter2=Hexagon
        elif machine == 'crafter2':
            name = "c2"
            shape = "hexagon"
        # ---Crafter3=Octagon
        elif machine == 'crafter3':
            name = "c3"
            shape = "septagon"
        # ---Crafter4=Octagon
        elif machine == 'crafter4':
            name = "c4"
            shape = "octagon"
        # ---Crafter5=Octagon
        elif machine == 'crafter5':
            name = "c5"
            shape = "doubleoctagon"
        # ---Wire, Cable, Cutter, Furnace, Press=Diamond
        else:
            name = machine[:2]
            label = machine.capitalize()
            shape = "diamond"
        name += f"{level}{_id}"
        _id += 1
        graph.node(name, label=label, shape=shape)
        # -Children
        if 'children' not in machine_data:
            return name
        for child in machine_data['children']:
            #child_count = math.ceil(child['count'])
            child_count = round(child['count'], 2)
            child_name = _generate_machine_graph(child, level+1)
            graph.edge(child_name, name, label=str(child_count))
        return name
    # -Body
    _ = _generate_machine_graph(machine_data)
    graph.format = format
    graph.render(f"{file_name}.gv")


## Body
# -Recipes
generate_base_recipes()
# --[Robot]T1
battery = add_recipe('battery', 'crafter1', copper=1, copper_liquid=1)
circuit = add_recipe('circuit', 'crafter1', gold=1, copper_wire=1)
electric_board = add_recipe('electric_board', 'crafter1', aluminium=1, copper_wire=1)
engine = add_recipe('engine', 'crafter1', iron=1, iron_gear=1)
heater_plate = add_recipe('heater_plate', 'crafter1', aluminium=1, iron_wire=1)
solar_cell = add_recipe('solar_cell', 'crafter1', gold=1, diamond_liquid=1)
server_rack = add_recipe('server_rack', 'crafter1', aluminium=1, iron=1)
# --[Robot]T2
fan = add_recipe('fan', 'crafter2', aluminium=6, diamond_gear=3, circuit=1)
power_supply = add_recipe('power_supply', 'crafter2', diamond=6, aluminium_liquid=3, circuit=1)
processor = add_recipe('processor', 'crafter2', gold_liquid=3, diamond_wire=3, circuit=1)
solar_panel = add_recipe('solar_panel', 'crafter2', circuit=1, electric_board=2, solar_cell=2)
advanced_engine = add_recipe('advanced_engine', 'crafter2', diamond=10, circuit=5, engine=5)
computer = add_recipe('computer', 'crafter2', processor=1, power_supply=1, fan=1)
laser = add_recipe('laser', 'crafter2', iron_liquid=5, battery=5, heater_plate=5)
# --[Robot]T3
super_computer = add_recipe('super_computer', 'crafter3', gold_cable=3, circuit=3, server_rack=1, computer=2)
ai_processor = add_recipe('ai_processor', 'crafter3', copper_plate=6, copper_cable=4, circuit=10, super_computer=1)
electric_engine = add_recipe('electric_engine', 'crafter3', iron_plate=5, battery=2, electric_board=2, advanced_engine=2)
robot_arms = add_recipe('robot_arms', 'crafter3', iron=8, aluminium_plate=2, aluminium_cable=3, laser=2)
robot_body = add_recipe('robot_body', 'crafter3', electric_board=5, solar_panel=2, electric_engine=1, robot_arms=1, )
robot_head = add_recipe('robot_head', 'crafter3', gold_plate=5, diamond_cable=10, circuit=10, ai_processor=1)
robot = add_recipe('robot', 'crafter3', iron_plate=10, diamond_cable=5, robot_body=1, robot_head=1)
# --[Bomber]T1
plutonium_cell = add_recipe('plutonium_cell', 'crafter4', plutonium=2, diamond_liquid=2, copper_cable=2, gold_cable=2, solar_cell=2)
plutonium_circuit = add_recipe('plutonium_circuit', 'crafter4', copper=5, plutonium=4, diamond_wire=2, gold_cable=1, circuit=5)
uranium_cell = add_recipe('uranium_cell', 'crafter4', uranium=2, diamond_liquid=2, copper_cable=2, gold_cable=2, solar_cell=2)
uranium_circuit = add_recipe('uranium_circuit', 'crafter4', copper=5, uranium=4, diamond_wire=2, gold_cable=1, circuit=5)
explosive = add_recipe('explosive', 'crafter3', diamond_wire=10, copper_cable=10, circuit=5, heater_plate=10)
trigger = add_recipe('trigger', 'crafter3', iron=40, diamond_wire=10, circuit=5, electric_board=5)
# --[Bomber]T2
ignition_system = add_recipe('ignition_system', 'crafter3', battery=2, ai_processor=2, trigger=2, explosive=5)
nuclear_cell = add_recipe('nuclear_cell', 'crafter4', electric_board=3, heater_plate=3, solar_cell=3, plutonium_cell=1, uranium_cell=1)
nuclear_circuit = add_recipe('nuclear_circuit', 'crafter4', gold_cable=3, circuit=3, processor=3, plutonium_circuit=1, uranium_circuit=1)
nuclear_core = add_recipe('nuclear_core', 'crafter5', diamond_cable=4, gold_cable=4, processor=10, plutonium_cell=1, uranium_cell=1, nuclear_cell=1)
nuclear_processor = add_recipe('nuclear_processor', 'crafter5', diamond_plate=10, processor=5, ai_processor=1, plutonium_circuit=1, uranium_circuit=1, nuclear_circuit=1)
# --[Bomber]T3
atomic_bomb = add_recipe('atomic_bomb', 'crafter5', plutonium=15, uranium=15, ignition_system=1, nuclear_cell=1, nuclear_processor=1, nuclear_core=1)
bomber = add_recipe('bomber', 'crafter5', ai_processor=2, robot=1, nuclear_cell=3, nuclear_processor=1, nuclear_circuit=3, atomic_bomb=1)
# -Machines
data = get_machine_count(robot, 1.5)
count = get_starter_count(data)
print(count)
generate_machine_graph(data, "output")
