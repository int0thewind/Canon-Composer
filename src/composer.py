from src.note import Note, fill_in_thirds, choose_from_inverse_possible_note, choose_from_all_notes
from typing import Tuple
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
    sec[0] = Note.choice(3, 5, 7)

    # Fill in thirds
    for i in range(1, half - 1):
        pri[i], sec[i] = fill_in_thirds()

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
