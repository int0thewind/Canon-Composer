from random import shuffle
from typing import Dict

convert_dict: Dict[int, int] = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
}


class Note:
    @staticmethod
    def _calibrate(num: int):
        while num > 7:
            num -= 7
        while num <= 0:
            num += 7
        return num

    def __init__(self, num: int):
        if not 1 <= num <= 7:
            num = Note._calibrate(num)
        self.num = num

    def __int__(self):
        return self.num

    def __repr__(self):
        return f'{self.num}'

    def __str__(self):
        return f'Note: {self.num}'

    def __hash__(self):
        return hash(self.num)

    def _compare(self, other):
        if isinstance(other, Note):
            return self.num - other.num
        raise TypeError()

    def __eq__(self, other):
        return self._compare(other) == 0

    def __lt__(self, other):
        return self._compare(other) < 0

    def __le__(self, other):
        return self._compare(other) <= 0

    def __gt__(self, other):
        return self._compare(other) > 0

    def __ge__(self, other):
        return self._compare(other) >= 0

    def _get_interval(self, interval: int):
        return {Note(self.num - interval), Note(self.num + interval)}

    def get_unison(self):
        return self._get_interval(0)

    def get_second(self):
        return self._get_interval(1)

    def get_third(self):
        return self._get_interval(2)

    def get_forth(self):
        return self._get_interval(3)

    def get_fifth(self):
        return self._get_interval(4)

    def get_sixth(self):
        return self._get_interval(5)

    def get_seventh(self):
        return self._get_interval(6)

    def get_inverse(self):
        if self.num == 1:
            return Note(5)
        if self.num == 2:
            return Note(4)
        if self.num == 3:
            return Note(3)
        if self.num == 4:
            return Note(2)
        if self.num == 5:
            return Note(1)
        if self.num == 6:
            return Note(7)
        if self.num == 7:
            return Note(6)

    def get_next_possible_notes(self, /, keep=False, step=True, leap=True):
        upper_leap = Note(self.num + 2)
        upper_step = Note(self.num + 1)
        lower_step = Note(self.num - 1)
        lower_leap = Note(self.num - 2)
        ret = []
        if keep:
            ret.append(self)
        if step:
            ret.append(lower_step)
            ret.append(upper_step)
        if leap:
            ret.append(lower_leap)
            ret.append(upper_leap)
        shuffle(ret)
        return ret

    def get_distance(self, other) -> int:
        num0 = self.num
        num1 = other.num
        distance = abs(num0 - num1)
        if distance > 3:
            distance = 7 - distance
        return distance

    def convert(self, root: int):
        return convert_dict[self.num] + root
