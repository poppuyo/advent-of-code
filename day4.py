from typing import List, Dict


class Day4:
    @staticmethod
    def is_valid_guess(guess: int, part_two: bool):
        if guess > 999999 or guess < 100000:
            return False
        if not Day4.has_two_adjacent_digits(guess, part_two):
            return False
        if not Day4.subsequent_digits_increase(guess):
            return False
        return True

    @staticmethod
    def subsequent_digits_increase(guess: int):
        for i in range(5):
            if int(str(guess)[i]) > int(str(guess)[i + 1]):
                return False
        return True

    @staticmethod
    def has_two_adjacent_digits(guess: int, part_two_logic: bool):
        if part_two_logic:
            if str(guess)[3] != str(guess)[4] and str(guess)[4] == str(guess)[5]:
                return True
            if str(guess)[0] == str(guess)[1] and str(guess)[1] != str(guess)[2]:
                return True
            for i in range(1, 5):
                if str(guess)[i - 1] != str(guess)[i] and \
                        str(guess)[i] == str(guess)[i + 1] and \
                        str(guess)[i + 1] != \
                        str(guess)[i + 2]:
                    return True
            return False
        else:
            for i in range(5):
                if str(guess)[i] == str(guess)[i + 1]:
                    return True
            return False

    @staticmethod
    def run():
        password_min: int = 284639
        # password_min: int = 111444
        password_max: int = 748759
        # password_max: int = 111446
        part_one_valid_guess_count: int = 0
        part_two_valid_guess_count: int = 0
        for i in range(password_min, password_max + 1):
            if Day4.is_valid_guess(i, False):
                part_one_valid_guess_count += 1
            if Day4.is_valid_guess(i, True):
                part_two_valid_guess_count += 1
            # print(f'{i}')

        print(f'part1: {part_one_valid_guess_count}, part2: {part_two_valid_guess_count}')


Day4.run()
