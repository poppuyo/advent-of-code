from typing import List, Dict, Tuple, Set
from math import sqrt, atan2, pi


class Day10:
    @staticmethod
    def read_map(raw_string: str) -> List[str]:
        working_stream: str = raw_string
        processed_map: List[str]

        processed_map = working_stream.split('\n')

        # for line in processed_map:
        #     print(line)

        return processed_map

    @staticmethod
    def get_direction_and_magnitude(src_x: int, src_y: int, dst_x: int, dst_y: int) -> Tuple[float, float]:
        # use atan2 for direction because math
        return atan2(dst_y - src_y, dst_x - src_x), sqrt((dst_x - src_x) ** 2 + (dst_y - src_y) ** 2)

    @staticmethod
    def generate_distances_dict(processed_map: List[str], src_x: int, src_y: int) \
            -> Dict[Tuple[int, int], Tuple[float, float]]:
        distance_dict: Dict[Tuple[int, int], Tuple[float, float]] = dict()
        height: int = len(processed_map)
        width: int = len(processed_map[0])
        for y in range(height):
            for x in range(width):
                if processed_map[y][x] == '#':
                    direction, magnitude = Day10.get_direction_and_magnitude(src_x=src_x, src_y=src_y, dst_x=x, dst_y=y)
                    if direction == 0 and magnitude == 0:
                        continue
                    else:
                        distance_dict[(x, y)] = direction, magnitude
        return distance_dict

    @staticmethod
    def get_count_of_unique_vectors(distance_dict: Dict[Tuple[int, int], Tuple[float, float]]) -> int:
        # i.e. get number of visible asteroids from location
        unique_vector_dict: Dict[float, float] = dict()

        for location, dir_and_mag in distance_dict.items():
            vector = dir_and_mag[0]
            magnitude = dir_and_mag[1]
            if vector in unique_vector_dict.keys():
                if unique_vector_dict[vector] < magnitude:
                    unique_vector_dict[vector] = magnitude
                    # print(f'{location[1], location[0]}: direction: {vector} with magnitude:{magnitude} is new smallest')
            else:
                unique_vector_dict[vector] = magnitude
                # print(f'{location[1], location[0]}: direction: {vector} with magnitude:{magnitude} is new')

        return len(unique_vector_dict.keys())

    @staticmethod
    def find_optimal_monitoring_post_location(processed_map: List[str]) -> Tuple[Tuple[int, int], int]:
        height: int = len(processed_map)
        width: int = len(processed_map[0])
        outpost_map: Dict[Tuple[int, int], int] = dict()

        for y in range(height):
            for x in range(width):
                if processed_map[y][x] == '#':
                    distances_dict = Day10.generate_distances_dict(processed_map, x, y)
                    visible_count = Day10.get_count_of_unique_vectors(distances_dict)
                    outpost_map[x, y] = visible_count

        best_count: int = 0
        best_location: Tuple[int, int] = -1, -1
        for location, count in outpost_map.items():
            if count > best_count:
                best_count = count
                best_location = location
        print(f'best_loc: {best_location} with {best_count} visible asteroids')
        return best_location, best_count

    @staticmethod
    def rotate_switch_dictionary(distances_dict: Dict[Tuple[int, int], Tuple[float, float]],
                                 atan2_rotate_value: float) -> Dict[Tuple[float, float], Tuple[int, int]]:
        rotated_switched_dict: Dict[Tuple[float, float], Tuple[int, int]] = dict()

        # "rotate" such that "up" is angle=0
        for coordinates, vectors in distances_dict.items():
            new_atan2: float = vectors[0] + atan2_rotate_value
            if new_atan2 < 0:
                # make everything positive such that the range is 0 to 2*pi
                new_atan2 += 2 * pi
            if (vectors[1], new_atan2) in rotated_switched_dict:
                raise ValueError()
            else:
                rotated_switched_dict[vectors[1], new_atan2] = coordinates
        return rotated_switched_dict

    @staticmethod
    def fire_laser(rotated_switched_dict: Dict[Tuple[float, float], Tuple[int, int]], zap_count: int):
        set_of_fire_angles: Set[float] = set()
        for dist, angle in rotated_switched_dict.keys():
            set_of_fire_angles.add(angle)
        sorted_firing_list: List[float] = sorted(set_of_fire_angles)

        firing_list_cursor: int = 0
        hit_count = 0
        while hit_count < zap_count:
            closest: int = 10000000
            closest_angle = 0
            for dist, angle in rotated_switched_dict.keys():
                if angle == sorted_firing_list[firing_list_cursor]:
                    # print(f'possible candidate found at {rotated_switched_dict[(dist, angle)]} with angle {angle} and dist {dist}')
                    if dist < closest:
                        closest = dist
                        closest_angle = angle
            if closest != 10000000:
                hit_count += 1
                print(
                    f'zap: {hit_count}: {rotated_switched_dict[(closest, closest_angle)]} at angle {closest_angle} and distance {closest}')
                del rotated_switched_dict[closest, sorted_firing_list[firing_list_cursor]]
            # else:
            #     print(f' found nothing to hit at {sorted_firing_list[firing_list_cursor]}')

            if firing_list_cursor < len(sorted_firing_list) - 1:
                firing_list_cursor += 1
            else:
                firing_list_cursor = 0
            if len(rotated_switched_dict) == 0:
                print(f'firing list is empty, exiting!')
                break

    @staticmethod
    def run():
        f = open('inputs/day10.txt', mode='r')
        image_stream: str = f.read()
        processed_map: List[str] = Day10.read_map(image_stream)
        best_location, best_count = Day10.find_optimal_monitoring_post_location(processed_map)

        # part 2
        new_distances_dict: Dict[Tuple[int, int], Tuple[float, float]] = \
            Day10.generate_distances_dict(processed_map, best_location[0], best_location[1])
        atan2_rotate_value = pi / 2
        rotated_switched_dict = Day10.rotate_switch_dictionary(new_distances_dict, atan2_rotate_value)
        Day10.fire_laser(rotated_switched_dict, 200)


Day10.run()
