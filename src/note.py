from random import shuffle, choice
from typing import Dict

note_to_midi: Dict[int, int] = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
}

midi_to_note: Dict[int, int] = {
    0: 1,
    2: 2,
    4: 3,
    5: 4,
    7: 5,
    9: 6,
    11: 7,
}


class Note:
    num: int

    @classmethod
    def choice(cls, *args: int):
        return Note(choice(args))

    @classmethod
    def from_midi(cls, midi: int, root: int):
        note = midi_to_note.get(midi % root)
        if isinstance(note, int):
            return cls(note)
        raise ValueError()

    def __init__(self, num: int):
        while num > 7:
            num -= 7
        while num <= 0:
            num += 7
        self.num = num

    def __int__(self):
        return self.num

    def __repr__(self):
        return str(self.num)

    def __str__(self):
        return f'Note: {self.num}'

    def __hash__(self):
        return hash(self.num)

    def _distance(self, other):
        if isinstance(other, Note):
            return self.num - other.num
        raise TypeError()

    def __eq__(self, other):
        return self._distance(other) == 0

    def __lt__(self, other):
        return self._distance(other) < 0

    def __le__(self, other):
        return self._distance(other) <= 0

    def __gt__(self, other):
        return self._distance(other) > 0

    def __ge__(self, other):
        return self._distance(other) >= 0

    def _get_interval(self, interval: int):
        return {Note(self.num - interval), Note(self.num + interval)}

    def get_unison(self):
        return self._get_interval(0)

    def get_second(self):
        return self._get_interval(1)

    def thirds(self):
        return self._get_interval(2)

    def get_forth(self):
        return self._get_interval(3)

    def get_fifth(self):
        return self._get_interval(4)

    def get_sixth(self):
        return self._get_interval(5)

    def get_seventh(self):
        return self._get_interval(6)

    def inv(self):
        return Note(6 - self.num)

    def get_next_possible_notes(self, /, no_option=True, keep=False, step=False, leap=False):
        if no_option:
            ret = list(ALL_NOTES)
            shuffle(ret)
            return ret
        ret = []
        if keep:
            ret += [self]
        if step:
            ret += [Note(self.num - 1), Note(self.num + 1)]
        if leap:
            ret += [Note(self.num - 2), Note(self.num + 2)]
        shuffle(ret)
        return ret

    def dist(self, other) -> int:
        dist = abs(self._distance(other))
        if dist > 3:
            dist = 7 - dist
        return dist

    def __sub__(self, other) -> int:
        dist = abs(self._distance(other))
        if dist > 3:
            dist = 7 - dist
        return dist

    def convert(self, root: int):
        return note_to_midi[self.num] + root


INVERSE_POSSIBLE_NOTE = {
    Note(2), Note(3), Note(4),
}


ALL_NOTES = {
    Note(1), Note(2), Note(3), Note(4), Note(5), Note(6), Note(7),
}
