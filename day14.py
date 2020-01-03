from typing import List, Dict, Tuple
from functools import reduce
import re


class CountMaterial:
    def __init__(self, count: int, material: str):
        self.count: int = count
        self.material: str = material

    def __str__(self):
        return f'{self.count}: {self.material}'


def from_raw_string(raw_str: str) -> List[CountMaterial]:
    ret_list: List[CountMaterial] = []

    regex = r'(\d+)\W?([a-zA-Z]+),?'
    m = re.findall(regex, raw_str)
    for item in m:
        ret_list.append(CountMaterial(count=int(item[0]), material=item[1]))

    print(ret_list)
    return ret_list


def parse_reactions(raw_input: List[str]) -> List[Tuple[List[CountMaterial], List[CountMaterial]]]:
    reaction_list: List[Tuple[List[CountMaterial], List[CountMaterial]]] = []
    for line in raw_input:
        left, right = line.split('=>')
        reaction_list.append((from_raw_string(left), from_raw_string(right)))
    return reaction_list

def find_required_recipe_cost(recipe_list: List[Tuple[List[CountMaterial], List[CountMaterial]]],
                              root_input: str,
                              desired_output: str,
                              desired_output_count: int) -> int:
    active_recipe_list: List[CountMaterial] = []
    for inputs, outputs in recipe_list:
        if desired_output in map(lambda x: x.material, outputs):
            active_recipe_list.append(inputs)

    if len(active_recipe_list) == 0:
        raise RuntimeError(f'desired output material: {desired_output} not found in recipe list')

    return 0

def run():
    f = open('inputs/day14.txt', mode='r')
    raw_input: List[str] = f.read().split(sep='\n')

    recipe_list = parse_reactions(raw_input)
    req_count =  find_required_recipe_cost(recipe_list, 'ORE', 'FUEL', 1)

run()