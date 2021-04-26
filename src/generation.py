import sys
from typing import List, Tuple, Optional
from random import random, choice

from src.note import Note

NoteSeries = List[Optional[Note]]


def randbin() -> int:
    return int(random() < 0.5)


def gen_ret(note_num: int) -> Tuple[NoteSeries, NoteSeries]:
    return [Note(1)] + [None] * (note_num - 1), [Note(1)] + [None] * (note_num - 1)


def reverse(note_num: int):
    ret = gen_ret(note_num)
    half_point = note_num // 2

    # Generate the second
    give_seven = randbin()
    ret[give_seven][1] = Note(7)
    ret[1 - give_seven][1] = choice([Note(2), Note(5)])
    del give_seven

    # Generate the rest
    while (ret[0][half_point - 1] is None) or ret[0][half_point - 1].get_distance(ret[1][half_point - 1]) == 'wide':
        i = 2
        while 0 <= i < half_point:
            primary_prev_distance = ret[0][i - 2].get_distance(ret[0][i - 1])
            secondary_prev_distance = ret[1][i - 2].get_distance(ret[1][i - 1])
            primary_possible_notes = ret[0][i - 1].get_next_possible_notes(
                leap=(primary_prev_distance <= 1),
            )
            secondary_possible_notes = ret[1][i - 1].get_next_possible_notes(
                leap=(secondary_prev_distance <= 1),
            )

            search_success = False

            for note in primary_possible_notes:
                secondary_possible_thirds = note.get_third()
                intersec = secondary_possible_thirds.intersection(secondary_possible_notes)
                if len(intersec) > 0:
                    search_success = True
                    ret[0][i] = note
                    ret[1][i] = choice(list(intersec))
                    break

            i += 1 if search_success else -1

    for i in range(half_point, note_num):
        ret[0][i] = ret[1][note_num - i - 1]
        ret[1][i] = ret[0][note_num - i - 1]

    return ret


def inverse_shift(note_num: int):
    pri, sec = gen_ret(note_num)
    half_point = note_num // 2

    # Generate the middle and the start
    give_five = randbin()
    pri[note_num - half_point - give_five] = Note(3)
    pri[note_num - half_point - (1 - give_five)] = Note(5)
    sec[0] = pri[half_point].get_inverse()
    sec[-1] = pri[half_point - 1].get_inverse()
    pri[-1] = Note(1)
    sec[half_point], sec[half_point - 1] = Note(5), Note(5)
    del give_five

    while pri[half_point - 2] is None or (pri[half_point - 1] in pri[half_point - 2].get_next_possible_notes()):
        i = 1
        while 0 <= i < half_point - 1:
            at_start = i <= 1
            primary_prev_distance = pri[i - 2].get_distance(pri[i - 1]) if not at_start else sys.maxsize
            primary_possible_notes = pri[i - 1].get_next_possible_notes(
                leap=(not at_start or primary_prev_distance <= 1)
            )
            secondary_prev_distance = sec[i - 2].get_distance(sec[i - 1]) if not at_start else sys.maxsize
            secondary_possible_notes = sec[i - 1].get_next_possible_notes(
                leap=(not at_start or secondary_prev_distance <= 1)
            )

            search_success = False

            for note in primary_possible_notes:
                secondary_possible_thirds = note.get_third()
                intersec = secondary_possible_thirds.intersection(secondary_possible_notes)
                while len(intersec) > 0:
                    primary_candidate_collection = pri[i - 1 + half_point].get_next_possible_notes(
                        leap=(pri[half_point + i - 1].get_distance(pri[half_point + i - 2]) <= 1)
                    )
                    primary_candidate = intersec.pop()
                    if primary_candidate in primary_candidate_collection:
                        search_success = True
                        pri[i] = note
                        pri[i + half_point] = primary_candidate.get_inverse()
                        sec[i] = pri[i + half_point].get_inverse()
                        sec[i + half_point] = pri[i].get_inverse()
                        break
                if search_success:
                    break

            i += 1 if search_success else -1

    return pri, sec


if __name__ == '__main__':
    primary, secondary = reverse(32)
    print(primary)
    print(secondary)
