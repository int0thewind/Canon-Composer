from typing import List, Tuple, Optional
from random import random, choice, shuffle

from src.note import Note, INVERSE_POSSIBLE_NOTE, ALL_NOTES

NoteSeries = List[Optional[Note]]


# TODO: meta requirements: Melody no big leap


def _randbin() -> int:
    return int(random() < 0.5)


def _create_note_series(note_num: int) -> Tuple[NoteSeries, NoteSeries]:
    return [None for _ in range(note_num)], [None for _ in range(note_num)]


def shift(note_num: int, reduce_leap: bool = False):
    pri, sec = _create_note_series(note_num)
    half_point = note_num // 2

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half_point - 1] = Note(1)
    sec[half_point] = Note(1)

    # Generate middles
    sel = (Note.choice(1, 3, 6), Note.choice(1, 3, 6))
    pri[half_point - 1], pri[half_point] = sel
    sec[0], sec[-1] = pri[half_point], pri[half_point - 1]
    del sel

    # Generate the rest
    i = 1
    while 1 <= i < half_point - 1:
        pri_possible_notes = pri[i - 1].get_next_possible_notes()
        sec_possible_notes = sec[i - 1].get_next_possible_notes()

        search_success = False

        for pri_note in pri_possible_notes:
            sec_possible_thirds = pri_note.thirds()
            intersect = sec_possible_thirds.intersection(sec_possible_notes)
            if len(intersect) > 0:
                search_success = True
                pri[i] = pri_note
                sec[i] = intersect.pop()
                break

        i += 1 if search_success else -1

    # Fill up the rest
    pri[half_point:len(pri)] = sec[0:half_point]
    sec[half_point:len(pri)] = pri[0:half_point]

    return pri, sec


def reverse(note_num: int, reduce_leap: bool = False):
    pri, sec = _create_note_series(note_num)
    half_point = note_num // 2

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[0] = Note(1)
    sec[1] = Note(1)

    # At lease one should have a leading tone
    sel = [Note(7), Note.choice(2, 5)]
    shuffle(sel)
    pri[1], sec[1] = tuple(sel)
    del sel

    # Generate the rest
    i = 2
    while 1 <= i < half_point:
        pri_possible_notes = pri[i - 1].get_next_possible_notes()
        sec_possible_notes = sec[i - 1].get_next_possible_notes()

        search_success = False
        for pri_note in pri_possible_notes:
            sec_possible_thirds = pri_note.thirds()
            intersect = sec_possible_thirds.intersection(sec_possible_notes)
            if len(intersect) > 0:
                search_success = True
                pri[i] = pri_note
                sec[i] = intersect.pop()
                break

        i += 1 if search_success else -1

    # Fill up the rest
    for i in range(half_point, note_num):
        pri[i] = sec[note_num - i - 1]
        sec[i] = pri[note_num - i - 1]

    return pri, sec


def reverse_shift(note_num: int, reduce_leap: bool = False):
    pri, sec = _create_note_series(note_num)
    half_point = note_num // 2

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half_point - 1] = Note(1)
    sec[half_point] = Note(1)

    # Generate middles
    pri[half_point - 1] = Note.choice(1, 3, 6)
    sec[0] = pri[half_point - 1]
    pri[half_point] = Note.choice(1, 3, 6)
    sec[-1] = pri[half_point]

    # Two sections with same algo
    # TODO: this is literally the mini version of reverse. Coalesce them?
    def reverse_shift_helper(start, end):
        mid = (end - start) // 2

        for ii in range(1, mid):
            i = ii + start
            pri_possible_notes = pri[i - 1].get_next_possible_notes()
            sec_possible_notes = sec[i - 1].get_next_possible_notes()

            search_success = False
            for pri_note in pri_possible_notes:
                sec_possible_thirds = pri_note.thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                # if len(intersect) > 0:
                if len(intersect) > 0:
                    search_success = True
                    pri[i] = pri_note
                    sec[i] = intersect.pop()
                    pri[end - ii - 1] = sec[i]
                    sec[end - ii - 1] = pri[i]
                    break

            assert search_success

            if (end - start) % 2 != 0:
                pri_possible_notes = pri[start + mid].get_next_possible_notes()
                sec_possible_notes = sec[start + mid].get_next_possible_notes()
                intersect = set(pri_possible_notes).intersection(sec_possible_notes)
                assert len(intersect) > 0
                sel = intersect.pop()
                pri[start + mid] = sel
                sec[start + mid] = sel

    reverse_shift_helper(0, half_point)
    reverse_shift_helper(half_point, note_num)

    return pri, sec


def inverse_shift(note_num: int, reduce_leap: bool = False):
    pri, sec = _create_note_series(note_num)
    half_point = note_num // 2

    # Generate fixed notes
    pri[0], pri[-1] = Note(1), Note(1)
    sec[note_num - half_point - 1: note_num - half_point + 1] = [Note(5), Note(5)]

    # Generate the middles that stacks upon the fixed
    pri[note_num - half_point - 1: note_num - half_point + 1] = [Note.choice(3, 5), Note.choice(3, 5)]
    sec[0] = pri[half_point].inv()
    sec[-1] = pri[half_point - 1].inv()
    sec[half_point], sec[half_point - 1] = Note(5), Note(5)

    i = 1
    while 1 <= i < half_point - 1:
        pri_possible_notes = pri[i - 1].get_next_possible_notes()
        sec_possible_notes = sec[i - 1].get_next_possible_notes()

        search_success = False
        for pri_note in pri_possible_notes:
            sec_possible_thirds = pri_note.thirds()
            intersect = sec_possible_thirds.intersection(sec_possible_notes)
            while len(intersect) > 0:
                primary_candidate_collection = pri[i - 1 + half_point].get_next_possible_notes()
                primary_candidate = intersect.pop()
                if primary_candidate in primary_candidate_collection:
                    search_success = True
                    pri[i] = pri_note
                    pri[i + half_point] = primary_candidate.inv()
                    sec[i] = pri[i + half_point].inv()
                    sec[i + half_point] = pri[i].inv()
                    break
            if search_success:
                break

        i += 1 if search_success else -1

    return pri, sec


def inverse_reverse_shift(note_num: int, reduce_leap: bool = False):
    pri, sec = _create_note_series(note_num)
    half_point = note_num // 2

    # Generate fixed notes
    pri[0], pri[-1] = Note(1), Note(1)
    sec[note_num - half_point - 1], sec[note_num - half_point] = Note(5), Note(5)

    # Generate the middles that stacks upon the fixed
    pri[note_num - half_point - 1], pri[note_num - half_point] = Note.choice(3, 5, 7), Note.choice(3, 5, 7)
    sec[0] = pri[half_point - 1].inv()
    sec[-1] = pri[half_point].inv()

    # Two sections with same algo
    def inverse_reverse_shift_helper(start, end):
        mid = (end - start) // 2

        for ii in range(1, mid):
            i = ii + start
            pri_possible_notes = pri[i - 1].get_next_possible_notes()
            sec_possible_notes = sec[i - 1].get_next_possible_notes()

            search_success = False
            for pri_note in pri_possible_notes:
                sec_possible_thirds = pri_note.thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                for sec_note_inv in intersect:
                    sec_note = sec_note_inv.inv()
                    pri_note_inv = pri_note.inv()
                    if sec_note in pri_note_inv.thirds():
                        search_success = True
                        pri[i] = pri_note
                        sec[i] = sec_note_inv
                        pri[end - ii - 1] = sec_note
                        sec[end - ii - 1] = pri_note_inv
                        break

            assert search_success

            if (end - start) % 2 != 0:
                sel = choice(INVERSE_POSSIBLE_NOTE)
                pri[start + mid] = sel
                sec[start + mid] = sel.inv()

    inverse_reverse_shift_helper(0, half_point)
    inverse_reverse_shift_helper(half_point, note_num)

    return pri, sec


def main():
    primary, secondary = inverse_reverse_shift(8)
    print(primary)
    print(secondary)


if __name__ == '__main__':
    main()
