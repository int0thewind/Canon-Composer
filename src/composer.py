import random
from src.note import Note, thirds_generator
from src.noteseries import unison_check, leap_check, NoteSeries
from typing import Tuple


def _prepare(note_num: int) -> Tuple[NoteSeries, NoteSeries, int]:
    if note_num % 2 != 0:
        raise NotImplementedError('Only even length is generated.')
    if not 8 <= note_num <= 16:
        raise NotImplementedError('Only length of 8 to 16 is supported.')
    return [None for _ in range(note_num)], [None for _ in range(note_num)], note_num // 2


def shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def shift_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def reverse(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def reverse_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def shift_reverse(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def shift_reverse_melodic(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def inverse_shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec


def inverse_reverse_shift(note_num: int):
    pri, sec, half = _prepare(note_num)

    return pri, sec
