from typing import Optional, List, Dict, Tuple
import copy
import math


class Day3:
    @staticmethod
    def manhattan_search(strip: List[str]):
        return

    @staticmethod
    def traverse_wire(state: Optional[Dict[Tuple[int, int], str]],
                      dists: Optional[Dict[Tuple[int, int], int]],
                      wire: List[str],
                      wire_char: str
                      ) -> Tuple[Dict[Tuple[int, int], str], Dict[Tuple[int,int], int]]:
        position: Tuple[int, int] = (0, 0)
        direction: Tuple[int, int] = (0, 0)
        wire_dist: int = 0

        if state is None:
            state: Dict[Tuple[int, int], str] = dict()
            state[(0, 0)] = 'o'  # origin

        if dists is None:
            dists: Dict[Tuple[int, int], int] = dict()
            dists[(0, 0)] = 0

        for vector in wire:
            if vector[0] == 'R':
                direction = (1, 0)
            elif vector[0] == 'L':
                direction = (-1, 0)
            elif vector[0] == 'U':
                direction = (0, -1)
            elif vector[0] == 'D':
                direction = (0, 1)
            magnitude = int(vector[1:])
            for c in range(magnitude):
                wire_dist += 1
                position = (position[0] + direction[0], position[1] + direction[1])
                if position in state:
                    if state[position] != wire_char and state[position] != 'o':  # if not origin and not intersecting self
                        state[position] = 'x'
                        dists[position] = wire_dist
                    else:
                        state[position] = '+'
                        if dists[position] > wire_dist:
                            dists[position] = wire_dist

                else:
                    state[position] = wire_char  # no wire was here before
                    dists[position] = wire_dist
        return state, dists

    @staticmethod
    def debug_draw(state: Dict[Tuple[int, int], str]):
        x_coords: List[int] = []
        y_coords: List[int] = []
        x_coords, y_coords = zip(*state.keys())
        x_offset: int = abs(min(x_coords))
        y_offset: int = abs(min(y_coords))
        grid: List[List[str]] = []

        # for position, value in state:


    @staticmethod
    def run():
        f = open('inputs/day3-1.txt', mode='r')
        wire_1: List[str] = f.readline().strip().split(',')
        wire_2: List[str] = f.readline().strip().split(',')
        first_dist: Dict[Tuple[int, int], int] = dict()
        second_dist: Dict[Tuple[int, int], int] = dict()

        print(wire_1)
        state, first_dist = Day3.traverse_wire(None, None, wire_1, 'a')
        print(wire_2)
        state, second_dist = Day3.traverse_wire(state, None, wire_2, 'b')

        manhattan_distances: List[int] = []
        wire_distances: List[int] = []

        intersections: List[Tuple[int, int]] = []

        for coordinate, value in state.items():
            if value == 'x':
                manhattan_distances.append(abs(coordinate[0]) + abs(coordinate[1]))
                intersections.append(coordinate)
                #wire_distances.append(state.get(coordinate))
                #print(f'{coordinate} = {state.get(coordinate)}')
                wire_distances.append(first_dist[coordinate] + second_dist[coordinate])
        print(min(manhattan_distances))
        print(min(wire_distances))

        #Day3.debug_draw(state[0])
Day3.run()