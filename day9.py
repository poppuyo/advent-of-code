from typing import List, Tuple, Optional


class Day9:
    @staticmethod
    def process_opcodes(strip: List[int], op3_arglist: Optional[List[int]] = []) -> List[int]:
        debug: bool = False
        cursor: int = 0
        rel_base_cursor: int = 0
        op3_arglist_cursor: int = 0

        while True:
            opcode, param_1_mode, param_2_mode, param_3_mode = Day9.process_parameter_mode(str(strip[cursor]))

            if cursor > len(strip):
                break
            if opcode == 99:
                break

            if debug:
                blah: List[str] = []
                blah2: List[str] = []
                for i in range(len(strip)):
                    blah.append(str(i).rjust(4))
                print(blah)
                for i in range(len(strip)):
                    blah2.append(str(strip[i]).rjust(4))
                print(blah2)
                try:
                    print(f'\topcode parse[{strip[cursor]}]: '
                          f'op={opcode},p1={param_1_mode},p2={param_2_mode},p3={param_3_mode}')
                    print(
                        f'\tcur={cursor}:op={strip[cursor]},p1={strip[cursor + 1]},p2={strip[cursor + 2]},p3={strip[cursor + 3]}')
                except IndexError:
                    pass

            if opcode == 1:  # add(operand1, operand2)
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                operand_3 = Day9.get_param(param_3_mode, cursor, 3, rel_base_cursor, strip, True)  # output op
                strip[operand_3] = operand_1 + operand_2
                cursor += 4
            elif opcode == 2:  # mult(operand1, operand2)
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                operand_3 = Day9.get_param(param_3_mode, cursor, 3, rel_base_cursor, strip, True)  # output op
                strip[operand_3] = operand_1 * operand_2
                cursor += 4
            elif opcode == 3:
                op3_input_val: int
                if op3_arglist_cursor < len(op3_arglist):
                    op3_input_val = op3_arglist[op3_arglist_cursor]
                    op3_arglist_cursor += 1
                else:
                    op3_input_val = int(input(f'input for opcode 3? '))
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip, True)  # output op
                strip[operand_1] = op3_input_val
                cursor += 2
            elif opcode == 4:  # print
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                print(operand_1)
                cursor += 2
            elif opcode == 5:  # JUMP IF TRUE (JNZ)
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                if operand_1 != 0:
                    cursor = operand_2
                else:
                    cursor += 3  # if we didn't jump, we need to increment as usual
            elif opcode == 6:  # JUMP IF FALSE (JZ)
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                if operand_1 == 0:
                    cursor = operand_2
                else:
                    cursor += 3  # if we didn't jump, we need to increment as usual
            elif opcode == 7:  # operand3 = 1 if operand1 < operand 2 else 0
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                operand_3 = Day9.get_param(param_3_mode, cursor, 3, rel_base_cursor, strip, True)  # output op
                strip[operand_3] = 1 if operand_1 < operand_2 else 0
                cursor += 4
            elif opcode == 8:  # operand3 = 1 if operand1 == operand 2 else 0
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                operand_2 = Day9.get_param(param_2_mode, cursor, 2, rel_base_cursor, strip)
                operand_3 = Day9.get_param(param_3_mode, cursor, 3, rel_base_cursor, strip, True)  # output op
                strip[operand_3] = 1 if operand_1 == operand_2 else 0
                cursor += 4
            elif opcode == 9:  # relative base shift
                operand_1 = Day9.get_param(param_1_mode, cursor, 1, rel_base_cursor, strip)
                rel_base_cursor += operand_1
                cursor += 2
                # raise NotImplementedError(f'opcode: {opcode} is not defined, from {strip[cursor]}')
            else:
                raise NotImplementedError(f'opcode: {opcode} is not defined, from {strip[cursor]}')

        return strip

    @staticmethod
    def get_param(mode: int,
                  cursor: int,
                  cursor_offset: int,
                  rel_base_cursor: int,
                  strip: List[int],
                  get_addr: bool = False) -> int:
        try:
            if mode == 0:
                return strip[strip[cursor + cursor_offset]] if not get_addr else strip[cursor + cursor_offset]
            elif mode == 1:
                return strip[cursor + cursor_offset] if not get_addr else cursor + cursor_offset
            elif mode == 2:
                # rel_base + value of param
                return strip[rel_base_cursor + strip[cursor + cursor_offset]] if not get_addr else rel_base_cursor + strip[cursor + cursor_offset]
            else:
                raise NotImplementedError(f'unsupported param mode: {mode}')
        except IndexError:
            pass

    @staticmethod
    def process_parameter_mode(opcode_with_possible_mode_params: str) -> Tuple[int, int, int, int]:
        if len(opcode_with_possible_mode_params) < 1 or len(opcode_with_possible_mode_params) > 6:
            raise ValueError(f'invalid opcode+param combo: {opcode_with_possible_mode_params}')

        opcode: int = int(opcode_with_possible_mode_params[-2:])
        param_1_mode: int = int(opcode_with_possible_mode_params[-3:-2]) if len(
            opcode_with_possible_mode_params[-3:-2]) == 1 else 0
        param_2_mode: int = int(opcode_with_possible_mode_params[-4:-3]) if len(
            opcode_with_possible_mode_params[-4:-3]) == 1 else 0
        param_3_mode: int = int(opcode_with_possible_mode_params[-5:-4]) if len(
            opcode_with_possible_mode_params[-5:-4]) == 1 else 0
        return opcode, param_1_mode, param_2_mode, param_3_mode

    @staticmethod
    def run():
        f = open('inputs/day9.txt', mode='r')
        memory_strip_str: List[str] = f.read().replace('\n', '').split(',')
        memory_strip: List[int] = list(map(lambda val: int(val), memory_strip_str))
        memory_strip_pt_one = memory_strip[:]
        memory_strip_pt_one.extend([0]*5000)

        print(Day9.process_opcodes(memory_strip_pt_one))

    @staticmethod
    def run_tests():
        print('should output 0: ', end='')
        Day9.run_test([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [1], [3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8])
        print('should output 0: ', end='')
        Day9.run_test([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0],
                      [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 0, 0, 1, 9])
        print('should output 1: ', end='')
        Day9.run_test([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [1],
                      [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 1, 1, 1, 9])
        print('should output 0: ', end='')
        Day9.run_test([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [1],
                      [3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8])
        print('should output 1: ', end='')
        Day9.run_test([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8],
                      [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8])
        print('should output 1: ', end='')
        Day9.run_test([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [-1],
                      [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
        print('should output 0: ', end='')
        Day9.run_test([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0],
                      [3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0])
        print('should output 1219070632396864: ', end='')
        Day9.run_test([1102, 34915192, 34915192, 7, 4, 7, 99, 0], [],
                      [1102, 34915192, 34915192, 7, 4, 7, 99, 1219070632396864])
        print('should output 1125899906842624: ', end='')
        Day9.run_test([104, 1125899906842624, 99], [],
                      [104, 1125899906842624, 99])
        return

    @staticmethod
    def run_test(input_strip: List[int], input_3: List[int], expected: List[int]):
        actual = Day9.process_opcodes(input_strip, input_3)
        if actual != expected:
            print(f'input:\n{input_strip}')
            print(f'actual:\n{actual}')
            print(f'expected:\n{expected}')


# Day7.run()
#Day9.run_tests()
print("============TESTS DONE============\n\n")
Day9.run()
