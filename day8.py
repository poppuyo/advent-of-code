from typing import List, Dict
from functools import reduce


def split_into_layers(image: str, w: int, h: int) -> Dict[int, List[List[int]]]:
    working_stream: str = image
    processed_image_layers: Dict[int, List[List[int]]] = dict()

    counter: int = 0
    while len(working_stream) > 0:
        working_layers: List[List[int]] = []
        for height_counter in range(h):
            working_list: List[int] = []
            for pixel in working_stream[:w]:
                working_list.append(int(pixel))
            working_stream = working_stream[w:]  # 'consume' from stream
            working_layers.append(working_list)
        processed_image_layers[counter] = working_layers
        counter += 1

    return processed_image_layers

def find_layer_with_smallest_instances_of_n(processed_image_layers: Dict[int, List[List[int]]], n: int) -> int:
    min_count: int = 99999
    candidate_layer: int = -1
    for layer_num, layer in processed_image_layers.items():
        layer_count: int = get_count_of_n_in_layer(layer, n)
        if layer_count < min_count:
            min_count = layer_count
            candidate_layer = layer_num
    return candidate_layer

def get_count_of_n_in_layer(layer: List[List[int]], n: int) -> int:
    #  https://www.geeksforgeeks.org/python-ways-to-flatten-a-2d-list/
    flattened_list: List[int] = reduce(lambda a, b: a + b, layer)
    return sum(map(lambda pixel: 1 if pixel == n else 0, flattened_list))

def decode_image(layer_dict: Dict[int, List[List[int]]]):
    working_image: List[List[int]] = []
    h = len(layer_dict[0])
    w = len(layer_dict[0][0])

    working_image = [[-1 for i in range(w)] for j in range(h)]
    for y in range(h):
        for x in range(w):
            pixel = 2
            for i in range(len(layer_dict.keys())):
                if layer_dict[i][y][x] != 2:
                    pixel = layer_dict[i][y][x]
                    break
            if pixel == 2:
                raise RuntimeError('pixel is still 2')
            else:
                # print(f'setting pixel: [{y}][{x}] = {pixel}')
                working_image[y][x] = pixel

    for line in working_image:
        for pixel in line:
            if pixel == 0:
                print('█', end='')
            else:
                print(' ', end='')
        print()

def helper_show_layers(layered_image: Dict[int, List[List[int]]]):
    for layer_num, layer in layered_image.items():
        print(f'Layer {layer_num}:')
        for line in layer:
            print('\t', end='')
            for pixel in line:
                print(pixel, end='')
            print()

def run():
    f = open('inputs/day8.txt', mode='r')
    image_stream: str = f.read()
    layered_image: Dict[int, List[List[int]]] = split_into_layers(image_stream, 25, 6)
    # start part 1
    layer_num: int = find_layer_with_smallest_instances_of_n(layered_image, 0)
    print(f'{get_count_of_n_in_layer(layered_image[layer_num], 1) * get_count_of_n_in_layer(layered_image[layer_num], 2)}')
    # end part 1
    print()
    # start part 2
    # Day8.helper_show_layers(layered_image)
    decode_image(layered_image)
    # end part 2
