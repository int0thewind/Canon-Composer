import random
from typing import Tuple, Set

from src.note import Note, fill_in_thirds, choose_from_inverse_possible_note, choose_from_all_notes, \
    INVERSE_POSSIBLE_NOTE
from src.noteseries import NoteSeries, inverse_notes, reverse_notes


def _prepare(note_num: int) -> Tuple[NoteSeries, NoteSeries, int]:
    if note_num % 2 != 0:
        raise NotImplementedError('Only even length is generated.')
    if not 8 <= note_num <= 16:
        raise NotImplementedError('Only length of 8 to 16 is supported.')
    return [None for _ in range(note_num)], [None for _ in range(note_num)], note_num // 2


def shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[half - 1] = Note(1)

    # Generate fixed middles
    sec[0] = Note.choice(1, 3, 6)
    pri[half - 1] = Note.choice(1, 3, 6)

    # Fill in thirds
    for i in range(1, half - 1):
        pri[i], sec[i] = fill_in_thirds()

    # Fill the rest
    pri[half:note_num] = sec[0:half]
    sec[half:note_num] = pri[0:half]

    return pri, sec


def shift_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[half - 1] = Note(1)

    # Generate fixed middles
    sec[0] = Note.choice(1, 3, 6)
    pri[half - 1] = Note.choice(1, 3, 6)

    # Fill in thirds
    melody_passed = False
    while not melody_passed:
        for i in range(1, half - 1):
            is_start = i == 1
            pri_possible_notes = pri[i - 1].get_next_possible_notes(
                leap=(True if is_start else pri[i - 2] - pri[i - 1] < 2)
            )
            sec_possible_notes = sec[i - 1].get_next_possible_notes(
                leap=(False if is_start else sec[i - 2] - sec[i - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i] = pri_note
                    sec[i] = intersect.pop()
                    break

            i += 1

        melody_passed = pri[half - 2] - pri[half - 1] < 2

    # Fill the rest
    pri[half:note_num] = sec[0:half]
    sec[half:note_num] = pri[0:half]

    return pri, sec


def reverse(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[0] = Note(1)

    # Generate fixed middles
    # NOP

    # Fill in thirds
    for i in range(1, half):
        pri[i], sec[i] = fill_in_thirds()

    # Fill the rest
    pri[half:note_num] = reverse_notes(sec[0:half])
    sec[half:note_num] = reverse_notes(pri[0:half])

    return pri, sec


def reverse_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[0] = Note(1)

    # Generate fixed middles
    # Second notes to be dominant
    sel = [Note(7), Note.choice(2, 5)]
    random.shuffle(sel)
    pri[1], sec[1] = tuple(sel)
    del sel

    # Fill in thirds
    for i in range(2, half):
        is_end = i == half - 1
        pri_possible_notes = pri[i - 1].get_next_possible_notes(
            leap=(False if is_end else pri[i - 2] - pri[i - 1] < 2)
        )
        sec_possible_notes = sec[i - 1].get_next_possible_notes(
            leap=(False if is_end else sec[i - 2] - sec[i - 1] < 2)
        )

        for pri_note in pri_possible_notes:
            sec_possible_thirds: Set[Note] = pri_note.get_thirds()
            intersect = sec_possible_thirds.intersection(sec_possible_notes)
            if len(intersect) > 0:
                pri[i] = pri_note
                sec[i] = intersect.pop()
                break

        i += 1

    # Fill the rest
    pri[half:note_num] = reverse_notes(sec[0:half])
    sec[half:note_num] = reverse_notes(pri[0:half])

    return pri, sec


def reverse_shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[half - 1] = Note(1)
    pri[-1] = Note(1)
    sec[half] = Note(1)

    # Generate fixed middles
    sec[0] = Note.choice(1, 3, 6)
    pri[half - 1] = sec[0]
    pri[half] = Note.choice(1, 3, 6)
    sec[-1] = pri[half]

    # Fill in thirds
    is_odd = half % 2 != 0
    half_half = half // 2

    for i in range(1, half_half):
        pri[i], sec[i] = fill_in_thirds()
        pri[half - i - 1], sec[half - i - 1] = sec[i], pri[i]
    if is_odd:
        pri[half_half] = choose_from_all_notes()
        sec[half_half] = pri[half_half]

    for i in range(1, half_half):
        i2 = i + half
        pri[i2], sec[i2] = fill_in_thirds()
        pri[note_num - i - 1], sec[note_num - i - 1] = sec[i2], pri[i2]
    if is_odd:
        pri[half_half + half] = choose_from_all_notes()
        sec[half_half + half] = pri[half_half + half]

    # Fill the rest
    # NOP

    return pri, sec


def reverse_shift_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    sec[half - 1] = Note(1)
    pri[-1] = Note(1)
    sec[half] = Note(1)

    # Generate fixed middles
    sec[0], pri[half] = random.choice([
        (Note(1), Note(1)),
        (Note(1), Note(3)),
        (Note(1), Note(6)),
        (Note(3), Note(1)),
        (Note(3), Note(3)),
        (Note(6), Note(1)),
        (Note(6), Note(6)),
    ])
    pri[half - 1] = sec[0]
    sec[-1] = pri[half]

    # Fill in thirds
    is_odd = half % 2 != 0
    half_half = half // 2

    first_half_passed = False
    while not first_half_passed:
        for i in range(1, half_half):
            pri_possible_notes = pri[i - 1].get_next_possible_notes(
                leap=(False if i == 1 else pri[i - 2] - pri[i - 1] < 2)
            )
            sec_possible_notes = sec[i - 1].get_next_possible_notes(
                leap=(False if i == 1 else sec[i - 2] - sec[i - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i] = pri_note
                    sec[i] = intersect.pop()
                    pri[half - i - 1], sec[half - i - 1] = sec[i], pri[i]
                    break

        if is_odd:
            pri_possible_notes = pri[half_half - 1].get_next_possible_notes(leap=False)
            sec_possible_notes = sec[half_half - 1].get_next_possible_notes(leap=False)
            intersect = set(pri_possible_notes).intersection(sec_possible_notes)
            if len(intersect) > 0:
                pri[half_half] = intersect.pop()
                sec[half_half] = pri[half_half]
                first_half_passed = True
            else:
                first_half_passed = False
        else:
            first_half_passed = True

    second_half_passed = False
    while not second_half_passed:
        for i in range(1, half_half):
            i2 = i + half
            pri_possible_notes = pri[i2 - 1].get_next_possible_notes(
                leap=(pri[i2 - 2] - pri[i2 - 1] < 2)
            )
            sec_possible_notes = sec[i2 - 1].get_next_possible_notes(
                leap=(sec[i2 - 2] - sec[i2 - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i2] = pri_note
                    sec[i2] = intersect.pop()
                    pri[note_num - i - 1], sec[note_num - i - 1] = sec[i2], pri[i2]
                    break
        if is_odd:
            pri_possible_notes = pri[half_half + half - 1].get_next_possible_notes(leap=False)
            sec_possible_notes = sec[half_half + half - 1].get_next_possible_notes(leap=False)
            intersect = set(pri_possible_notes).intersection(sec_possible_notes)
            if len(intersect) > 0:
                pri[half_half + half] = intersect.pop()
                sec[half_half + half] = pri[half_half + half]
                second_half_passed = True
            else:
                second_half_passed = False
        else:
            second_half_passed = True

    # Fill the rest
    # NOP

    return pri, sec


def inverse_shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half - 1] = Note(5)
    sec[half] = Note(5)

    # Generate fixed middles
    pri[half - 1] = Note.choice(3, 5, 7)
    sec[0] = Note.choice(1, 3, 6)

    # Fill in thirds
    for i in range(1, half - 1):
        pri[i], sec[i] = fill_in_thirds()

    # Fill the rest
    pri[half:note_num] = inverse_notes(sec[0:half])
    sec[half:note_num] = inverse_notes(pri[0:half])

    return pri, sec


def inverse_shift_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half - 1] = Note(5)
    sec[half] = Note(5)

    # Generate fixed middles
    pri[half - 1] = Note.choice(3, 5, 7)
    sec[0] = Note.choice(1, 3, 6)

    # Fill in thirds
    melody_passed = False
    while not melody_passed:
        for i in range(1, half - 1):
            is_start = i == 1
            pri_possible_notes = pri[i - 1].get_next_possible_notes(
                leap=(True if is_start else pri[i - 2] - pri[i - 1] < 2)
            )
            sec_possible_notes = sec[i - 1].get_next_possible_notes(
                leap=(False if is_start else sec[i - 2] - sec[i - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i] = pri_note
                    sec[i] = intersect.pop()
                    break

            i += 1

        melody_passed = pri[half - 2] - pri[half - 1] < 2

    # Fill the rest
    pri[half:note_num] = inverse_notes(sec[0:half])
    sec[half:note_num] = inverse_notes(pri[0:half])

    return pri, sec


def inverse_reverse_shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half - 1] = Note(5)
    sec[half] = Note(5)

    # Generate fixed middles
    sec[0] = Note.choice(1, 3, 6)
    pri[half - 1] = sec[0]
    pri[half] = Note.choice(3, 5, 7)
    sec[-1] = pri[half]

    # Fill in thirds
    is_odd = half % 2 != 0
    half_half = half // 2

    for i in range(1, half_half):
        pri[i], sec[i] = fill_in_thirds()
        pri[half - i - 1], sec[half - i - 1] = sec[i].inv(), pri[i].inv()
    if is_odd:
        pri[half_half] = choose_from_inverse_possible_note()
        sec[half_half] = pri[half_half].inv()

    for i in range(1, half_half):
        i2 = i + half
        pri[i + half], sec[i + half] = fill_in_thirds()
        pri[note_num - i - 1], sec[note_num - i - 1] = sec[i].inv(), pri[i].inv()
    if is_odd:
        pri[half_half + half] = choose_from_inverse_possible_note()
        sec[half_half + half] = pri[half_half + half].inv()

    # Fill the rest
    # NOP

    return pri, sec


def inverse_reverse_shift_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    # Generate headers
    pri[0] = Note(1)
    pri[-1] = Note(1)
    sec[half - 1] = Note(5)
    sec[half] = Note(5)

    # Generate fixed middles
    sec[0], sec[-1] = random.choice([
        (Note(1), Note(1)),
        (Note(1), Note(3)),
        (Note(1), Note(6)),
        (Note(3), Note(1)),
        (Note(3), Note(3)),
        (Note(6), Note(1)),
        (Note(6), Note(6)),
    ])
    pri[half - 1] = sec[0].inv()
    pri[half] = sec[-1].inv()

    # Fill in thirds
    is_odd = half % 2 != 0
    half_half = half // 2

    first_half_passed = False
    while not first_half_passed:
        for i in range(1, half_half):
            pri_possible_notes = pri[i - 1].get_next_possible_notes(
                leap=(False if i == 1 else pri[i - 2] - pri[i - 1] < 2)
            )
            sec_possible_notes = sec[i - 1].get_next_possible_notes(
                leap=(False if i == 1 else sec[i - 2] - sec[i - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i] = pri_note
                    sec[i] = intersect.pop()
                    pri[half - i - 1], sec[half - i - 1] = sec[i].inv(), pri[i].inv()
                    break

        if is_odd:
            pri_possible_notes = pri[half_half - 1].get_next_possible_notes(leap=True)
            sec_possible_notes = sec[half_half - 1].get_next_possible_notes(leap=True)
            # print(pri_possible_notes, sec_possible_notes)
            intersect = set(pri_possible_notes)\
                .intersection(inverse_notes(sec_possible_notes)).intersection(INVERSE_POSSIBLE_NOTE)
            if len(intersect) > 0:
                pri[half_half] = intersect.pop()
                sec[half_half] = pri[half_half].inv()
                first_half_passed = True
            else:
                first_half_passed = False
        else:
            first_half_passed = True

    second_half_passed = False
    while not second_half_passed:
        for i in range(1, half_half):
            i2 = i + half
            pri_possible_notes = pri[i2 - 1].get_next_possible_notes(
                leap=(pri[i2 - 2] - pri[i2 - 1] < 2)
            )
            sec_possible_notes = sec[i2 - 1].get_next_possible_notes(
                leap=(sec[i2 - 2] - sec[i2 - 1] < 2)
            )

            for pri_note in pri_possible_notes:
                sec_possible_thirds: Set[Note] = pri_note.get_thirds()
                intersect = sec_possible_thirds.intersection(sec_possible_notes)
                if len(intersect) > 0:
                    pri[i2] = pri_note
                    sec[i2] = intersect.pop()
                    pri[note_num - i - 1], sec[note_num - i - 1] = sec[i2].inv(), pri[i2].inv()
                    break
        if is_odd:
            pri_possible_notes = pri[half_half + half - 1].get_next_possible_notes(leap=True)
            sec_possible_notes = sec[half_half + half - 1].get_next_possible_notes(leap=True)
            intersect = set(pri_possible_notes)\
                .intersection(inverse_notes(sec_possible_notes)).intersection(INVERSE_POSSIBLE_NOTE)
            if len(intersect) > 0:
                pri[half_half + half] = intersect.pop()
                sec[half_half + half] = pri[half_half + half].inv()
                second_half_passed = True
            else:
                second_half_passed = False
        else:
            second_half_passed = True

    # Fill the rest
    # NOP

    return pri, sec
