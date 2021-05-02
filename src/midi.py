import math
import sys
from math import ceil
from random import choices
from typing import List, Literal, Dict, Tuple
from src.note import Note
from src.canontype import CanonTypeAbbr

NoteLeap = Literal['no_jump', 'jump_up', 'jump_down']


def _choose_from_leaps(d: Dict[int, NoteLeap], jump_prob: float) -> Tuple[int, bool]:
    assert len(d) == 2
    pool: List[int] = []
    probs: List[float] = []
    for k, v in d.items():
        pool.append(k)
        probs.append(1 - jump_prob if v == 'no_jump' else jump_prob)
    choosed_value = choices(pool, probs)[0]
    return choosed_value, d[choosed_value] != 'no_jump'


def _find_possible_notes(prev_midi: int, int_list: List[int]) -> Dict[int, NoteLeap]:
    ret: Dict[int, NoteLeap] = {}
    min_dist = sys.maxsize
    min_candidate = -1
    for i in int_list:
        if (dist := abs(i - prev_midi)) < 12:
            note_leap: NoteLeap = 'jump_down' if i < prev_midi else 'jump_up'
            ret[i] = note_leap
            if dist < min_dist:
                min_dist = dist
                min_candidate = i
    ret[min_candidate] = 'no_jump'
    return ret


def _primary_to_midi(primary: List[Note], root: int) -> List[int]:
    primary_midi: List[int] = [primary[0].convert(root)]
    num_spaces = len(primary) - 1
    possible_leaps = ceil(num_spaces / 5)
    leap_probability = possible_leaps / num_spaces

    total_leaps = 0
    for i in range(1, len(primary)):
        curr_note = primary[i]
        if total_leaps <= possible_leaps:
            curr_note_list = curr_note.get_all_possible_midi(root)
            prev_note_midi = primary_midi[i - 1]
            possible_notes_dict = _find_possible_notes(prev_note_midi, curr_note_list)
            curr_note_midi, is_curr_jumped = _choose_from_leaps(possible_notes_dict, leap_probability)


    return primary_midi


def note_series_to_midi_number(primary: List[Note], canon_type: CanonTypeAbbr):
    pass


def write_midi(primary: List[Note], secondary: List[Note]):
    pass


def main():
    print(_find_possible_notes(60, Note(2).get_all_possible_midi(60)))


if __name__ == '__main__':
    main()
