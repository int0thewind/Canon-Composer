from typing import List, Optional

from src.note import Note


def reverse(note_list: List[Note]) -> List[Note]:
    list_copy = note_list.copy()
    list_copy.reverse()
    return list_copy


def shift(note_list: List[Note]) -> List[Note]:
    assert len(note_list) % 2 == 0
    middle_point = len(note_list) % 2
    list_copy = note_list.copy()
    list_copy[0: middle_point] = note_list[middle_point: len(note_list)]
    list_copy[middle_point: len(note_list)] = note_list[0: middle_point]
    return list_copy


def leap_check(note_list: List[Note], max_leaps: int) -> bool:
    leaps = 0
    for i in range(len(note_list) - 1):
        if note_list[i] - note_list[i + 1] >= 2:
            leaps += 1
    return leaps <= max_leaps


def unison_check(note_list: List[Note], max_unison: int) -> bool:
    leaps = 0
    for i in range(len(note_list) - 1):
        if note_list[i] - note_list[i + 1] == 0:
            leaps += 1
    return leaps <= max_unison


NoteSeries = List[Optional[Note]]