from typing import List, Tuple


class Day5:
    @staticmethod
    def process_opcodes(strip: List[int]) -> List[int]:
        cursor: int = 0
        while True:
            opcode, param_1_mode, param_2_mode, param_3_mode = Day5.process_parameter_mode(str(strip[cursor]))

            if cursor > len(strip):
                break
            if opcode == 99:
                break

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
            except:
                pass

            if opcode == 1:  # add(operand1, operand2)
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                strip[strip[cursor + 3]] = operand_1 + operand_2
                cursor += 4
            elif opcode == 2:  # mult(operand1, operand2)
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                strip[strip[cursor + 3]] = operand_1 * operand_2
                cursor += 4
            elif opcode == 3:
                strip[strip[cursor + 1]] = int(input(f'input for opcode 3? '))
                cursor += 2
            elif opcode == 4:  # print
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                print(operand_1)
                cursor += 2
            elif opcode == 5:  # JUMP IF TRUE (JNZ)
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                if operand_1 != 0:
                    cursor = operand_2
                else:
                    cursor += 3  # if we didn't jump, we need to increment as usual
            elif opcode == 6:  # JUMP IF FALSE (JZ)
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                if operand_1 == 0:
                    cursor = operand_2
                else:
                    cursor += 3  # if we didn't jump, we need to increment as usual
            elif opcode == 7:  # operand3 = 1 if operand1 < operand 2 else 0
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                strip[strip[cursor + 3]] = 1 if operand_1 < operand_2 else 0
                cursor += 4
            elif opcode == 8:  # operand3 = 1 if operand1 == operand 2 else 0
                operand_1 = strip[strip[cursor + 1]] if param_1_mode == 0 else strip[cursor + 1]
                operand_2 = strip[strip[cursor + 2]] if param_2_mode == 0 else strip[cursor + 2]
                strip[strip[cursor + 3]] = 1 if operand_1 == operand_2 else 0
                cursor += 4
            else:
                raise NotImplementedError(f'opcode: {opcode} is not defined, from {strip[cursor]}')

        return strip

    @staticmethod
    def process_parameter_mode(opcode_with_possible_mode_params: str) -> Tuple[int, int, int, int]:
        if len(opcode_with_possible_mode_params) < 1 or len(opcode_with_possible_mode_params) > 6:
            raise ValueError(f'invalid opcode+param combo: {opcode_with_possible_mode_params}')

        opcode: int = int(opcode_with_possible_mode_params[-2:])
        param_1_mode: int = 1 if opcode_with_possible_mode_params[-3:-2] == '1' else 0
        param_2_mode: int = 1 if opcode_with_possible_mode_params[-4:-3] == '1' else 0
        param_3_mode: int = 1 if opcode_with_possible_mode_params[-5:-4] == '1' else 0
        return opcode, param_1_mode, param_2_mode, param_3_mode

    @staticmethod
    def run():
        f = open('inputs/day5.txt', mode='r')
        memory_strip_str: List[str] = f.read().replace('\n', '').split(',')
        memory_strip: List[int] = list(map(lambda val: int(val), memory_strip_str))
        memory_strip_pt_one = memory_strip[:]
        # Day5.sanitize_input(memory_strip_pt_one)
        print(Day5.process_opcodes(memory_strip_pt_one))

    # @staticmethod
    # def run_tests():
    #     return
    #
    #
    # @staticmethod
    # def run_test(input_strip: List[int], expected: List[int]):
    #     mod_input_strip: List[str] = list(map(lambda val: str(val), input_strip)) # compat
    #
    #     Day5.process_opcodes(mod_input_strip)


Day5.run()
