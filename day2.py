from typing import List, Dict


def process_opcodes(strip: List[str]):
    cursor: int = 0
    while True:
        # print(cursor)
        if cursor > len(strip):
            break
        if int(strip[cursor]) == 99:
            break
        if int(strip[cursor]) == 1:
            strip[int(strip[cursor + 3])] = str(int(strip[int(strip[cursor + 1])]) + int(strip[int(strip[cursor + 2])]))
        elif int(strip[cursor]) == 2:
            strip[int(strip[cursor + 3])] = str(int(strip[int(strip[cursor + 1])]) * int(strip[int(strip[cursor + 2])]))
        else:
            # raise NotImplementedError(f'opcode: {strip[cursor]} is not defined!')
            return None
        cursor += 4
    # print(strip)

    return strip


def run():
    f = open('inputs/day2-1.txt', mode='r')
    memory_strip: List[str] = f.read().split(',')
    memory_strip_pt_one = memory_strip[:]
    # part 1
    print('original: ')
    print(memory_strip_pt_one)
    memory_strip_pt_one[1] = '12'
    memory_strip_pt_one[2] = '2'
    print('answer_1: ')
    process_opcodes(memory_strip_pt_one)

    for i in range(0, 100):
        for j in range(0, 100):
            # print(f'noun: {i}, verb: {j}')
            memory_search_strip: List[str] = memory_strip[:]
            memory_search_strip[1] = str(i)
            memory_search_strip[2] = str(j)
            to_test: List[str] = process_opcodes(memory_search_strip)
            if to_test is not None and to_test[0] == '19690720':
                print(f'noun: {i}, verb: {j} - result: {to_test[0]}')

